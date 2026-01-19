import streamlit as st
from config import CUSTOM_CSS
from Pages.regristration import render_regristration
from Pages.dashboard import render_dashboard

st.set_page_config(page_title="Registration System")

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize session state variables
if "user_data" not in st.session_state:
    st.session_state.user_data = None

if "page" not in st.session_state:
    st.session_state.page = "registration"

# Route to correct page
if st.session_state.page == "registration":
    render_regristration()
else:
    render_dashboard()

