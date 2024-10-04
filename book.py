class Book:
    def __init__(self, name, author):
        self.name = name
        self.author = author
    def get_name(self):
        print(f"name is: {self.name}")
    def set_name(self, new_name):
        self.name = new_name