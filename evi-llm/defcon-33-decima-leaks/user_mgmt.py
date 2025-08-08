USERS = {
    'admin': 'SuperSecretPassword123!',
    'jane.doe': 'Password!2024',
    'service_account': 'svc-decima-acc-001',
}

def authenticate(username, password):
    return USERS.get(username) == password

def list_users():
    return list(USERS.keys())

if __name__ == "__main__":
    print('Authenticate admin:', authenticate('admin', 'SuperSecretPassword123!'))
    print('All users:', list_users()) 