import streamlit as st
from utils.validation import validate_name, validate_email, validate_password, validate_confirm_password
from datetime import datetime

def render_regristration():
    st.title("User Registration")
    
    # --- Full Name Field ---
    Username = st.text_input("Full Name", placeholder="Enter your full name")
    
    # Real-time validation (check as user types)
    if Username: 
        name_error = validate_name(Username)
        if name_error:
            st.error(f"❌ {name_error}")
        else:
            st.success("✅ Name looks good")
    
    # --- Email Field ---
    Email = st.text_input("Email", placeholder="Enter your email address")
    
    # Real-time validation
    if Email:
        email_error = validate_email(Email)
        if email_error:
            st.error(f"❌ {email_error}")
        else:
            st.success("✅ Email looks good")
    
    # --- Password Field ---
    Password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    # Real-time validation
    if Password:
        password_error = validate_password(Password)
        if password_error:
            st.error(f"❌ {password_error}")
        else:
            st.success("✅ Password is strong")
    
    # --- Confirm Password Field ---
    Confirm_Password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
    
    # Real-time validation
    if Confirm_Password:
        confirm_error = validate_confirm_password(Password, Confirm_Password)
        if confirm_error:
            st.error(f"❌ {confirm_error}")
        else:
            st.success("✅ Passwords match")
    
    # --- Terms and Conditions Checkbox ---
    terms = st.checkbox("I agree to the Terms and Conditions *")
    
    # --- Register Button ---
    if st.button("Register"):
        # Validate everything one more time
        name_error = validate_name(Username)
        email_error = validate_email(Email)
        password_error = validate_password(Password)
        confirm_error = validate_confirm_password(Password, Confirm_Password)
        
        # Check if all valid AND terms accepted
        if name_error:
            st.error(f"❌ {name_error}")
        elif email_error:
            st.error(f"❌ {email_error}")
        elif password_error:
            st.error(f"❌ {password_error}")
        elif confirm_error:
            st.error(f"❌ {confirm_error}")
        elif not terms:
            st.error("❌ Please accept Terms and Conditions")
        else:
            # Everything is valid! Save data and go to dashboard
            st.session_state.user_data = {
                "name": Username,
                "email": Email,
                "registration_date": datetime.now().strftime("%B %d, %Y at %I:%M %p")
            }
            
            # Navigate to dashboard
            st.session_state.page = "dashboard"
            
            # Rerun immediately (NO success message before this!)
            st.rerun()