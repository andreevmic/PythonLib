from book import Book

class LibrarySystem:
    def __init__(self):
        self.books = []
    def load_data(self):
        file = open('all_books.txt', 'r')
        content = file.readlines()
        for line in content:
                print(line.strip())
        file.close()
    def save_data(self, book):
        file = open('all_books.txt', 'a')
        file.write(str(book) + "\n")
        file.close()