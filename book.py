class Book:
    def __init__(self, name = "Standart book name", author = "Standart book author", 
                 genre = "Standart book genre", year = "Standart book year", copies = "Standart book number of copies"):
        self.id = None
        self.name = name
        self.author = author
        self.genre = genre
        self.year = year
        self.copies = copies
    #getr setr
    def get_id(self):
        return self.id
    def set_id(self, new_id):
        self.id = new_id
    def get_name(self):
        return self.name
    def set_name(self, new_name):
        self.name = new_name
    def get_author(self):
        return self.author
    def set_author(self, new_author):
        self.author = new_author
    def get_genre(self):
        return self.genre
    def set_genre(self, new_genre):
        self.genre = new_genre
    def get_year(self):
        return self.year
    def set_year(self, new_year):
        self.year = new_year
    def get_copies(self):
        return self.copies
    def set_copies(self, new_copies):
        self.copies = new_copies
    #info
    def get_info(self):
        return (f"ID: {self.get_id()}, Name: {self.get_name()}, "
                f"Author: {self.get_author()}, Genre: {self.get_genre()}, "
                f"Year: {self.get_year()}, Copies: {self.get_copies()}")
    def __str__(self):
        return self.get_info()