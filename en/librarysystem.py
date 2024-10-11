from book import Book
from files import File
from datetime import datetime, timedelta
from utilities import Utilities
from collections import Counter

class LibrarySystem:
    def __init__(self):
        # Load previously generated book IDs and all books
        self.generated_ids = File.read_lines("book_ids.txt")
        self.books_dict = self.load_all_books()

    def display_all_books(self):
        """Displays all books in the library. If there are no books, shows a message."""
        if not self.books_dict:
            print("No books available!")
            return False
        for book in self.books_dict.values():
            print(str(book).strip())
        return True

    def load_all_books(self):
        """Loads all books from the 'all_books.txt' file into a dictionary."""
        content = File.read_lines("all_books.txt")
        books = {}
        for line in content:
            # Extract book details using utilities
            book_id = Utilities.find_text_until(line, "ID:", ",")
            book_name = Utilities.find_text_until(line, "Name:", ",")
            book_author = Utilities.find_text_until(line, "Author:", ",")
            book_genre = Utilities.find_text_until(line, "Genre:", ",")
            book_year = Utilities.find_text_until(line, "Year:", ",")
            book_copies = Utilities.find_word(line, "Copies:")
            if isinstance(book_copies, list):
                book_copies = book_copies[0]
            book = Book(book_name, book_author, book_genre, book_year, int(book_copies))
            book.id = book_id
            books[book_id] = book
        return books

    def sort_books(self, sort_key, reverse=False):
        """Sorts books by the specified key."""
        books = list(self.books_dict.values())
        sorted_books = sorted(books, key=lambda book: getattr(book, sort_key).strip().lower(), reverse=reverse)
        return sorted_books

    def request_sorted_books(self):
        """Gets user input for the sort key and displays sorted books."""
        if not self.books_dict:
            print("No books available!")
            return
        # List of valid sort keys
        valid_keys = ["id", "name", "author", "genre", "year", "copies"]
        sort_key = input("Enter the parameter to sort by (id, name, author, genre, year, copies, cancel: 1): ")
        if sort_key == "1" or sort_key not in valid_keys:
            return
        sorted_books = self.sort_books(sort_key)
        for book in sorted_books:
            print(str(book).strip())

    def add_new_book(self):
        """Adds a new book to the library."""
        book = Book()
        field_mapping = {
            "book title": "name",
            "author's name": "author",
            "book genre": "genre",
            "year of publication": "year",
            "number of copies": "copies"
        }
        for field, attr in field_mapping.items():
            input_value = input(f"Enter {field} (Cancel: 1): ")
            if input_value == "1":
                return False
            if attr == "copies":
                input_value = int(input_value)
            setattr(book, attr, input_value)
        
        existing_book = Utilities.find_word("all_books.txt", f"Name: {book.name}")
        if existing_book:
            print("A book with this name already exists.")
            choice = Utilities.get_user_choice("1. Add a new book with the same name\n2. Cancel\nEnter 1 or 2: ", 1, 2)
            if choice == 2:
                return False
        
        book.id = Utilities.generate_unique_id(self.generated_ids, "book_ids.txt")
        File.append_line("all_books.txt", str(book))
        self.books_dict = self.load_all_books()
        return True

    def remove_book(self, book_id):
        """Removes a book from the library by its ID."""
        book = self.find_book(book_id)
        File.remove_line("all_books.txt", str(book))
        File.remove_line("book_ids.txt", str(book_id))
        self.books_dict = self.load_all_books()
        print("Book removed!")

    def find_book(self, book_id):
        """Finds a book by its ID."""
        return self.books_dict.get(str(book_id), None)

    def lend_book_to_user(self, book, user):
        """Lends a book to a user with a return date."""
        current_date = datetime.now()
        return_date = current_date + timedelta(weeks=1)
        formatted_return_date = Utilities.format_date(return_date)
        new_line = f"{book.id} {book.name} {formatted_return_date}"
        content = File.read_lines(f"users/{user.login}_books.txt")
        
        for line in content:
            if line.strip() == new_line:
                print("You have already borrowed this book!")
                return False
        
        File.append_line(f"users/{user.login}_books.txt", new_line)
        return True

    def increase_book_copies(self, book_id):
        """Increases the number of copies of a book by 1."""
        if book_id in self.books_dict:
            book = self.books_dict[book_id]
            book.copies += 1
            File.update_line("all_books.txt", str(book), self.find_book_position(book_id))

    def apply_fine(self, days, user):
        """Applies a fine to the user for overdue book returns."""
        existing_fine = File.read_lines(f"users/{user.login}_fines.txt")
        if existing_fine:
            fine_amount = int(existing_fine[0]) + 50 * days
        else:
            fine_amount = 50 * days
        File.append_line(f"users/{user.login}_fines.txt", str(fine_amount))

    def return_book(self, book, user):
        """Allows the user to return a book and handles possible fines."""
        content = File.read_lines(f"users/{user.login}_books.txt")
        date_format = "%d-%m-%Y"
        current_date = datetime.now()
        book_found = False

        for line in content:
            parts = line.split()
            if not parts:
                continue
            id_from_line = parts[0]
            if id_from_line == str(book.id):
                return_date_str = Utilities.extract_date(line, r'\d{2}-\d{2}-\d{4}')
                formatted_return_date = datetime.strptime(return_date_str, date_format)
                time_difference = formatted_return_date - current_date
                if time_difference.days < 0:
                    self.apply_fine(abs(time_difference.days), user)
                File.remove_line(f"users/{user.login}_books.txt", line)
                self.increase_book_copies(book.id)
                Utilities.log_message(f"{user.login} returned book {book.name}({book.id})")
                book_found = True
                break
        if not book_found:
            print("Book not found in the list of borrowed books.")
        else:
            print("Book returned.")

    def find_book_position(self, book_id):
        """Finds the position of a book in the 'all_books.txt' file by its ID."""
        content = File.read_lines("all_books.txt")
        for count, line in enumerate(content):
            id_from_line = Utilities.find_word(line, "ID: ").strip()
            if id_from_line == str(book_id):
                return count
        return None

    def decrease_book_copies(self, book_id):
        """Decreases the number of copies of a book by 1."""
        if book_id in self.books_dict:
            book = self.books_dict[book_id]
            if book.copies > 0:
                book.copies -= 1
                position = self.find_book_position(book_id)
                print(f"Position for book with ID {book_id}: {position}")
                if position is not None:
                    File.update_line("all_books.txt", str(book), position)
                else:
                    print("Book position not found.")
        else:
            print("Book not found in the library.")

    def borrow_book(self, book_id, user):
        """Allows the user to borrow a book temporarily."""
        print("Contents of books_dict:", self.books_dict)
        if user.fines:
            print(f"Please settle your fine: {user.fines}")
            return
        try:
            book_id = int(book_id)
        except ValueError:
            print("Invalid book ID.")
            return
        book = self.find_book(book_id)
        if book is None:
            print("Book not found.")
            return
        if book.copies == 0:
            print("This book is not available.")
            return
        if self.lend_book_to_user(book, user):
            self.decrease_book_copies(book.id)
            Utilities.log_message(f"{user.login} borrowed book {book.name}({book.id})")
            File.append_line("report.txt", f"{book.id}")
            user.load_info()
            self.books_dict = self.load_all_books()
            print("Book borrowed.")

    def generate_report(self):
        """Generates a report on the most popular book based on borrowed books."""
        content = File.read_lines("report.txt")
        if not content:
            print("Report is empty!")
            return
        lines_count = Counter(content)
        most_common_line = lines_count.most_common(1)[0][0]
        book = self.find_book(int(most_common_line))
        print(f"The most popular book: {book.name}")
