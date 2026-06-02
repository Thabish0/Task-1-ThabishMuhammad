from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import re
import sqlite3
import os
from utils.entropy import calculate_entropy
from utils.breach_checker import BreachChecker
from utils.recommendation import get_recommendations
from utils.scorer import calculate_score

app = Flask(__name__)
CORS(app)

# Load ML model
model = None
try:
    if os.path.exists('models/password_model.pkl'):
        model = joblib.load('models/password_model.pkl')
        print("✅ ML Model loaded successfully")
    else:
        print("⚠️ Model not found. Please run train_model.py first")
except Exception as e:
    print(f"❌ Error loading model: {e}")

# Initialize breach checker
breach_checker = BreachChecker()

# Password strength class mapping
STRENGTH_CLASSES = ['Weak', 'Medium', 'Strong', 'Very Strong']

def extract_features(password):
    """Extract features from password for ML model"""
    length = len(password)
    uppercase_count = sum(1 for c in password if c.isupper())
    lowercase_count = sum(1 for c in password if c.islower())
    digit_count = sum(1 for c in password if c.isdigit())
    special_count = sum(1 for c in password if not c.isalnum())
    entropy = calculate_entropy(password)
    
    return [length, uppercase_count, lowercase_count, digit_count, special_count, entropy]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_password():
    try:
        data = request.json
        password = data.get('password', '')
        
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        
        # Basic security: Input sanitization
        if len(password) > 100:
            return jsonify({'error': 'Password too long'}), 400
        
        # Extract features
        features = extract_features(password)
        
        # ML Prediction
        ml_prediction = None
        if model:
            features_array = np.array(features).reshape(1, -1)
            prediction_class = model.predict(features_array)[0]
            ml_prediction = STRENGTH_CLASSES[prediction_class]
        
        # Calculate entropy
        entropy = calculate_entropy(password)
        
        # Check breach status
        breach_status = breach_checker.check_breach(password)
        
        # Calculate score
        score = calculate_score(password, entropy)
        
        # Get recommendations
        recommendations = get_recommendations(password, entropy, score)
        
        # Get character breakdown
        char_breakdown = {
            'length': len(password),
            'uppercase': sum(1 for c in password if c.isupper()),
            'lowercase': sum(1 for c in password if c.islower()),
            'digits': sum(1 for c in password if c.isdigit()),
            'special': sum(1 for c in password if not c.isalnum())
        }
        
        # Determine strength level for meter
        if score < 30:
            strength_level = 'very-weak'
        elif score < 50:
            strength_level = 'weak'
        elif score < 70:
            strength_level = 'medium'
        elif score < 90:
            strength_level = 'strong'
        else:
            strength_level = 'very-strong'
        
        # Live feedback checks
        checks = {
            'length': len(password) >= 12,
            'uppercase': char_breakdown['uppercase'] > 0,
            'lowercase': char_breakdown['lowercase'] > 0,
            'digits': char_breakdown['digits'] > 0,
            'special': char_breakdown['special'] > 0,
            'entropy': entropy >= 60
        }
        
        return jsonify({
            'success': True,
            'ml_prediction': ml_prediction,
            'entropy': round(entropy, 2),
            'score': score,
            'breach_status': breach_status,
            'recommendations': recommendations,
            'char_breakdown': char_breakdown,
            'checks': checks,
            'strength_level': strength_level,
            'strength_text': ml_prediction if ml_prediction else get_strength_from_score(score)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['GET'])
def generate_password():
    """Generate a strong random password"""
    import random
    import string
    
    length = 16
    uppercase = random.choices(string.ascii_uppercase, k=3)
    lowercase = random.choices(string.ascii_lowercase, k=6)
    digits = random.choices(string.digits, k=4)
    special = random.choices('!@#$%^&*', k=3)
    
    password_list = uppercase + lowercase + digits + special
    random.shuffle(password_list)
    password = ''.join(password_list)
    
    return jsonify({'password': password})

def get_strength_from_score(score):
    if score < 30:
        return 'Very Weak'
    elif score < 50:
        return 'Weak'
    elif score < 70:
        return 'Medium'
    elif score < 90:
        return 'Strong'
    else:
        return 'Very Strong'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)