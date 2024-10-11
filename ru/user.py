import os
from files import File
from utilities import Utilities

class User:
    def __init__(self, login="", password=""):
        # Инициализация атрибутов пользователя
        self.id = None
        self.login = login
        self.password = password
        self.ids = self.load_ids()           # Загрузка идентификаторов пользователей
        self.logins = self.load_logins()     # Загрузка логинов пользователей
        self.passwords = self.load_passwords() # Загрузка паролей пользователей
        self.rented_books = None              # Список взятых книг
        self.fines = None                      # Штрафы
        self.admin = False                     # Является ли пользователь администратором

    def load_info(self):
        """Загрузка информации о пользователе из файлов."""
        self.ids = self.load_ids()
        self.logins = self.load_logins()
        self.passwords = self.load_passwords()
        self.id = self.load_id()
        self.rented_books = self.load_rented_books()
        self.fines = self.load_fines()

    def load_id(self):
        """Загрузка ID пользователя по его логину."""
        id = self.ids[self.logins.index(self.login)]
        return id

    def print_info(self):
        """Вывод информации о пользователе."""
        print(self.get_info().strip())

    def get_info(self):
        """Получение информации о пользователе в виде строки."""
        return (f"ID: {self.id}, "
                f"Login: {self.login}, "
                f"Password: {self.password}")
    
    def get_books_info(self, fines):
        """Вывод информации о взятых книгах и штрафах пользователя."""
        print("Взятые книги:")
        if self.rented_books:
            for book in self.rented_books:
                print(book.strip())
        else:
            print("Нет взятых книг")
            if fines:
                print("Штрафы:")
                if self.fines:
                    for fine in self.fines:
                        print(fine.strip())
                else:
                    print("Нет штрафов")
            return False

        print("Штрафы:")
        if self.fines:
            for fine in self.fines:
                print(fine.strip())
        else:
            print("Нет штрафов")
        return True
    
    @staticmethod
    def get_all_users_info():
        """Вывод информации о всех пользователях."""
        content = File.read_content("users.txt")
        for line in content:
            match = Utilities.find(line, "Login: ")
            print(f"Login: {match}")
            print("Rented books: ")
            book_lines = File.read_content(f"users/{match}_books.txt")
            if not book_lines:
                print("Нет взятых книг")
            else:
                for book_line in book_lines:
                    print(book_line.strip())
            print("Fines: ")
            fine_lines = File.read_content(f"users/{match}_fines.txt")
            if not fine_lines:
                print("Нет штрафов")
            else:
                for fine_line in fine_lines:
                    print(fine_line.strip())
            print("")  # Пустая строка для разделения пользователей
            
    def __str__(self):
        """Строковое представление пользователя."""
        return self.get_info()

    def load_ids(self):
        """Загрузка всех ID пользователей из файла."""
        content = File.read_content("user_ids.txt")
        ids = [line.strip() for line in content]
        return ids

    def load_logins(self):
        """Загрузка всех логинов пользователей из файла."""
        content = File.read_content("users.txt")
        logins = []
        for line in content:
            login = Utilities.find(line, "Login:")
            if login: 
                logins.append(login)
        return logins
    
    def load_passwords(self):
        """Загрузка всех паролей пользователей из файла."""
        content = File.read_content("users.txt")
        passwords = []
        for line in content:
            password = Utilities.find(line, "Password:")
            if password:
                passwords.append(password)
        return passwords
    
    def load_rented_books(self):
        """Загрузка списка взятых книг пользователя."""
        content = File.read_content(f"users/{self.login}_books.txt")
        return content
    
    def load_fines(self):
        """Загрузка списка штрафов пользователя."""
        content = File.read_content(f"users/{self.login}_fines.txt")
        return content

    def add_user(self, login, password):
        """Добавление нового пользователя."""
        self.login = login
        self.password = password
        user = User(login, password)
        user.id = Utilities.generate_unique_id(self.ids, "user_ids.txt")
        File.write_content("users.txt", str(user))

    def check_is_adm(self):
        """Проверка, является ли пользователь администратором."""
        content = File.read_content("admins.txt")
        for line in content:
            if line == self.login:
                self.admin = True
                print(f"Здравствуй, {self.login}!")

    def log_in(self):
        """Логин пользователя."""
        while True:
            try:
                login = input("Введите ваш логин (Отмена: 1): ")
                if login == "1":
                    return False
                if login in self.logins:
                    password = input("Введите пароль (Отмена: 1): ")
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
        """Регистрация нового пользователя."""
        while True:
            try:
                login = input("Придумайте логин (Отмена: 1): ")
                if login == "1":
                    return False
                if login in self.logins:
                    print("Логин занят")
                elif len(login) < 4:
                    print("Придумайте логин по длинее (от 4 знаков)")
                else: 
                    password = input("Придумайте пароль (Отмена: 1): ")
                    if password == "1":
                        return False
                    if len(password) < 4:
                        print("Придумайте пароль по длинее (от 4 знаков)")
                    self.add_user(login, password)
                    
                    # Создание файлов для книг и штрафов пользователя
                    with open(f"users/{login}_books.txt", 'w') as file:
                        pass
                    with open(f"users/{login}_fines.txt", 'w') as file:
                        pass
                    
                    print("Вы успешно зарегестрировались!")
                    self.load_info()
                    return True
            except ValueError:
                print("Ошибка ввода.")

    def show_users(self):
        """Отображение информации о других пользователях."""
        content = File.read_content("users.txt")
        if len(content) == 1:
            print("Других пользователей нет(")
            return False
        for line in content:
            if Utilities.find_till(line, "ID:", ",").strip() != str(self.id):
                print(line.strip())
        return True

    @staticmethod
    def find_user(user_id):
        """Поиск пользователя по его ID."""
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
        """Удаление пользователя по его ID."""
        user = User.find_user(user_id)
        File.delete_line("users.txt", str(user))
        File.delete_line("user_ids.txt", str(user.id))
        os.remove(f"users/{user.login}_books.txt")
        os.remove(f"users/{user.login}_fines.txt")
        print("Пользователь удалён!")
