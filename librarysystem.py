from book import Book
import re
import random
from files import File

class LibrarySystem:
    def __init__(self):
        self.generated_ids = self.load_ids()
    def load_data(self):
        file = open('all_books.txt', 'r')
        content = file.readlines()
        file.close()
        return content
    def save_data(self, book):
        file = open('all_books.txt', 'a')
        file.write(str(book) + "\n")
        file.close()
    def find_number(self, text):
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        return None
    def load_ids(self):
        with open('ids.txt', 'r') as file:
            return set(line.strip() for line in file)
    def save_id(self, new_id):
        with open('ids.txt', 'a') as file:
            file.write(f"{new_id}\n")
    def generate_unique_id(self):
        while True:
            new_id = random.randint(100000,999999)
            if str(new_id) not in self.generated_ids:
                self.generated_ids.add(str(new_id))
                self.save_id(new_id)
                return new_id
    def extract_name(self, text):
        match = re.search(r'Name:\s*(\w+)', text)
        if match:
            return match.group(1)
        return None
    def add_book(self, book):
        book.id = self.generate_unique_id()
        content = self.load_data()
        for line in content:
            if book.name == self.extract_name(line):
                print("Wrong name")
                return

        self.save_data(book)
    def remove_book(self, id):
        content = self.load_data()
        updated_content = []
        for line in content:
            id_old = self.find_number(line)
            if id != id_old:
                updated_content.append(line.strip())
        file = open('all_books.txt', 'w')
        for line in updated_content:
            file.write(line + "\n")
        file.close()
        #Deleting from ids
        file = open('ids.txt', 'r')
        content_ids = file.readlines()
        file.close()
        updated_content_ids = []
        for line in content_ids:
            id_old = self.find_number(line)
            if id != id_old:
                updated_content_ids.append(line.strip())
        file = open('ids.txt', 'w')
        for line in updated_content_ids:
            file.write(line + "\n")
        file.close()

    def find_book(self, book_id):
        content = File.read_content("all_books.txt")
        for line in content:
            print(line)
            #Спросить надасуге поч функция не подходит для поиска
            #id = File.find(line, "ID: ")
            match = match = re.search(r'ID: \s*([^,]+)', line)
            if match:
                id = match.group(1).strip()
            #
            if id:
                if int(id) == book_id:
                    book_name = File.find_till(line, "Name:", ",")
                    book_author = File.find_till(line, "Author:", ",")
                    book_genre = File.find_till(line, "Genre:", ",")
                    book_year = File.find_till(line, "Year:", ",")
                    book_copies = File.find(line, "Copies:")
                    if isinstance(book_copies, list):
                        book_copies = book_copies[0]
                    book = Book(book_name, book_author, book_genre, book_year, int(book_copies))
                    book.id = book_id
                    return book

    def add_book_to_user(self, book, user):
        content = File.read_content(f"users/{user.login}.txt")
        new_line = ""
        for line in content:
            old_books = File.find(line, "B")
            if old_books:
                match = re.search(r'Books:\s*(.+)', line)
                is_empty = match is not None
                if is_empty:
                    new_line = line.strip() + f"{book.name}"
                else:
                    new_line = line.strip() + f", {book.name}"
        if new_line:
            File.rewrite_content(f"users/{user.login}.txt", new_line, 0)

    def find_book_pos(self, book_id):
        content = File.read_content("all_books.txt")
        count = 0
        for line in content:
            match = match = re.search(r'ID: \s*([^,]+)', line)
            if match:
                id = match.group(1).strip()
            if int(id) == book_id:
                return count
            count += 1

    def decrement_book_copies(self, book):
        book.copies = int(book.copies) - 1
        position = self.find_book_pos(book.id)
        File.rewrite_content(f"all_books.txt", str(book), position)

    def take_book(self, book_id, user):
        book = self.find_book(book_id)
        if book.copies == 0:
            print("Этой книги нет в наличии")
        else:
            print("Книга взята")
            self.add_book_to_user(book, user)
            self.decrement_book_copies(book)

