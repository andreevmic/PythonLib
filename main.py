from book import Book
from librarysystem import LibrarySystem
from user import User
from files import File
from utilities import Utilities

my_book = Book("Garry Potter", "Serega Pirat", "Prikoli", 2024)
my_user = User()

print(my_book.get_info())

librarysystem = LibrarySystem()
def vxod():
    print("1. Вход")
    print("2. Регистрация")
    print("3. Выход")

    choice = int(input())
    if choice == 1:
        my_user.log_in()
        choose_function()
    if choice == 2:
        my_user.registration()
        if my_user.login:  # Убедитесь, что логин задан
            my_user.load_info()
            choose_function()
        else:
            print("Ошибка: Логин не задан.")
            vxod()
    if choice == 3:
        exit()

def choose_function():
    if my_user.admin == True:
        print("1. Вывести все книги")
        print("2. Добавить книгу")
        print("3. Удалить книгу")
        print("4. Отсортировать книги")
        print("5. Взять книгу")
        print("6. Вернуть книгу")
        print("7. Самая популярная книга")
        print("8. Информация о пользователе")
        print("9. Удалить пользователя")
        print("10. Вывести информацию о пользователях")
        print("11. Вывести логи о пользователях")
        print("12. Выход")

        choice = Utilities.get_user_choice("Введите номер действия: ", 1, 12)
        if choice == 1: 
            librarysystem.print_all_books()
        if choice == 2:
            librarysystem.add_book()
        if choice == 3:
            librarysystem.print_all_books()
            id_to_del = Utilities.get_user_choice("Выберите id книги, которую хотите удалить: ", 100000, 999999)
            librarysystem.remove_book(id_to_del)
        if choice == 4:
            librarysystem.get_sorted_books()
        if choice == 5:
            librarysystem.print_all_books()
            id_to_take = Utilities.get_user_choice("Выберите id книги, которую хотите взять: ", 100000, 999999)
            librarysystem.take_book(id_to_take, my_user)
        if choice == 6:
            result = ''.join(my_user.get_books_info())
            print(result.strip())
            id_to_return = Utilities.get_user_choice("Выберите id книги, которую хотите вернуть: ", 100000, 999999)
            book_to_return = librarysystem.find_book(id_to_return)
            librarysystem.return_book(book_to_return, my_user)
        if choice == 7:
            LibrarySystem.get_report()
        if choice == 8:
            result = ''.join(my_user.get_books_info())
            print(result.strip())
        if choice == 9:
            User.show_users()
            id_to_del = Utilities.get_user_choice("Выберите id пользователя, которого хотите удалить: ", 100000, 999999)
            User.delete_user(id_to_del)
        if choice == 10:
            User.get_all_users_info()
        if choice == 11:
            File.get_log()
        if choice == 12:
            print("Завершение работы")
            vxod()
    else:
        print("1. Вывести все книги")
        print("2. Отсортировать книги")
        print("3. Информация о пользователе")
        print("4. Взять книгу")
        print("5. Вернуть книгу")
        print("6. Самая популярная книга")
        print("7. Выход")

        choice = Utilities.get_user_choice("Введите номер действия: ", 1, 7)
        if choice == 1: 
            librarysystem.print_all_books()
        if choice == 2:
            librarysystem.get_sorted_books()
        if choice == 3:
            result = ''.join(my_user.get_books_info())
            print(result.strip())
        if choice == 4:
            librarysystem.print_all_books()
            id_to_take = Utilities.get_user_choice("Выберите id книги, которую хотите взять: ", 100000, 999999)
            librarysystem.take_book(id_to_take, my_user)
        if choice == 5:
            result = ''.join(my_user.get_books_info())
            print(result.strip())
            id_to_return = Utilities.get_user_choice("Выберите id книги, которую хотите вернуть: ", 100000, 999999)
            book_to_return = librarysystem.find_book(id_to_return)
            librarysystem.return_book(book_to_return, my_user)
        if choice == 6:
            LibrarySystem.get_report()
        if choice == 7:
            print("Завершение работы")
            vxod()
    choose_function()

vxod()