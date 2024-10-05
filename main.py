from book import Book
from librarysystem import LibrarySystem
from user import User

my_book = Book("Garry Potter", "Serega Pirat", "Prikoli", 2024)
my_user = User()

#my_book.get_name()
#my_book.set_name("911")
#my_book.get_name()
print(my_book.get_info())

librarysystem = LibrarySystem()
#librarysystem.save_data(my_book)
#librarysystem.load_data()
#librarysystem.add_book(my_book)
#librarysystem.remove_book(1)
def vxod():
    print("1. Вход")
    print("2. Регистрация")
    print("3. Выход")

    choice = int(input())
    if choice == 1:
        my_user.log_in()
    if choice == 2:
        my_user.registration()
    if choice == 3:
        return
    choose_function()

def choose_function():
    print("1. Вывести все книги")
    print("2. Добавить книгу")
    print("3. Удалить книгу")
    print("4. Выход")

    choice = int(input("Введите номер действия(1, 2, 3, 4): "))
    if choice == 1: 
        content = librarysystem.load_data()
        for line in content:
            print(line)
    if choice == 2:
        new_book = Book()
        new_book.name = input("Введите название книги: ")
        new_book.author = input("Введите имя автора: ")
        new_book.genre = input("Введите жанр книги: ")
        new_book.year = input("Введите год выхода книги: ")
        new_book.copies = input("Введите тираж книги: ")
        librarysystem.add_book(new_book)
    if choice == 3:
        content = librarysystem.load_data()
        for line in content:
            print(line)
        id_to_del = int(input("Выберите id книги, которую хотите удалить: "))
        librarysystem.remove_book(id_to_del)
    if choice == 4:
        print("Завершение работы")
        vxod()

vxod()