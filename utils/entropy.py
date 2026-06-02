import math
from collections import Counter

def calculate_entropy(password):
    """
    Calculate Shannon entropy of a password.
    Higher entropy means more randomness and stronger password.
    """
    if not password:
        return 0.0
    
    # Count character frequencies
    password_length = len(password)
    char_counts = Counter(password)
    
    # Calculate entropy
    entropy = 0.0
    for count in char_counts.values():
        probability = count / password_length
        entropy -= probability * math.log2(probability)
    
    # Scale entropy by length
    total_entropy = entropy * password_length
    
    return total_entropy

def get_entropy_level(entropy):
    """
    Classify entropy level
    """
    if entropy < 30:
        return "Very Weak", "red"
    elif entropy < 50:
        return "Weak", "orange"
    elif entropy < 70:
        return "Medium", "yellow"
    elif entropy < 90:
        return "Strong", "lightgreen"
    else:
        return "Excellent", "green"