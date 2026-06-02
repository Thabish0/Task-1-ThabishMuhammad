def get_recommendations(password, entropy, score):
    """
    Generate intelligent recommendations for password improvement
    """
    recommendations = []
    
    # Length recommendations
    if len(password) < 8:
        recommendations.append("📏 Increase password length to at least 12 characters")
    elif len(password) < 12:
        recommendations.append("📏 Consider using 12+ characters for better security")
    
    # Character type recommendations
    if not any(c.isupper() for c in password):
        recommendations.append("🔠 Add uppercase letters (A-Z)")
    
    if not any(c.islower() for c in password):
        recommendations.append("🔡 Add lowercase letters (a-z)")
    
    if not any(c.isdigit() for c in password):
        recommendations.append("🔢 Include numbers (0-9)")
    
    if not any(not c.isalnum() for c in password):
        recommendations.append("✨ Add special characters (!@#$%^&*)")
    
    # Entropy recommendations
    if entropy < 50:
        recommendations.append("🎲 Avoid repeated characters or patterns to increase randomness")
    
    # Common patterns
    common_patterns = ['123', 'abc', 'qwerty', 'password', 'admin']
    for pattern in common_patterns:
        if pattern in password.lower():
            recommendations.append(f"🚫 Avoid common patterns like '{pattern}'")
            break
    
    # Sequential characters
    if any(password[i] == chr(ord(password[i-1]) + 1) for i in range(1, len(password))):
        recommendations.append("📈 Avoid sequential characters (abc, 123, etc.)")
    
    # Repeated characters
    if len(set(password)) < len(password) * 0.5:
        recommendations.append("🔄 Reduce repeated characters for better security")
    
    # Dictionary words
    common_words = ['password', 'admin', 'user', 'login', 'welcome', 'master']
    for word in common_words:
        if word in password.lower():
            recommendations.append(f"📖 Avoid dictionary words like '{word}'")
            break
    
    # Score-based recommendations
    if score < 50:
        recommendations.append("🔒 Combine multiple improvements for a stronger password")
    elif score < 70:
        recommendations.append("💪 Good start! Add more variety to reach excellent security")
    
    # Add positive recommendations if password is already strong
    if not recommendations:
        recommendations.append("✅ Excellent! Your password is very strong")
        recommendations.append("🎉 Consider using a password manager for unique passwords")
    
    # Limit to top 5 recommendations
    return recommendations[:5]

def get_strength_feedback(checks):
    """
    Get detailed feedback based on check results
    """
    feedback = []
    
    if checks.get('length', False):
        feedback.append("✓ Good length")
    else:
        feedback.append("✗ Increase length to 12+ characters")
    
    if checks.get('uppercase', False):
        feedback.append("✓ Has uppercase")
    else:
        feedback.append("✗ Add uppercase letters")
    
    if checks.get('lowercase', False):
        feedback.append("✓ Has lowercase")
    else:
        feedback.append("✗ Add lowercase letters")
    
    if checks.get('digits', False):
        feedback.append("✓ Has numbers")
    else:
        feedback.append("✗ Add numbers")
    
    if checks.get('special', False):
        feedback.append("✓ Has special characters")
    else:
        feedback.append("✗ Add special characters")
    
    if checks.get('entropy', False):
        feedback.append("✓ Good randomness")
    else:
        feedback.append("✗ Improve randomness")
    
    return feedback