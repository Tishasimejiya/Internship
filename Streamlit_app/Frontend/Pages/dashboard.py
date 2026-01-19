import streamlit as st
from datetime import datetime


def render_dashboard():
    """Display user dashboard"""
    
    # Get user data from session state
    user_data = st.session_state.user_data
    
    # If no data, show error
    if not user_data:
        st.error("❌ No user data found. Please register first.")
        return
    
    # --- Header ---
    st.title("📊 User Dashboard")
    st.write("Welcome to your dashboard!")
    
    st.markdown("---")
    
    # --- User Information Section ---
    st.subheader("👤 User Information")
    
    # Display user details
    st.write(f"**Full Name:** {user_data['name']}")
    st.write(f"**Email:** {user_data['email']}")
    st.write(f"**Registration Date:** {user_data['registration_date']}")
    
    st.markdown("---")
    
    # --- Logout Button ---
    if st.button("🚪 Logout", type="primary"):
        # Clear user data
        st.session_state.user_data = None
        # Go back to registration page
        st.session_state.page = "registration"
        # Rerun to show registration page
        st.rerun()
