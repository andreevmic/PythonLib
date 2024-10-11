from librarysystem import LibrarySystem
from user import User
from utilities import Utilities
import sys

my_user = User()

librarysystem = LibrarySystem()

def vxod():
    print("1. Вход")
    print("2. Регистрация")
    print("3. Выход")

    choice = Utilities.get_user_choice("Введите номер действия: ", 1, 3)
    if choice == 1:
        if my_user.log_in():
            choose_function()
    if choice == 2:
        if my_user.registration():
            choose_function()
    if choice == 3:
        exit()
    vxod()

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
            if librarysystem.add_book():
                print("Книга добавлена!")
        if choice == 3:
            if librarysystem.print_all_books():
                id_to_del = Utilities.get_user_choice("Выберите id книги, которую хотите удалить(Отмена: 1): ", 100000, 999999, 1)
                if id_to_del:
                    librarysystem.remove_book(id_to_del)
        if choice == 4:
            librarysystem.get_sorted_books()
        if choice == 5:
            if librarysystem.print_all_books():
                id_to_take = Utilities.get_user_choice("Выберите id книги, которую хотите взять(Отмена: 1): ", 100000, 999999, 1)
                if id_to_take:
                    librarysystem.take_book(id_to_take, my_user)
        if choice == 6:
            if my_user.get_books_info(False):
                id_to_return = Utilities.get_user_choice("Выберите id книги, которую хотите вернуть(Отмена: 1): ", 100000, 999999, 1)
                if id_to_return:
                    book_to_return = librarysystem.find_book(id_to_return)
                    librarysystem.return_book(book_to_return, my_user)
        if choice == 7:
            LibrarySystem.get_report()
        if choice == 8:
            my_user.print_info()
            my_user.get_books_info(True)
        if choice == 9:
            if my_user.show_users():
                id_to_del = Utilities.get_user_choice("Выберите id пользователя, которого хотите удалить(Отмена: 1): ", 100000, 999999, 1)
                if str(id_to_del) == my_user.id:
                    print("Вы точно хотите удалить свой аккаунт?")
                    sure = Utilities.get_user_choice("1. Да\n2. Нет\n3. Отмена\n: ", 1, 2, 3)
                    if sure == 1:
                        User.delete_user(id_to_del)
                        exit()
                    if sure == 2:
                        choose_function()
                if id_to_del:
                    User.delete_user(id_to_del)
                    my_user.load_info()
        if choice == 10:
            User.get_all_users_info()
        if choice == 11:
            Utilities.get_log()
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
            my_user.print_info()
            my_user.get_books_info(True)
        if choice == 4:
            if librarysystem.print_all_books():
                id_to_take = Utilities.get_user_choice("Выберите id книги, которую хотите взять(Отмена: 1): ", 100000, 999999, 1)
                if id_to_take:
                    librarysystem.take_book(id_to_take, my_user)
        if choice == 5:
            if my_user.get_books_info(False):
                id_to_return = Utilities.get_user_choice("Выберите id книги, которую хотите вернуть(Отмена: 1): ", 100000, 999999, 1)
                if id_to_return:
                    book_to_return = librarysystem.find_book(id_to_return)
                    librarysystem.return_book(book_to_return, my_user)
        if choice == 6:
            LibrarySystem.get_report()
        if choice == 7:
            print("Завершение работы")
            vxod()
    choose_function()

vxod()