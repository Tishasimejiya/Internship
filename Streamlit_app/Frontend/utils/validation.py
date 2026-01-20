def validate_name(name):
    """Validate name - only letters and spaces allowed"""
    
    # Check if empty
    if not name or name.strip() == "":
        return "Name is required"
    
    # Check if name contains only letters and spaces
    if not all(char.isalpha() or char.isspace() for char in name):
        return "Name should contain only letters"
    
    # Check minimum length
    if len(name.strip()) < 2:
        return "Name must be at least 2 characters"
    
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
