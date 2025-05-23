import streamlit_authenticator as stauth
import yaml

def load_auth_config(users_file='config/users.yaml'):
    with open(users_file) as f:
        config = yaml.safe_load(f)
    return config

def get_authenticator(config):
    return stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['cookie'].get('path', '/')
    )

