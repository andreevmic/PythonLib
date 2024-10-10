from book import Book
import re
import random
from files import File
from datetime import datetime, timedelta
from utilities import Utilities

class LibrarySystem:
    def __init__(self):
        self.generated_ids = File.read_content("ids.txt")
        self.books_array = self.load_all_books()

    def print_all_books(self):
        for book in self.books_array:
            print(str(book))

    def load_all_books(self):
        content = File.read_content("all_books.txt")
        books = []
        for line in content:
            book_id = File.find_till(line, "ID:", ",")
            book_name = File.find_till(line, "Name:", ",")
            book_author = File.find_till(line, "Author:", ",")
            book_genre = File.find_till(line, "Genre:", ",")
            book_year = File.find_till(line, "Year:", ",")
            book_copies = File.find(line, "Copies:")
            if isinstance(book_copies, list):
                book_copies = book_copies[0]
            book = Book(book_name, book_author, book_genre, book_year, int(book_copies))
            book.id = book_id
            books.append(book)
        return books

    def sort_books(self, sort_parameter, reverse = False):
        books = self.books_array
        sorted_books = sorted(books, key=lambda book: getattr(book, sort_parameter).strip().lower(), reverse=reverse)
        return sorted_books
    
    def get_sorted_books(self):
        sort_parameter = input("Введите параметр, которому хотите отсортировать(name, author): ")
        sorted_books = self.sort_books(sort_parameter)
        for book in sorted_books:
            print(str(book))

    def generate_unique_id(self):
        while True:
            new_id = random.randint(100000,999999)
            if str(new_id) not in self.generated_ids:
                self.generated_ids.append(str(new_id))
                File.write_content("ids.txt", str(new_id))
                return new_id
    
    def add_book(self):
        book = Book()
        book.name = input("Введите название книги: ")
        book.author = input("Введите имя автора: ")
        book.genre = input("Введите жанр книги: ")
        book.year = input("Введите год выхода книги: ")
        book.copies = input("Введите тираж книги: ")
        book.id = self.generate_unique_id()
        if book.name == File.find("all_books.txt", "Name: "):
            print("Книга с таким именем уже существует, вы уверены, что хотите добваить ещё одну?")
            choice = Utilities.get_user_choice("1. Да\n2. Нет\nВведите 1 или 2: ", 1, 2)
            if choice == 2:
                return
        File.write_content(str(book))
        self.books_array = self.load_all_books()

    def remove_book(self, id):
        book = LibrarySystem.find_book(id)
        File.delete_line("all_books.txt", str(book))
        File.delete_line("ids.txt", id)
        self.books_array = self.load_all_books()

    @staticmethod
    def find_book(book_id):
        content = File.read_content("all_books.txt")
        for line in content:
            id = File.find(line, "ID: ").strip()
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
        current_date = datetime.now()
        date_in_week = current_date + timedelta(weeks=1)
        date_to_return = Utilities.format_time(date_in_week)
        new_line = f"{book.id}" + f" {book.name}" + f" {date_to_return}"
        File.write_content(f"users/{user.login}_books.txt", new_line)

    def increment_book_copies(self, book):
        book.copies = int(book.copies) + 1
        position = self.find_book_pos(book.id)
        File.rewrite_content(f"all_books.txt", str(book), position)

    def give_fine(self, days, user):
        count = 50 * days
        File.write_content(f"users/{user.login}_fines.txt", str(count))

    def return_book(self, book, user):
        content = File.read_content(f"users/{user.login}_books.txt")
        date_to_return = None
        date_format = "%d-%m-%Y"
        current_date = datetime.now()
        for line in content:
            match = re.search(r'\d{2}-\d{2}-\d{4}', line)
            if match:
                date_to_return = match.group(0)
                formated_date_to_return = datetime.strptime(date_to_return, date_format)
                time_difference = formated_date_to_return - current_date
                if time_difference.days < 0:
                    self.give_fine(abs(time_difference.days), user)
                File.delete_line(f"users/{user.login}_books.txt", line)
                self.increment_book_copies(book)
                File.log(f"{user.login} вернул книгу {book.name}({book.id})")
                self.books_array = self.load_all_books()

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
            File.log(f"{user.login} взял книгу {book.name}({book.id})")
            File.write_content("report.txt", f"{book.id}")
            self.books_array = self.load_all_books()

    @staticmethod
    def get_report():
        content = File.read_content("report.txt")
        lines_count = {}
        for line in content:
            if line in lines_count:
                lines_count[line] += 1
            else:
                lines_count[line] = 1
        max_line = max(lines_count, key=lines_count.get)
        book = LibrarySystem.find_book(int(max_line))
        print(f"Самая популярная книга: {book.name}")