import os
from files import File
from utilities import Utilities

class User:
    def __init__(self, login = "", password = ""):
        self.id = None
        self.login = login
        self.password = password
        self.ids = self.load_ids()
        self.logins = self.load_logins()
        self.passwords = self.load_passwords()
        self.rented_books = None
        self.fines = None
        self.admin = False

    def load_info(self):
        self.rented_books = self.load_rented_books()
        self.fines = self.load_fines()
        self.ids = self.load_ids()
        self.logins = self.load_logins()
        self.passwords = self.load_passwords()

    def print_info(self):
        print(self.get_info().strip())

    def get_info(self):
        return (f"ID: {self.id}, "
                f"Login: {self.login}, "
                f"Password: {self.password}")
    
    def get_books_info(self):
        print("Взятые книги:")
        if self.rented_books:
            for book in self.rented_books:
                print(book.strip())
        else:
            print("Нет")
        print("Штрафы:")
        if self.fines:
            for fine in self.fines:
                print(fine.strip())
        else:
            print("Нет")
    
    @staticmethod
    def get_all_users_info():
        content = File.read_content("users.txt")
        for line in content:
            match = Utilities.find(line, "Login: ")
            print(f"Login: {match}")
            print("Rented books: ")
            book_lines = File.read_content(f"users/{match}_books.txt")
            if not book_lines:
                print("Нет")
            else:
                for book_line in book_lines:
                    print(book_line.strip())
            print("Fines: ")
            fine_lines = File.read_content(f"users/{match}_fines.txt")
            if not fine_lines:
                print("Нет")
            else:
                for fine_line in fine_lines:
                    print(fine_line.strip())
            print("")
            
    def __str__(self):
        return self.get_info()

    def load_ids(self):
        content = File.read_content("user_ids.txt")
        ids = []
        for line in content:
            id = Utilities.find(line, "ID:")
            if id:
                ids.append(id)
        return ids

    def load_logins(self):
        content = File.read_content("users.txt")
        logins = []
        for line in content:
            login = Utilities.find(line, "Login:")
            if login: 
                logins.append(login)
        return logins
    
    def load_passwords(self):
        content = File.read_content("users.txt")
        passwords = []
        for line in content:
            password = Utilities.find(line, "Password:")
            if password:
                passwords.append(password)
        return passwords
    
    def load_rented_books(self):
        content = File.read_content(f"users/{self.login}_books.txt")
        return content
    
    def load_fines(self):
        content = File.read_content(f"users/{self.login}_fines.txt")
        return content

    def add_user(self, login, password):
        self.login = login
        self.password = password
        user = User(login, password)
        user.id = Utilities.generate_unique_id(self.ids, "user_ids.txt")
        File.write_content("users.txt", str(user))

    def check_is_adm(self):
        content = File.read_content("admins.txt")
        for line in content:
            if line == self.login:
                self.admin = True
                print(f"Здравствуй, {self.login}!")

    def log_in(self):
        while True:
                try:
                    login = input("Введите ваш логин(Отмена: 1): ")
                    if login == "1":
                        return False
                    if login in self.logins:
                        password = input("Введите пароль(Отмена: 1): ")
                        if password == "1":
                            return False
                        if password == self.passwords[self.logins.index(login)]:
                            self.login = login
                            self.password = password
                            print("Вы успешно зашли")
                            self.check_is_adm()
                            self.load_info()
                            return True
                        else:
                            print("Неверный пароль")
                    else:
                        print("Неверный логин")
                except ValueError:
                    print("Ошибка ввода.")

    def registration(self):
        while True:
                try:
                    login = input("Придумайте логин(Отмена: 1): ")
                    if login == "1":
                        return False
                    if login in self.logins:
                        print("Логин занят")
                    if len(login) < 4:
                        print("Придумайте логин по длинее(от 4 знаков)1")
                    else: 
                        password = input("Придумайте пароль(Отмена: 1): ")
                        if password == "1":
                            return False
                        if len(password) < 4:
                            print("Придумайте пароль по длинее(от 4 знаков)1")
                        self.add_user(login, password)
                        with open(f"users/{login}_books.txt",'w') as file:
                            pass
                        with open(f"users/{login}_fines.txt",'w') as file:
                            pass
                        print("Вы успешно зарегестрировались!")
                        self.load_info()
                        return True
                except ValueError:
                    print("Ошибка ввода.")

    @staticmethod
    def show_users():
        content = File.read_content("users.txt")
        for line in content:
            print(line)

    @staticmethod
    def find_user(user_id):
        content = File.read_content("users.txt")
        for line in content:
            id = Utilities.find(line, "ID: ").strip()
            if id:
                if int(id) == user_id:
                    user_login = Utilities.find_till(line, "Login:", ",")
                    user_password = Utilities.find(line, "Password:")
                    user = User(user_login, user_password)
                    user.id = user_id
                    return user

    @staticmethod
    def delete_user(user_id):
        user = User.find_user(user_id)
        File.delete_line("users.txt", str(user))
        os.remove(f"users/{user.login}_books.txt")
        os.remove(f"users/{user.login}_fines.txt")
        print("Пользователь удалён!")
