import streamlit as st
from login import login
from dashboard import dashboard


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title='Sales Intelligence Hub',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)


# ---------------- CUSTOM STYLING ---------------- #

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f7fa;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: #0f172a;
        margin-top: 20px;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #475569;
        font-size: 18px;
        margin-bottom: 30px;
    }

    div[data-testid="stSidebar"] {
        background-color: #111827;
    }

    div[data-testid="stSidebar"] * {
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- SESSION STATE ---------------- #

if 'Authenticated' not in st.session_state:

    st.session_state['Authenticated'] = False

if 'user_details' not in st.session_state:

    st.session_state['user_details'] = None


# ---------------- APPLICATION FLOW ---------------- #

if st.session_state['Authenticated']:

    dashboard()

else:

    st.markdown(
        """
        <div class="main-title">
            📊 Sales Intelligence Hub
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sub-title">
            Branch-Based Sales & Financial Tracking System
        </div>
        """,
        unsafe_allow_html=True
    )

    login()