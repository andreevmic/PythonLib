from files import File

class User:
    def __init__(self, login = "", password = ""):
        self.id = None
        self.login = login
        self.password = password
        self.ids = self.load_ids()
        self.logins = self.load_logins()
        self.passwords = self.load_passwords()

    def get_info(self):
        return (f"ID: {self.id}, "
                f"Login: {self.login}, "
                f"Password: {self.password}")
    
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
    
    def add_user(self, login, password):
        user = User(login, password)
        user.id = File.generate_unique_id(self.ids)
        File.write_content("users.txt", str(user))

    def log_in(self):
        login = input("Введите ваш логин: ")
        password = input("Введите пароль: ")
        if login in self.logins:
            if password in self.passwords:
                print("Вы успешно зашли")
            else : print("Неверный пароль")
        else : print("Неверный логин")

    def registration(self):
        login = input("Придумайте логин: ")
        if login in self.logins:
            print("Логин занят")
        else: 
            password = input("Придумайте пароль: ")
            self.add_user(login, password)