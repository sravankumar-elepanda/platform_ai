import yaml
import streamlit_authenticator as stauth

def load_auth_config(path):
    with open(path) as f:
        return yaml.safe_load(f)

def get_authenticator(config):
    return stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['cookie'].get('path', '/')
    )
