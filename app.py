import streamlit as st
from modules.auth import load_auth_config, get_authenticator
import os

st.set_page_config("AI Asset Hub", layout="wide", page_icon="🤖")

# Show CWD and list files for debug
st.write("CWD:", os.getcwd())
st.write("FILES in CWD:", os.listdir())

try:
    config = load_auth_config('config/users.yaml')
    st.write("Loaded config:", config)
except Exception as e:
    st.error(f"Error loading config: {e}")

try:
    authenticator = get_authenticator(config)
    st.write("Authenticator created.")
except Exception as e:
    st.error(f"Error creating authenticator: {e}")

try:
    login_return = authenticator.login(location='main')
    st.write("login_return:", login_return)
except Exception as e:
    st.error(f"Error in login: {e}")

if 'login_return' in locals() and login_return:
    name, auth_status, username = login_return
    st.success(f"Logged in as {username}!")
    st.write("auth_status:", auth_status)
else:
    st.info("Please login.")
