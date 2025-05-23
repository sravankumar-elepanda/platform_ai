def get_role(config, username):
    return config['credentials']['usernames'].get(username, {}).get('role', 'Guest')

def is_admin(role):
    return role.lower() == 'admin'

def is_registered(role):
    return role.lower() in ['admin', 'registered', 'domain admin', 'approver', 'reviewer', 'asset owner']

def can_edit(role, owner, username):
    return is_admin(role) or (username == owner)

