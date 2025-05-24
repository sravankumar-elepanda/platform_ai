import streamlit as st
from modules.auth import load_auth_config, get_authenticator
from modules.asset_io import load_assets, save_assets
from modules.permissions import get_role, is_admin, is_registered, can_edit
from modules.ui import display_asset_card
import os

# 1. Set page config as first Streamlit command
st.set_page_config("AI Asset Hub", layout="wide", page_icon="🤖")

LOGO_PATH = "static/cisco_logo.png"

# 2. Authenticator
config = load_auth_config('config/users.yaml')
authenticator = get_authenticator(config)
login_return = authenticator.login(location='main')
if not login_return:
    st.stop()
name, auth_status, username = login_return

# ---- DEBUG: Show login state ----
st.write(f"DEBUG: auth_status={auth_status}, username={username}, role={get_role(config, username)}")

if auth_status:
    role = get_role(config, username)
    admin = is_admin(role)
    registered = is_registered(role)

    # App top bar/logo
    col1, col2 = st.columns([0.13, 0.87])
    with col1:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=90)
    with col2:
        st.title("AI Asset Hub – Central Catalog for AI Platforms, Agents, Scripts & Workflows")
        st.markdown("Register, discover, and rate internal **Agents**, **Scripts**, **Workflows**, and **Platforms**.")

    assets = load_assets('data/assets.json')
    st.write("DEBUG: Assets loaded:", assets)

    asset_types = ["Agents", "Scripts", "Workflows", "Platforms"]
    selected_tab = st.sidebar.radio("Choose Asset Type", asset_types)
    st.sidebar.markdown("---")

    # ---- Main Page Tabs ----
    st.header(f"{selected_tab} Catalog")

    if st.button(f"➕ Register New {selected_tab[:-1]}", key="reg_btn", disabled=not (auth_status and registered)):
        st.session_state["register"] = True

    from modules.ui import asset_form  # Import here to avoid circular import

    if st.session_state.get("register"):
        asset_form(selected_tab, assets, save_assets, username)
        if st.button("Back", key="back_btn"):
            st.session_state["register"] = False
        st.stop()

    # ---- List Assets ----
    filtered_assets = assets.get(selected_tab, [])
    for asset in filtered_assets:
        with st.container():
            display_asset_card(asset, selected_tab)
            if can_edit(role, asset.get("Owner", ""), username):
                st.markdown(f"<small>Owner: <b>{asset.get('Owner','')}</b></small>", unsafe_allow_html=True)
                if st.button("✏️ Edit", key=f"edit_{asset['Name']}"):
                    st.session_state["register"] = False
                    asset_form(selected_tab, assets, save_assets, username, asset)
                    st.stop()
                if st.button("🗑️ Delete", key=f"del_{asset['Name']}"):
                    assets[selected_tab] = [x for x in assets[selected_tab] if x["Name"] != asset["Name"]]
                    save_assets(assets, 'data/assets.json')
                    st.experimental_rerun()

    # ---- Admin Panel ----
    if admin:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Admin Panel")
        st.sidebar.write("Add/remove users and assign roles (feature to be expanded).")

    st.markdown("<center><sub>AI Asset Hub © 2024 | Cisco Internal</sub></center>", unsafe_allow_html=True)
elif auth_status is False:
    st.error("Incorrect username or password.")
elif auth_status is None:
    st.warning("Please enter your username and password.")
