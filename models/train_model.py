import sys
import os
# Add the parent directory (project root) to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import re
from utils.entropy import calculate_entropy


def generate_dataset():
    """Generate synthetic password dataset with strength labels"""
    passwords = []
    strengths = []
    
    # Define password patterns and their strengths
    weak_passwords = [
        '123456', 'password', '12345678', 'qwerty', 'abc123',
        'admin', 'welcome', 'letmein', 'password123', '12345',
        'passw0rd', 'iloveyou', 'sunshine', 'qwerty123', 'monkey'
    ]
    
    medium_passwords = [
        'Passw0rd123', 'SecurePass99', 'HelloWorld7', 'Summer2023',
        'Football99', 'Password123!', 'Welcome2023', 'Computer22',
        'Admin@123', 'User@2023'
    ]
    
    strong_passwords = [
        'P@ssw0rd2023!', 'Secure#Pass99', 'Hello@World77', 'Summer$2024',
        'C0mplex!P@ss', 'Str0ng!P@ssw0rd', 'V3ry!Secure#2024', 'R@nd0m$tr0ng'
    ]
    
    very_strong_passwords = [
        'X#9kL$2mNp@4qR!7', 'P@55w0rd!S3cur3#2024', 'C0mpl3x#P@$$w0rd!2024',
        'R@nd0m!S3cur3#K3y$99', 'V3ry!Str0ng#P@ssw0rd$2024'
    ]
    
    # Generate weak passwords (with variations)
    for pwd in weak_passwords:
        passwords.append(pwd)
        strengths.append(0)  # Weak
        # Add variations
        for _ in range(5):
            var_pwd = pwd + str(np.random.randint(10, 99))
            passwords.append(var_pwd)
            strengths.append(0)
    
    # Generate medium passwords
    for pwd in medium_passwords:
        passwords.append(pwd)
        strengths.append(1)  # Medium
        # Add variations
        for _ in range(8):
            var_pwd = pwd + str(np.random.choice(['!', '@', '#', '$']))
            passwords.append(var_pwd)
            strengths.append(1)
    
    # Generate strong passwords
    for pwd in strong_passwords:
        passwords.append(pwd)
        strengths.append(2)  # Strong
        for _ in range(10):
            var_pwd = pwd + str(np.random.randint(10, 999))
            passwords.append(var_pwd)
            strengths.append(2)
    
    # Generate very strong passwords
    for pwd in very_strong_passwords:
        passwords.append(pwd)
        strengths.append(3)  # Very Strong
        for _ in range(15):
            # Create complex variations
            chars = list(pwd)
            np.random.shuffle(chars)
            var_pwd = ''.join(chars)
            passwords.append(var_pwd)
            strengths.append(3)
    
    # Generate additional random passwords
    for _ in range(500):
        length = np.random.randint(6, 20)
        has_upper = np.random.choice([True, False])
        has_lower = np.random.choice([True, False])
        has_digit = np.random.choice([True, False])
        has_special = np.random.choice([True, False])
        
        chars = []
        if has_upper:
            chars.extend(np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), size=np.random.randint(1, 4)))
        if has_lower:
            chars.extend(np.random.choice(list('abcdefghijklmnopqrstuvwxyz'), size=np.random.randint(3, 8)))
        if has_digit:
            chars.extend(np.random.choice(list('0123456789'), size=np.random.randint(1, 4)))
        if has_special:
            chars.extend(np.random.choice(list('!@#$%^&*'), size=np.random.randint(1, 3)))
        
        if len(chars) < length:
            chars.extend(np.random.choice(list('abcdefghijklmnopqrstuvwxyz'), size=length - len(chars)))
        
        np.random.shuffle(chars)
        password = ''.join(chars)
        
        # Determine strength based on complexity
        length_score = len(password) >= 12
        upper_score = has_upper
        lower_score = has_lower
        digit_score = has_digit
        special_score = has_special
        complexity = sum([length_score, upper_score, lower_score, digit_score, special_score])
        
        if complexity <= 2:
            strength = 0
        elif complexity == 3:
            strength = 1
        elif complexity == 4:
            strength = 2
        else:
            strength = 3
            
        passwords.append(password)
        strengths.append(strength)
    
    # Create DataFrame
    df = pd.DataFrame({'password': passwords, 'strength': strengths})
    
    # Extract features
    features = []
    for pwd in passwords:
        features.append([
            len(pwd),
            sum(1 for c in pwd if c.isupper()),
            sum(1 for c in pwd if c.islower()),
            sum(1 for c in pwd if c.isdigit()),
            sum(1 for c in pwd if not c.isalnum()),
            calculate_entropy(pwd)
        ])
    
    feature_df = pd.DataFrame(features, columns=['length', 'uppercase', 'lowercase', 'digits', 'special', 'entropy'])
    
    return feature_df, df['strength']

def train_model():
    """Train Random Forest model for password strength prediction"""
    print("Generating dataset...")
    X, y = generate_dataset()
    
    print(f"Dataset shape: {X.shape}")
    print(f"Class distribution:\n{y.value_counts()}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train Random Forest
    print("\nTraining Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Weak', 'Medium', 'Strong', 'Very Strong']))
    
    # Feature importance
    feature_names = ['length', 'uppercase', 'lowercase', 'digits', 'special', 'entropy']
    importance = rf_model.feature_importances_
    print("\nFeature Importance:")
    for name, imp in zip(feature_names, importance):
        print(f"  {name}: {imp:.4f}")
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(rf_model, 'models/password_model.pkl')
    print("\n✅ Model saved to 'models/password_model.pkl'")

if __name__ == '__main__':
    train_model()