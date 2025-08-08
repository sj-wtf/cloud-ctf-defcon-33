import random

def get_user_info(user_id):
    fake_users = {
        1: {'name': 'John Smith', 'role': 'Lead Developer'},
        2: {'name': 'Jane Doe', 'role': 'Product Manager'},
        3: {'name': 'Alice Johnson', 'role': 'Security Analyst'},
    }
    return fake_users.get(user_id, {'error': 'User not found'})

def list_resources():
    return [
        'https://internal.decima-tech.com/dashboard',
        'https://ci.decima-tech.com/job/production-deploy',
        's3://decima-leaked-data-bucket/backups/2024-06-01/'
    ]

if __name__ == "__main__":
    print(get_user_info(random.choice([1,2,3,4])))
    print(list_resources()) 