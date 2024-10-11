from book import Book
from files import File
from datetime import datetime, timedelta
from utilities import Utilities

class LibrarySystem:
    def __init__(self):
        self.generated_ids = File.read_content("book_ids.txt")
        self.books_array = self.load_all_books()

    def print_all_books(self):
        if not self.books_array:
            print("Нет книг!")
            return False
        for book in self.books_array:
            print(str(book).strip())
        return True

    def load_all_books(self):
        content = File.read_content("all_books.txt")
        books = []
        for line in content:
            book_id = Utilities.find_till(line, "ID:", ",")
            book_name = Utilities.find_till(line, "Name:", ",")
            book_author = Utilities.find_till(line, "Author:", ",")
            book_genre = Utilities.find_till(line, "Genre:", ",")
            book_year = Utilities.find_till(line, "Year:", ",")
            book_copies = Utilities.find(line, "Copies:")
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
        if not self.books_array:
            print("Нет книг!")
            return
        parametr_list = ["id", "name", "author", "genre", "year", "copies"]
        sort_parameter = input("Введите параметр, которому хотите отсортировать(id, name, author, genre, year, copies, отмена: 1): ")
        if sort_parameter == "1" or sort_parameter not in parametr_list:
            return
        sorted_books = self.sort_books(sort_parameter)
        for book in sorted_books:
            print(str(book).strip())
    
    def add_book(self):
        book = Book()
        book.name = input("Введите название книги(Отмена: 1): ")
        if book.name == "1": return False
        book.author = input("Введите имя автора(Отмена: 1): ")
        if book.author == "1": return False
        book.genre = input("Введите жанр книги(Отмена: 1): ")
        if book.genre == "1": return False
        book.year = input("Введите год выхода книги(Отмена: 1): ")
        if book.year == "1": return False
        book.copies = input("Введите тираж книги(Отмена: 1): ")
        if book.copies == "1": return False
        book.id = Utilities.generate_unique_id(self.generated_ids, "book_ids.txt")
        if book.name == Utilities.find("all_books.txt", "Name: "):
            print("Книга с таким именем уже существует, вы уверены, что хотите добваить ещё одну?")
            choice = Utilities.get_user_choice("1. Да\n2. Нет\nВведите 1 или 2: ", 1, 2)
            if choice == 2:
                return False
        File.write_content("all_books.txt", str(book))
        self.books_array = self.load_all_books()
        return True

    def remove_book(self, id):
        book = LibrarySystem.find_book(id)
        File.delete_line("all_books.txt", str(book))
        File.delete_line("book_ids.txt", id)
        self.books_array = self.load_all_books()
        print("Книга удалена!")

    @staticmethod
    def find_book(book_id):
        content = File.read_content("all_books.txt")
        for line in content:
            id = Utilities.find(line, "ID: ").strip()
            if id:
                if int(id) == book_id:
                    book_name = Utilities.find_till(line, "Name:", ",")
                    book_author = Utilities.find_till(line, "Author:", ",")
                    book_genre = Utilities.find_till(line, "Genre:", ",")
                    book_year = Utilities.find_till(line, "Year:", ",")
                    book_copies = Utilities.find(line, "Copies:")
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
        content = File.read_content(f"users/{user.login}_books.txt")
        for line in content:
            if line.strip() == new_line:
                print("Вы уже брали эту книгу!")
                return False
        File.write_content(f"users/{user.login}_books.txt", new_line)
        return True

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
            date_to_return = Utilities.date_find(line, r'\d{2}-\d{2}-\d{4}')
            formated_date_to_return = datetime.strptime(date_to_return, date_format)
            time_difference = formated_date_to_return - current_date
            if time_difference.days < 0:
                self.give_fine(abs(time_difference.days), user)
            File.delete_line(f"users/{user.login}_books.txt", line)
            self.increment_book_copies(book)
            Utilities.log(f"{user.login} вернул книгу {book.name}({book.id})")
            self.books_array = self.load_all_books()
            print("Книга возвращена")

    def find_book_pos(self, book_id):
        content = File.read_content("all_books.txt")
        count = 0
        for line in content:
            id = Utilities.find(line, "ID: ").strip()
            if int(id) == book_id:
                return count
            count += 1

    def decrement_book_copies(self, book):
        book.copies = int(book.copies) - 1
        position = self.find_book_pos(book.id)
        File.rewrite_content(f"all_books.txt", str(book), position)

    def take_book(self, book_id, user):
        book = self.find_book(book_id)
        if user.fines:
            print(f"Погасите задолжность: {user.fines}")
        if book.copies == 0:
            print("Этой книги нет в наличии")
        else:
            if self.add_book_to_user(book, user):
                self.decrement_book_copies(book)
                Utilities.log(f"{user.login} взял книгу {book.name}({book.id})")
                File.write_content("report.txt", f"{book.id}")
                user.load_info()
                self.books_array = self.load_all_books()
                print("Книга взята")

    @staticmethod
    def get_report():
        content = File.read_content("report.txt")
        if not content:
            print("Такой нет!")
            return
        lines_count = {}
        for line in content:
            if line in lines_count:
                lines_count[line] += 1
            else:
                lines_count[line] = 1
        max_line = max(lines_count, key=lines_count.get)
        book = LibrarySystem.find_book(int(max_line))
        print(f"Самая популярная книга: {book.name}")