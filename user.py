from files import File
import os
import re
from librarysystem import LibrarySystem

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
        content = File.read_content(f"users/{self.login}_books.txt")
        return content
    
    @staticmethod
    def get_all_users_info():
        with open("users.txt", 'r') as file1:
            content = file1.readlines()
            for line in content:
                match = File.find(line, "Login: ")
                print(f"Login: {match}")
                with open(f"users/{match}_books.txt", 'r') as file2:
                    print("Rented books: ")
                    book_lines = file2.readlines()
                    if not book_lines:
                        print("Нет")
                    else:
                        for book_line in book_lines:
                            print(book_line.strip())
                with open(f"users/{match}_fines.txt", 'r') as file3:
                    print("Fines: ")
                    fine_lines = file3.readlines()
                    if not fine_lines:
                        print("Нет")
                    else:
                        for fine_line in fine_lines:
                            print(fine_line.strip())
            print("")
            
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
        content = File.read_content(f"users/{self.login}_books.txt")
        return content
    
    def load_fines(self):
        content = File.read_content(f"users/{self.login}_fines.txt")
        return content

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
            with open(f"users/{login}_books.txt",'w') as file:
                pass
            with open(f"users/{login}_fines.txt",'w') as file:
                pass

    @staticmethod
    def show_users():
        content = File.read_content("users.txt")
        for line in content:
            print(line)

    @staticmethod
    def find_user(user_id):
        content = File.read_content("users.txt")
        for line in content:
            #Спросить надасуге поч функция не подходит для поиска
            #id = File.find(line, "ID: ")
            match = match = re.search(r'ID: \s*([^,]+)', line)
            if match:
                id = match.group(1).strip()
            #
            if id:
                if int(id) == user_id:
                    user_login = File.find_till(line, "Login:", ",")
                    user_password = File.find(line, "Password:")
                    user = User(user_login, user_password)
                    user.id = user_id
                    return user

    def delete_user(user_id):
        user = User.find_user(user_id)
        File.delete_line("users.txt", str(user))
        os.remove(f"users/{user.login}_books.txt")
        os.remove(f"users/{user.login}_fines.txt")
