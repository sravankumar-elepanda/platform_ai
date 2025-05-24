import streamlit as st
from modules.auth import load_auth_config, get_authenticator

st.set_page_config("AI Asset Hub", layout="wide", page_icon="🤖")
config = load_auth_config('config/users.yaml')
authenticator = get_authenticator(config)

login_return = authenticator.login(location='main')

if login_return:
    name, auth_status, username = login_return
    if auth_status:
        st.success(f"Logged in as {username}!")
        # Continue to your app logic
    else:
        st.warning("Login failed. Please try again.")
else:
    # Don't show anything here except login (Streamlit Authenticator will render the login form)
    pass
