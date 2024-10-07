from files import File
import os

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

    def get_info(self):
        return (f"ID: {self.id}, "
                f"Login: {self.login}, "
                f"Password: {self.password}")
    
    def get_books_info(self):
        if not self.login:
            print("Ошибка: Логин не установлен")
            return []
        content = File.read_content(f"users/{self.login}.txt")
        return content
    
    def __str__(self):
        return self.get_info()

    def load_ids(self):
        content = File.read_content("users.txt")
        ids = []
        for line in content:
            id = File.find(line, "ID:")
            if id:
                ids.append(id)
        return ids

    def load_logins(self):
        content = File.read_content("users.txt")
        logins = []
        for line in content:
            login = File.find(line, "Login:")
            if login: 
                logins.append(login)
        return logins
    
    def load_passwords(self):
        content = File.read_content("users.txt")
        passwords = []
        for line in content:
            password = File.find(line, "Password:")
            if password:
                passwords.append(password)
        return passwords
    
    def load_rented_books(self):
        if not self.login:
            print("Ошибка: Логин не установлен")
            return []
        content = File.read_content(f"users/{self.login}.txt")
        books = []
        for line in content:
            book = File.find_all(line, "Books: ")
            if book:
                books.extend(book)
        return books
    
    def load_fines(self):
        content = File.read_content(f"users/{self.login}.txt")
        fines = []
        for line in content:
            fine = File.find_all(line, "Fines: ")
            if fine:
                fines.extend(fine)
        return fines

    def add_user(self, login, password):
        self.login = login
        self.password = password
        user = User(login, password)
        user.id = File.generate_unique_id(self.ids)
        File.write_content("users.txt", str(user))

    def check_is_adm(self):
        content = File.read_content("admins.txt")
        for line in content:
            if line == self.login:
                self.admin = True
                print(f"Здравствуй, {self.login}!")

    def log_in(self):
        login = input("Введите ваш логин: ")
        password = input("Введите пароль: ")
        if login in self.logins:
            if password in self.passwords:
                self.login = login
                print("Вы успешно зашли")
                self.check_is_adm()
            else:
                print("Неверный пароль")
        else:
            print("Неверный логин")


    def registration(self):
        login = input("Придумайте логин: ")
        if login in self.logins:
            print("Логин занят")
            self.login = ""
        else: 
            password = input("Придумайте пароль: ")
            self.add_user(login, password)
            with open(f"users/{login}.txt",'w') as file:
                file.write('Books: \nFines: ')