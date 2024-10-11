class Book:
    def __init__(self, title="Standard Book Title", author="Standard Book Author", 
                 genre="Standard Book Genre", year=2024, copies=0):
        """
        Initializes a book object with the given parameters.

        :param title: The title of the book.
        :param author: The author of the book.
        :param genre: The genre of the book.
        :param year: The year of publication.
        :param copies: The number of copies available.
        """
        self.id = None  # Unique identifier for the book (to be assigned later)
        self.title = title  # Title of the book
        self.author = author  # Author of the book
        self.genre = genre  # Genre of the book
        self.year = year  # Year of publication
        self.copies = copies  # Number of copies available

    def get_details(self):
        """
        Returns a string with the book's details.

        :return: A string containing the book's information.
        """
        return (f"ID: {self.id}, Title: {self.title}, "
                f"Author: {self.author}, Genre: {self.genre}, "
                f"Year: {self.year}, Copies: {self.copies}")

    def __str__(self):
        """
        Returns the string representation of the book object.
        
        :return: A string with the book's information.
        """
        return self.get_details()  # Use the get_details method to retrieve book info
