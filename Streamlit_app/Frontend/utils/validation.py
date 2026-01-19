def validate_name(name):
    """Check if name is valid"""
    if not name:
        return "Please enter your name"
    if not name.strip():
        return "Name cannot be empty spaces"
    
    # Check if name contains at least one letter
    has_letter = False
    for char in name:
        if char.isalpha(): 
            has_letter = True
            break
    
    if not has_letter:
        return "Name must contain at least one letter (not just numbers)"
    
    return None  


def validate_email(email):
    """Check if email is valid"""
    if not email:
        return "Please enter your email"
    if "@" not in email:
        return "Email must contain @"
    if "." not in email:
        return "Email must contain . (dot)"
    return None  # None means valid


def validate_password(password):
    """Check if password is strong"""
    if not password:
        return "Please enter a password"
    if len(password) < 8:
        return "Password must be at least 8 characters"
    return None  # None means valid


def validate_confirm_password(password, confirm):
    """Check if passwords match"""
    if not confirm:
        return "Please confirm your password"
    if password != confirm:
        return "Passwords do not match"
    return None  # None means valid
