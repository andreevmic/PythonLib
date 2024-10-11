import os
from files import File
from utilities import Utilities

class User:
    def __init__(self, login="", password=""):
        # Initialize user attributes
        self.id = None
        self.login = login
        self.password = password
        self.ids = self.load_ids()           # Load user IDs
        self.logins = self.load_logins()     # Load user logins
        self.passwords = self.load_passwords() # Load user passwords
        self.rented_books = None              # List of rented books
        self.fines = None                      # Fines
        self.admin = False                     # Is the user an admin

    def load_info(self):
        """Load user information from files."""
        self.ids = self.load_ids()
        self.logins = self.load_logins()
        self.passwords = self.load_passwords()
        self.id = self.load_id()
        self.rented_books = self.load_rented_books()
        self.fines = self.load_fines()

    def load_id(self):
        """Load user ID based on their login."""
        user_id = self.ids[self.logins.index(self.login)]
        return user_id

    def display_info(self):
        """Display user information."""
        print(self.get_info().strip())

    def get_info(self):
        """Retrieve user information as a string."""
        return (f"ID: {self.id}, "
                f"Login: {self.login}, "
                f"Password: {self.password}")

    def display_books_info(self, fines):
        """Display information about rented books and fines for the user."""
        print("Rented books:")
        if self.rented_books:
            for book in self.rented_books:
                print(book.strip())
        else:
            print("No rented books")
            if fines:
                print("Fines:")
                if self.fines:
                    for fine in self.fines:
                        print(fine.strip())
                else:
                    print("No fines")
            return False

        print("Fines:")
        if self.fines:
            for fine in self.fines:
                print(fine.strip())
        else:
            print("No fines")
        return True

    @staticmethod
    def display_all_users_info():
        """Display information about all users."""
        content = File.read_lines("users.txt")
        for line in content:
            match = Utilities.find_word(line, "Login: ")
            print(f"Login: {match}")
            print("Rented books:")
            book_lines = File.read_lines(f"users/{match}_books.txt")
            if not book_lines:
                print("No rented books")
            else:
                for book_line in book_lines:
                    print(book_line.strip())
            print("Fines:")
            fine_lines = File.read_lines(f"users/{match}_fines.txt")
            if not fine_lines:
                print("No fines")
            else:
                for fine_line in fine_lines:
                    print(fine_line.strip())
            print("")  # Empty line to separate users

    def __str__(self):
        """String representation of the user."""
        return self.get_info()

    def load_ids(self):
        """Load all user IDs from the file."""
        content = File.read_lines("user_ids.txt")
        ids = [line.strip() for line in content]
        return ids

    def load_logins(self):
        """Load all user logins from the file."""
        content = File.read_lines("users.txt")
        logins = []
        for line in content:
            login = Utilities.find_word(line, "Login:")
            if login: 
                logins.append(login)
        return logins

    def load_passwords(self):
        """Load all user passwords from the file."""
        content = File.read_lines("users.txt")
        passwords = []
        for line in content:
            password = Utilities.find_word(line, "Password:")
            if password:
                passwords.append(password)
        return passwords

    def load_rented_books(self):
        """Load the list of rented books for the user."""
        content = File.read_lines(f"users/{self.login}_books.txt")
        return content

    def load_fines(self):
        """Load the list of fines for the user."""
        content = File.read_lines(f"users/{self.login}_fines.txt")
        return content

    def add_user(self, login, password):
        """Add a new user."""
        self.login = login
        self.password = password
        user = User(login, password)
        user.id = Utilities.generate_unique_id(self.ids, "user_ids.txt")
        File.append_line("users.txt", str(user))

    def check_is_admin(self):
        """Check if the user is an admin."""
        content = File.read_lines("admins.txt")
        for line in content:
            if line == self.login:
                self.admin = True
                print(f"Hello, {self.login}!")

    def log_in(self):
        """User login."""
        while True:
            try:
                login = input("Enter your login (Cancel: 1): ")
                if login == "1":
                    return False
                if login in self.logins:
                    password = input("Enter password (Cancel: 1): ")
                    if password == "1":
                        return False
                    if password == self.passwords[self.logins.index(login)]:
                        self.login = login
                        self.password = password
                        print("You have successfully logged in")
                        self.check_is_admin()
                        self.load_info()
                        return True
                    else:
                        print("Incorrect password")
                else:
                    print("Incorrect login")
            except ValueError:
                print("Input error.")

    def register(self):
        """Register a new user."""
        while True:
            try:
                login = input("Create a login (Cancel: 1): ")
                if login == "1":
                    return False
                if login in self.logins:
                    print("Login is taken")
                elif len(login) < 4:
                    print("Choose a longer login (at least 4 characters)")
                else: 
                    password = input("Create a password (Cancel: 1): ")
                    if password == "1":
                        return False
                    if len(password) < 4:
                        print("Choose a longer password (at least 4 characters)")
                    self.add_user(login, password)
                    
                    # Create files for user's books and fines
                    with open(f"users/{login}_books.txt", 'w') as file:
                        pass
                    with open(f"users/{login}_fines.txt", 'w') as file:
                        pass
                    
                    print("You have successfully registered!")
                    self.load_info()
                    return True
            except ValueError:
                print("Input error.")

    def display_users(self):
        """Display information about other users."""
        content = File.read_lines("users.txt")
        if len(content) == 1:
            print("No other users found(")
            return False
        for line in content:
            if Utilities.find_text_until(line, "ID:", ",").strip() != str(self.id):
                print(line.strip())
        return True

    @staticmethod
    def find_user(user_id):
        """Find a user by their ID."""
        content = File.read_lines("users.txt")
        for line in content:
            user_id_str = Utilities.find_word(line, "ID: ").strip()
            if user_id_str:
                if int(user_id_str) == user_id:
                    user_login = Utilities.find_text_until(line, "Login:", ",")
                    user_password = Utilities.find_word(line, "Password:")
                    user = User(user_login, user_password)
                    user.id = user_id
                    return user

    @staticmethod
    def delete_user(user_id):
        """Delete a user by their ID."""
        user = User.find_user(user_id)
        File.remove_line("users.txt", str(user))
        File.remove_line("user_ids.txt", str(user.id))
        os.remove(f"users/{user.login}_books.txt")
        os.remove(f"users/{user.login}_fines.txt")
        print("User deleted!")
