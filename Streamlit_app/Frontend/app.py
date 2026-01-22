import streamlit as st
from config import CUSTOM_CSS
from Pages.registration import render_registration  
from Pages.dashboard import render_dashboard
from utils.logger import log_app_startup, log_page_navigation

# Log application startup (BEFORE everything else)
log_app_startup()

st.set_page_config(page_title="Registration System ")

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize session state variables
if "user_data" not in st.session_state:
    st.session_state.user_data = None

if "page" not in st.session_state:
    st.session_state.page = "registration"

# Track previous page for logging
if "previous_page" not in st.session_state:
    st.session_state.previous_page = "registration"

# Log page navigation if page changed
if st.session_state.previous_page != st.session_state.page:
    log_page_navigation(st.session_state.previous_page, st.session_state.page)
    st.session_state.previous_page = st.session_state.page

# Route to correct page
if st.session_state.page == "registration":
    render_registration()
else:
    render_dashboard()
