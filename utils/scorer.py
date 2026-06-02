def calculate_score(password, entropy):
    """
    Calculate password security score out of 100 based on multiple criteria
    """
    score = 0
    
    # Length criteria (20 points)
    length = len(password)
    if length >= 16:
        score += 20
    elif length >= 12:
        score += 18
    elif length >= 10:
        score += 14
    elif length >= 8:
        score += 10
    elif length >= 6:
        score += 5
    else:
        score += 0
    
    # Uppercase criteria (15 points)
    uppercase_count = sum(1 for c in password if c.isupper())
    if uppercase_count >= 3:
        score += 15
    elif uppercase_count >= 1:
        score += 10
    else:
        score += 0
    
    # Lowercase criteria (15 points)
    lowercase_count = sum(1 for c in password if c.islower())
    if lowercase_count >= 4:
        score += 15
    elif lowercase_count >= 1:
        score += 10
    else:
        score += 0
    
    # Numbers criteria (15 points)
    digit_count = sum(1 for c in password if c.isdigit())
    if digit_count >= 3:
        score += 15
    elif digit_count >= 1:
        score += 10
    else:
        score += 0
    
    # Special characters criteria (15 points)
    special_count = sum(1 for c in password if not c.isalnum())
    if special_count >= 3:
        score += 15
    elif special_count >= 1:
        score += 10
    else:
        score += 0
    
    # Entropy criteria (20 points)
    if entropy >= 80:
        score += 20
    elif entropy >= 60:
        score += 16
    elif entropy >= 40:
        score += 12
    elif entropy >= 20:
        score += 8
    else:
        score += 4
    
    # Bonus for character variety
    has_upper = uppercase_count > 0
    has_lower = lowercase_count > 0
    has_digit = digit_count > 0
    has_special = special_count > 0
    variety_count = sum([has_upper, has_lower, has_digit, has_special])
    
    if variety_count == 4:
        score = min(100, score + 5)
    
    return min(100, score)

def get_score_level(score):
    """
    Get descriptive level based on score
    """
    if score < 30:
        return "Very Weak", "#dc3545"
    elif score < 50:
        return "Weak", "#fd7e14"
    elif score < 70:
        return "Medium", "#ffc107"
    elif score < 90:
        return "Strong", "#28a745"
    else:
        return "Very Strong", "#198038"