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

