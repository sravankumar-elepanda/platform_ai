import streamlit as st
from modules.auth import load_auth_config, get_authenticator

st.set_page_config("AI Asset Hub", layout="wide", page_icon="🤖")
config = load_auth_config('config/users.yaml')
authenticator = get_authenticator(config)
login_return = authenticator.login(location='main')
st.write("DEBUG: login_return =", login_return)
if not login_return:
    st.stop()
name, auth_status, username = login_return
st.write("Logged in!", auth_status, username)
