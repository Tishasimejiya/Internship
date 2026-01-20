import sys
import os

# Add Frontend folder to path
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, '../Frontend')
sys.path.insert(0, frontend_dir)

# Import validation functions
from utils.validation import validate_name, validate_email, validate_password, validate_confirm_password

print("\n" + "="*60)
print("RUNNING VALIDATION TESTS")
print("="*60)

# ================================================
# Test 1: validate_name()
# ================================================

def test_validate_name():
    """Test name validation"""
    print("\n--- Testing validate_name() ---")
    
    # Test 1.1: Valid name
    result = validate_name("Tisha Simejiya")
    if result is None:  # No error means valid
        print("✅ Test 1.1 PASSED: Valid name accepted")
    else:
        print(f"❌ Test 1.1 FAILED: {result}")
        exit(1)
    
    # Test 1.2: Empty name
    result = validate_name("")
    if result is not None:  # Should return error
        print("✅ Test 1.2 PASSED: Empty name rejected")
    else:
        print("❌ Test 1.2 FAILED: Should reject empty name")
        exit(1)
    
    # Test 1.3: Name with numbers
    result = validate_name("Tisha123")
    if result is not None:  # Should return error
        print("✅ Test 1.3 PASSED: Name with numbers rejected")
    else:
        print("❌ Test 1.3 FAILED: Should reject name with numbers")
        exit(1)

# ================================================
# Test 2: validate_email()
# ================================================

def test_validate_email():
    """Test email validation"""
    print("\n--- Testing validate_email() ---")
    
    # Test 2.1: Valid email
    result = validate_email("tisha@gmail.com")
    if result is None:
        print("✅ Test 2.1 PASSED: Valid email accepted")
    else:
        print(f"❌ Test 2.1 FAILED: {result}")
        exit(1)
    
    # Test 2.2: Another valid email
    result = validate_email("user@yahoo.in")
    if result is None:
        print("✅ Test 2.2 PASSED: Valid email accepted")
    else:
        print(f"❌ Test 2.2 FAILED: {result}")
        exit(1)
    
    # Test 2.3: Invalid email (no @)
    result = validate_email("notanemail.com")
    if result is not None:
        print("✅ Test 2.3 PASSED: Invalid email rejected")
    else:
        print("❌ Test 2.3 FAILED: Should reject email without @")
        exit(1)
    
    # Test 2.4: Empty email
    result = validate_email("")
    if result is not None:
        print("✅ Test 2.4 PASSED: Empty email rejected")
    else:
        print("❌ Test 2.4 FAILED: Should reject empty email")
        exit(1)

# ================================================
# Test 3: validate_password()
# ================================================

def test_validate_password():
    """Test password validation"""
    print("\n--- Testing validate_password() ---")
    
    # Test 3.1: Strong password
    result = validate_password("Strong@123")
    if result is None:
        print("✅ Test 3.1 PASSED: Strong password accepted")
    else:
        print(f"❌ Test 3.1 FAILED: {result}")
        exit(1)
    
    # Test 3.2: Weak password (too short)
    result = validate_password("weak")
    if result is not None:
        print("✅ Test 3.2 PASSED: Weak password rejected")
    else:
        print("❌ Test 3.2 FAILED: Should reject weak password")
        exit(1)
    
    # Test 3.3: Empty password
    result = validate_password("")
    if result is not None:
        print("✅ Test 3.3 PASSED: Empty password rejected")
    else:
        print("❌ Test 3.3 FAILED: Should reject empty password")
        exit(1)

# ================================================
# Test 4: validate_confirm_password()
# ================================================

def test_validate_confirm_password():
    """Test password confirmation"""
    print("\n--- Testing validate_confirm_password() ---")
    
    # Test 4.1: Matching passwords
    result = validate_confirm_password("Strong@123", "Strong@123")
    if result is None:
        print("✅ Test 4.1 PASSED: Matching passwords accepted")
    else:
        print(f"❌ Test 4.1 FAILED: {result}")
        exit(1)
    
    # Test 4.2: Non-matching passwords
    result = validate_confirm_password("Password1", "Password2")
    if result is not None:
        print("✅ Test 4.2 PASSED: Non-matching passwords rejected")
    else:
        print("❌ Test 4.2 FAILED: Should reject non-matching passwords")
        exit(1)

# ================================================
# Run all tests
# ================================================

if __name__ == "__main__":
    try:
        test_validate_name()
        test_validate_email()
        test_validate_password()
        test_validate_confirm_password()
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("="*60)
        print()
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        exit(1)