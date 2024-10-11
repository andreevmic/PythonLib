from book import Book
from files import File
from datetime import datetime, timedelta
from utilities import Utilities
from collections import Counter

class LibrarySystem:
    def __init__(self):
        # Загружаем ранее сгенерированные ID книг и все книги
        self.generated_ids = File.read_content("book_ids.txt")
        self.books_array = self.load_all_books()

    def print_all_books(self):
        """Выводит все книги в библиотеке. Если книг нет, выводит сообщение."""
        if not self.books_array:
            print("Нет книг!")
            return False
        for book in self.books_array.values():
            print(str(book).strip())
        return True

    def load_all_books(self):
        """Загружает все книги из файла 'all_books.txt' в словарь."""
        content = File.read_content("all_books.txt")
        books = {}
        for line in content:
            # Извлечение деталей книги с помощью утилит
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
            books[book_id] = book
        return books

    def sort_books(self, sort_parameter, reverse=False):
        """Сортирует книги по указанному параметру."""
        books = list(self.books_array.values())
        sorted_books = sorted(books, key=lambda book: getattr(book, sort_parameter).strip().lower(), reverse=reverse)
        return sorted_books

    def get_sorted_books(self):
        """Получает ввод от пользователя для параметра сортировки и выводит отсортированные книги."""
        if not self.books_array:
            print("Нет книг!")
            return
        # Список допустимых параметров для сортировки
        param_list = ["id", "name", "author", "genre", "year", "copies"]
        sort_parameter = input("Введите параметр, по которому хотите отсортировать (id, name, author, genre, year, copies, отмена: 1): ")
        if sort_parameter == "1" or sort_parameter not in param_list:
            return
        sorted_books = self.sort_books(sort_parameter)
        for book in sorted_books:
            print(str(book).strip())

    def add_book(self):
        """Добавляет новую книгу в библиотеку."""
        book = Book()
        field_mapping = {
            "название книги": "name",
            "имя автора": "author",
            "жанр книги": "genre",
            "год выхода книги": "year",
            "тираж книги": "copies"
        }
        for field, attr in field_mapping.items():
            input_value = input(f"Введите {field} (Отмена: 1): ")
            if input_value == "1":
                return False
            if attr == "copies":
                input_value = int(input_value)
            setattr(book, attr, input_value)
        
        existing_book = Utilities.find("all_books.txt", f"Name: {book.name}")
        if existing_book:
            print("Книга с таким именем уже существует.")
            choice = Utilities.get_user_choice("1. Добавить новую книгу с тем же именем\n2. Отмена\nВведите 1 или 2: ", 1, 2)
            if choice == 2:
                return False
        
        book.id = Utilities.generate_unique_id(self.generated_ids, "book_ids.txt")
        File.write_content("all_books.txt", str(book))
        self.books_array = self.load_all_books()
        return True

    def remove_book(self, id):
        """Удаляет книгу из библиотеки по её ID."""
        book = self.find_book(id)
        File.delete_line("all_books.txt", str(book))
        File.delete_line("book_ids.txt", str(id))
        self.books_array = self.load_all_books()
        print("Книга удалена!")

    def find_book(self, book_id):
        """Находит книгу по её ID."""
        return self.books_array.get(str(book_id), None)

    def add_book_to_user(self, book, user):
        """Добавляет книгу пользователю с указанием даты возврата."""
        current_date = datetime.now()
        date_in_week = current_date + timedelta(weeks=1)
        date_to_return = Utilities.format_time(date_in_week)
        new_line = f"{book.id} {book.name} {date_to_return}"
        content = File.read_content(f"users/{user.login}_books.txt")
        
        for line in content:
            if line.strip() == new_line:
                print("Вы уже брали эту книгу!")
                return False
        
        File.write_content(f"users/{user.login}_books.txt", new_line)
        return True

    def increment_book_copies(self, book_id):
        """Увеличивает количество копий книги на 1."""
        if book_id in self.books_array:
            book = self.books_array[book_id]
            book.copies += 1
            File.rewrite_content(f"all_books.txt", str(book), self.find_book_pos(book_id))

    def give_fine(self, days, user):
        """Назначает штраф пользователю за просрочку возврата книги."""
        existing_fine = File.read_content(f"users/{user.login}_fines.txt")
        if existing_fine:
            fine_count = int(existing_fine[0]) + 50 * days
        else:
            fine_count = 50 * days
        File.write_content(f"users/{user.login}_fines.txt", str(fine_count))

    def return_book(self, book, user):
        """Возвращает книгу пользователем и обрабатывает возможные штрафы."""
        content = File.read_content(f"users/{user.login}_books.txt")
        date_format = "%d-%m-%Y"
        current_date = datetime.now()
        book_found = False

        for line in content:
            parts = line.split()
            if not parts:
                continue
            id_from_line = parts[0]
            if id_from_line == str(book.id):
                date_to_return = Utilities.date_find(line, r'\d{2}-\d{2}-\d{4}')
                formated_date_to_return = datetime.strptime(date_to_return, date_format)
                time_difference = formated_date_to_return - current_date
                if time_difference.days < 0:
                    self.give_fine(abs(time_difference.days), user)
                File.delete_line(f"users/{user.login}_books.txt", line)
                self.increment_book_copies(book.id)
                Utilities.log(f"{user.login} вернул книгу {book.name}({book.id})")
                book_found = True
                break
        if not book_found:
            print("Книга не найдена в списке взятых книг.")
        else:
            print("Книга возвращена")

    def find_book_pos(self, book_id):
        """Находит позицию книги в файле 'all_books.txt' по её ID."""
        content = File.read_content("all_books.txt")
        for count, line in enumerate(content):
            id = Utilities.find(line, "ID: ").strip()
            if id == str(book_id):
                return count
        return None

    def decrement_book_copies(self, book_id):
        """Уменьшает количество копий книги на 1."""
        if book_id in self.books_array:
            book = self.books_array[book_id]
            if book.copies > 0:
                book.copies -= 1
                position = self.find_book_pos(book_id)
                print(f"Позиция для книги с ID {book_id}: {position}")
                if position is not None:
                    File.rewrite_content(f"all_books.txt", str(book), position)
                else:
                    print("Позиция книги не найдена.")
        else:
            print("Книга не найдена в библиотеке.")

    def take_book(self, book_id, user):
        """Позволяет пользователю взять книгу на время."""
        print("Содержимое books_array:", self.books_array)
        if user.fines:
            print(f"Погасите задолженность: {user.fines}")
            return
        try:
            book_id = int(book_id)
        except ValueError:
            print("Некорректный ID книги.")
            return
        book = self.find_book(book_id)
        if book is None:
            print("Книга не найдена.")
            return
        if book.copies == 0:
            print("Этой книги нет в наличии.")
            return
        if self.add_book_to_user(book, user):
            self.decrement_book_copies(book.id)
            Utilities.log(f"{user.login} взял книгу {book.name}({book.id})")
            File.write_content("report.txt", f"{book.id}")
            user.load_info()
            self.books_array = self.load_all_books()
            print("Книга взята")

    def get_report(self):
        """Выводит отчет о самой популярной книге на основе взятых книг."""
        content = File.read_content("report.txt")
        if not content:
            print("Отчет пуст!")
            return
        lines_count = Counter(content)
        max_line = lines_count.most_common(1)[0][0]
        book = self.find_book(int(max_line))
        print(f"Самая популярная книга: {book.name}")
