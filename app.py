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
name, auth_status, username = authenticator.login(location='main')
st.sidebar.markdown("---")

# Helper values
role = get_role(config, username) if auth_status else "Guest"
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

asset_types = ["Agents", "Scripts", "Workflows", "Platforms"]
selected_tab = st.sidebar.radio("Choose Asset Type", asset_types)
st.sidebar.markdown("---")

# ---- Main Page Tabs ----
st.header(f"{selected_tab} Catalog")

if st.button(f"➕ Register New {selected_tab[:-1]}", key="reg_btn", disabled=not (auth_status and registered)):
    st.session_state["register"] = True

def asset_form(asset_type, edit_data=None):
    st.header(f"{'Edit' if edit_data else 'Register New'} {asset_type[:-1]}")
    form = st.form(f"{asset_type}_form_{edit_data['Name'] if edit_data else 'new'}")
    name = form.text_input("Name", value=edit_data.get("Name") if edit_data else "")
    desc = form.text_area("Description", value=edit_data.get("Description") if edit_data else "")
    owner = form.text_input("Owner", value=edit_data.get("Owner") if edit_data else username)
    status = form.selectbox("Status", ["Published", "Draft", "Pending Approval"], index=0 if not edit_data else ["Published", "Draft", "Pending Approval"].index(edit_data.get("Status", "Published")))
    # Type-specific
    if asset_type == "Agents":
        domain = form.selectbox("Domain", ["Security", "Networking", "Storage", "CI/CD", "Custom"], index=0 if not edit_data else ["Security", "Networking", "Storage", "CI/CD", "Custom"].index(edit_data.get("Domain", "Security")))
        input_type = form.text_input("Input", value=edit_data.get("Input") if edit_data else "")
        output_type = form.text_input("Output", value=edit_data.get("Output") if edit_data else "")
        endpoint = form.text_input("API Endpoint", value=edit_data.get("Endpoint") if edit_data else "")
        link = form.text_input("GitHub/YAML Link", value=edit_data.get("Link") if edit_data else "")
    elif asset_type == "Scripts":
        lang = form.selectbox("Language", ["Python", "Bash", "Ansible", "Other"], index=0 if not edit_data else ["Python", "Bash", "Ansible", "Other"].index(edit_data.get("Language", "Python")))
        input_type = form.text_input("Input", value=edit_data.get("Input") if edit_data else "")
        output_type = form.text_input("Output", value=edit_data.get("Output") if edit_data else "")
        link = form.text_input("Script Link", value=edit_data.get("Link") if edit_data else "")
    elif asset_type == "Workflows":
        steps = form.text_area("Steps (comma separated)", value=edit_data.get("Steps") if edit_data else "")
        output_type = form.text_input("Output", value=edit_data.get("Output") if edit_data else "")
        link = form.text_input("GitHub/Definition Link", value=edit_data.get("Link") if edit_data else "")
    else:  # Platforms
        link = form.text_input("Platform URL", value=edit_data.get("Link") if edit_data else "")

    submitted = form.form_submit_button("Save" if edit_data else f"Register {asset_type[:-1]}")
    if submitted:
        # Validation: duplicate name in same asset type
        if not edit_data and any(x["Name"] == name for x in assets[asset_type]):
            st.warning("Asset with that name already exists!")
            return None
        a = {"Name": name, "Description": desc, "Status": status, "Owner": owner}
        if asset_type == "Agents":
            a.update({"Domain": domain, "Input": input_type, "Output": output_type, "Endpoint": endpoint, "Link": link})
        elif asset_type == "Scripts":
            a.update({"Language": lang, "Input": input_type, "Output": output_type, "Link": link})
        elif asset_type == "Workflows":
            a.update({"Steps": steps, "Output": output_type, "Link": link})
        else:
            a.update({"Link": link, "Owner": owner})
        if edit_data:
            idx = [i for i, x in enumerate(assets[asset_type]) if x["Name"] == edit_data["Name"]][0]
            assets[asset_type][idx] = a
        else:
            assets[asset_type].append(a)
        save_assets(assets, 'data/assets.json')
        st.success("Saved!")
        st.experimental_rerun()

if st.session_state.get("register"):
    asset_form(selected_tab)
    if st.button("Back", key="back_btn"):
        st.session_state["register"] = False
    st.stop()

# ---- List Assets ----
filtered_assets = assets[selected_tab]
for asset in filtered_assets:
    with st.container():
        display_asset_card(asset, selected_tab)
        if can_edit(role, asset.get("Owner", ""), username):
            st.markdown(f"<small>Owner: <b>{asset.get('Owner','')}</b></small>", unsafe_allow_html=True)
            if st.button("✏️ Edit", key=f"edit_{asset['Name']}"):
                st.session_state["register"] = False
                asset_form(selected_tab, asset)
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

