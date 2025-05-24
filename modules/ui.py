import streamlit as st

def display_asset_card(asset, asset_type):
    link_html = f'<a href="{asset.get("Link")}" target="_blank">🌐 More Info</a>' if asset.get("Link") else ''
    approval_html = ("<br><span style='color:#aaa'>Not Published (Approval Pending)</span>"
                     if asset.get('Status', 'Published') != "Published" else '')
    st.markdown(
        f"""
        <div style="border-radius:15px;border:1px solid #eee;padding:18px 16px;margin-bottom:14px;box-shadow:0 2px 6px #ddd;">
            <div style="display:flex;align-items:center;">
                <span style="font-size:2em;margin-right:16px;">{"🤖" if asset_type=="Agents" else ("📝" if asset_type=="Scripts" else "🔄" if asset_type=="Workflows" else "🧩")}</span>
                <div>
                    <b style="font-size:1.2em;">{asset['Name']}</b>
                    <div style="font-size:0.93em;color:#555;">{asset.get('Description','')}</div>
                    <span style="font-size:0.8em;color:#7A7;">👤 {asset.get('Owner','')}</span>
                </div>
            </div>
            <div style="margin:7px 0 0 40px;font-size:0.92em;">
                <span style="color:#888;">Input:</span> {asset.get('Input','-')} | <span style="color:#888;">Output:</span> {asset.get('Output','-')}
            </div>
            <div style="margin-left:40px;font-size:0.9em;color:#57a;">{asset.get('Domain','') or asset.get('Language','')}</div>
            {link_html}
            {approval_html}
        </div>
        """, unsafe_allow_html=True)

def asset_form(asset_type, assets, save_assets, username, edit_data=None):
    st.header(f"{'Edit' if edit_data else 'Register New'} {asset_type[:-1]}")
    form = st.form(f"{asset_type}_form_{edit_data['Name'] if edit_data else 'new'}")
    name = form.text_input("Name", value=edit_data.get("Name") if edit_data else "")
    desc = form.text_area("Description", value=edit_data.get("Description") if edit_data else "")
    owner = form.text_input("Owner", value=edit_data.get("Owner") if edit_data else username)
    status = form.selectbox("Status", ["Published", "Draft", "Pending Approval"], index=0 if not edit_data else ["Published", "Draft", "Pending Approval"].index(edit_data.get("Status", "Published")))
    # Type-specific fields
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
