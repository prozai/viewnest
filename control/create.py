class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.is_admin = True

# Create a user
user = User("user", "password")

# Create an admin
admin = Admin("admin", "password")