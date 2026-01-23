import streamlit as st
from utils.logger import log_dashboard_access
from utils.database import get_all_registrations, get_registration_count  # NEW IMPORT


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
    
    # NEW SECTION: Show all registrations from database
    st.markdown("---")
    st.header("📊 All Registrations (Database)")
    
    try:
        total_count = get_registration_count()
        st.metric("Total Registrations in Database", total_count)
        
        registrations = get_all_registrations()
        
        if registrations:
            for reg in registrations:
                with st.container():
                    col1, col2, col3 = st.columns([1, 2, 2])
                    col1.write(f"**#{reg[0]}**")
                    col2.write(f"**{reg[1]}**")
                    col3.write(f"{reg[2]}")
                    st.caption(f"📅 Registered: {reg[4]}")
                    st.divider()
        else:
            st.info("📭 No registrations in database yet!")
    except Exception as e:
        st.error(f"❌ Could not load registrations: {e}")
