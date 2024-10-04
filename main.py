from book import Book
from librarysystem import LibrarySystem

my_book = Book(1, "Garry Potter", "Serega Pirat", "Prikoli", 2024)

#my_book.get_name()
#my_book.set_name("911")
#my_book.get_name()
print(my_book.get_info())

librarysystem = LibrarySystem()
#librarysystem.save_data(my_book)
librarysystem.load_data()