import streamlit as st
from utils.logger import log_dashboard_access

def render_dashboard():
    # Log dashboard access (only once when page loads)
    if st.session_state.user_data:
        # Use session state to track if already logged
        if "dashboard_logged" not in st.session_state:
            log_dashboard_access(
                st.session_state.user_data.get("name", "Unknown"),
                st.session_state.user_data.get("email", "Unknown")
            )
            st.session_state.dashboard_logged = True
    
    st.title("✅ Welcome to Dashboard!")
    
    if st.session_state.user_data:
        st.success("🎉 Registration Successful!")
        
        st.markdown("---")
        
        st.subheader("📋 Your Details:")
        st.write(f"**👤 Name:** {st.session_state.user_data['name']}")
        st.write(f"**📧 Email:** {st.session_state.user_data['email']}")
        st.write(f"**📅 Registered On:** {st.session_state.user_data['registration_date']}")
        
        st.markdown("---")
    
    # Logout button
    if st.button("🚪 Logout"):
        # Clear dashboard log flag
        if "dashboard_logged" in st.session_state:
            del st.session_state.dashboard_logged
        
        st.session_state.page = "registration"
        st.session_state.user_data = None
        st.rerun()
