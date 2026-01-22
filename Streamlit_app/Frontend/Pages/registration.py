import streamlit as st
from utils.validation import validate_name, validate_email, validate_password, validate_confirm_password
from datetime import date, datetime
from utils.logger import (
    log_registration_attempt,
    log_validation_error,
    log_validation_success,
    log_successful_registration,
    log_registration_failure,
    log_terms_not_accepted
)

def render_registration():
    st.title("User Registration V4")

    # --- Full Name Field ---
    Username = st.text_input("Full Name", placeholder="Enter your full Name here")
    
    # Real-time validation (check as user types)
    if Username: 
        name_error = validate_name(Username)
        if name_error:
            st.error(f"❌ {name_error}")
            log_validation_error("Full Name", name_error, Username)
        else:
            st.success("✅ Name looks good")
            log_validation_success("Full Name")
    
    # --- Email Field ---
    Email = st.text_input("Email", placeholder="Enter your email address")

    # Real-time validation
    if Email:
        email_error = validate_email(Email)
        if email_error:
            st.error(f"❌ {email_error}")
            log_validation_error("Email", email_error, Email)
        else:
            st.success("✅ Email looks good")
            log_validation_success("Email")

    # --- Password Field ---
    Password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    # Real-time validation
    if Password:
        password_error = validate_password(Password)
        if password_error:
            st.error(f"❌ {password_error}")
            log_validation_error("Password", password_error, "***HIDDEN***")
        else:
            st.success("✅ Password is strong")
            log_validation_success("Password")
    
    # --- Confirm Password Field ---
    Confirm_Password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
    
    # Real-time validation
    if Confirm_Password:
        confirm_error = validate_confirm_password(Password, Confirm_Password)
        if confirm_error:
            st.error(f"❌ {confirm_error}")
            log_validation_error("Confirm Password", confirm_error, "***HIDDEN***")
        else:
            st.success("✅ Passwords match")
            log_validation_success("Confirm Password")
    
    # --- Terms and Conditions Checkbox ---
    terms = st.checkbox("I agree to the Terms and Conditions *")
    
    # --- Register Button ---
    if st.button("Register"):
        # Log registration attempt
        log_registration_attempt(Username if Username else "EMPTY", Email if Email else "EMPTY")
        
        # Validate everything one more time
        name_error = validate_name(Username)
        email_error = validate_email(Email)
        password_error = validate_password(Password)
        confirm_error = validate_confirm_password(Password, Confirm_Password)
        
        # Collect all errors
        errors = []
        
        # Check if all valid AND terms accepted
        if name_error:
            st.error(f"❌ {name_error}")
            errors.append(name_error)
            log_validation_error("Full Name (Final)", name_error, Username)
        
        if email_error:
            st.error(f"❌ {email_error}")
            errors.append(email_error)
            log_validation_error("Email (Final)", email_error, Email)
        
        if password_error:
            st.error(f"❌ {password_error}")
            errors.append(password_error)
            log_validation_error("Password (Final)", password_error, "***HIDDEN***")
        
        if confirm_error:
            st.error(f"❌ {confirm_error}")
            errors.append(confirm_error)
            log_validation_error("Confirm Password (Final)", confirm_error, "***HIDDEN***")
        
        if not terms:
            st.error("❌ Please accept Terms and Conditions")
            errors.append("Terms not accepted")
            log_terms_not_accepted(Email if Email else "UNKNOWN")
        
        # If there are errors, log failure
        if errors:
            log_registration_failure(Email if Email else "UNKNOWN", errors)
        else:
            # Everything is valid! Save data and go to dashboard
            registration_date = date.today().strftime("%B %d, %Y")
            
            st.session_state.user_data = {
                "name": Username,
                "email": Email,
                "registration_date": registration_date
            }
            
            # Log successful registration
            log_successful_registration(Username, Email, registration_date)
            
            # Navigate to dashboard
            st.session_state.page = "dashboard"
            
            # Rerun immediately
            st.rerun()
