import json

def login(email, password):
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        print('Error: File not found')
        return
    except json.decoder.JSONDecodeError:
        print('Error: Invalid JSON format')
        return

    for user in users:
        if user.get('email') == email and user.get('password') == password:
            return 'Login successful'

    return 'Invalid email or password'


email = input("Enter email: ")
password = input("Enter password: ")

result = login(email, password)

if result:
    print(result)
