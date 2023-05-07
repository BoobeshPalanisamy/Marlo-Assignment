import json
import re


class User:
    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password

    def validate(self):
        if not self.first_name:
            return 'First name cannot be empty'
        if not self.last_name:
            return 'Last name cannot be empty'
        if not self.username:
            return 'Username cannot be empty'
        if not self.email:
            return 'Email cannot be empty'
        if not self.password:
            return 'Password cannot be empty'
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            return 'Email is invalid'
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', self.password):
            return 'Password must be at least 8 characters long and contain at least one letter and one number'
        return None

    def register(self):
        validation_error = self.validate()
        if validation_error:
            return validation_error

        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            users = []

        # Check if the email or username is already registered
        for user in users:
            if user['email'] == self.email:
                return 'Email is already registered'
            if user['username'] == self.username:
                return 'Username is already taken'

        # Add new user to the user list
        new_user = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
        users.append(new_user)

        # Save updated user data to JSON file
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)

        return 'User registered successfully'


# Get user input and create new User object
first_name = input("Enter first name: ")
last_name = input("Enter last name: ")
username = input("Enter username: ")
email = input("Enter email: ")
password = input("Enter password: ")

user = User(first_name, last_name, username, email, password)

# Register the new user and store data in JSON file
result = user.register()
print(result)
