import streamlit as st
from utils.validation import validate_name, validate_email, validate_password, validate_confirm_password
from datetime import date, datetime
import os
from utils.logger import (
    log_registration_attempt,
    log_validation_error,
    log_validation_success,
    log_successful_registration,
    log_registration_failure,
    log_terms_not_accepted
)
from utils.database import save_registration_to_db


def render_registration():
    st.title("User Registration V6 - With File Backup")

    # --- Full Name Field ---
    Username = st.text_input("Full Name", placeholder="Enter your full Name here")
    
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
    
    if Confirm_Password:
        confirm_error = validate_confirm_password(Password, Confirm_Password)
        if confirm_error:
            st.error(f"❌ {confirm_error}")
            log_validation_error("Confirm Password", confirm_error, "***HIDDEN***")
        else:
            st.success("✅ Passwords match")
            log_validation_success("Confirm Password")
    
    # --- FILE UPLOAD (NEW!) ---
    st.markdown("---")
    st.subheader("📎 Upload Document (Optional)")
    uploaded_file = st.file_uploader(
        "Choose a text file", 
        type=['txt'],
        help="Only .txt files allowed. Max size: 5MB"
    )
    
    if uploaded_file is not None:
        # Check file size (5MB max)
        if uploaded_file.size > 5 * 1024 * 1024:
            st.error("❌ File too large! Maximum 5MB allowed")
            uploaded_file = None
        else:
            st.success(f"✅ File selected: {uploaded_file.name} ({uploaded_file.size} bytes)")
    
    # --- Terms and Conditions Checkbox ---
    terms = st.checkbox("I agree to the Terms and Conditions *")
    
    # --- Register Button ---
    if st.button("Register"):
        log_registration_attempt(Username if Username else "EMPTY", Email if Email else "EMPTY")
        
        # Validate everything
        name_error = validate_name(Username)
        email_error = validate_email(Email)
        password_error = validate_password(Password)
        confirm_error = validate_confirm_password(Password, Confirm_Password)
        
        errors = []
        
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
        
        if errors:
            log_registration_failure(Email if Email else "UNKNOWN", errors)
        else:
            registration_date = date.today().strftime("%B %d, %Y")
            
            # Save uploaded file (NEW!)
            file_path = None
            if uploaded_file is not None:
                try:
                    # Create uploads directory
                    os.makedirs("/app/Frontend/uploads", exist_ok=True)
                    
                    # Generate unique filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    safe_username = Username.replace(' ', '_').replace('/', '_')
                    filename = f"{timestamp}_{safe_username}_{uploaded_file.name}"
                    file_path = f"/app/Frontend/uploads/{filename}"
                    
                    # Save file
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    st.success(f"✅ File uploaded: {filename}")
                except Exception as e:
                    st.error(f"❌ File upload failed: {e}")
                    file_path = None
            
            st.session_state.user_data = {
                "name": Username,
                "email": Email,
                "registration_date": registration_date,
                "file_path": file_path
            }
            
            log_successful_registration(Username, Email, registration_date)
            
            # Save to database (including file path)
            save_registration_to_db(Username, Email, registration_date, file_path)
            
            st.session_state.page = "dashboard"
            st.rerun()
