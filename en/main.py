from librarysystem import LibrarySystem
from user import User
from utilities import Utilities

# Creating instances of User and LibrarySystem classes
current_user = User()
library_system = LibrarySystem()

def login_menu():
    """
    Function for user login and registration in the library system.
    """
    print("1. Login")
    print("2. Register")
    print("3. Exit")

    choice = Utilities.get_user_choice("Enter the action number: ", 1, 3)
    if choice == 1:
        if current_user.log_in():
            main_menu()
    elif choice == 2:
        if current_user.register():
            main_menu()
    elif choice == 3:
        exit()

    # Recursively call the function to show the menu again
    login_menu()

def main_menu():
    """
    Function to display the menu based on the user's role (admin or regular user).
    """
    if current_user.admin:
        # Admin menu
        print("1. Display all books")
        print("2. Add a book")
        print("3. Remove a book")
        print("4. Sort books")
        print("5. Borrow a book")
        print("6. Return a book")
        print("7. Most popular book")
        print("8. User information")
        print("9. Delete user")
        print("10. Display all users")
        print("11. Display user logs")
        print("12. Exit")

        choice = Utilities.get_user_choice("Enter the action number: ", 1, 12)

        # Handling admin choices
        if choice == 1:
            library_system.display_all_books()
        elif choice == 2:
            if library_system.add_new_book():
                print("Book added!")
        elif choice == 3:
            if library_system.display_all_books():
                id_to_remove = Utilities.get_user_choice("Select the ID of the book you want to remove (Cancel: 1): ", 100000, 999999, 1)
                if id_to_remove:
                    library_system.remove_book(id_to_remove)
        elif choice == 4:
            library_system.request_sorted_books()
        elif choice == 5:
            if library_system.display_all_books():
                id_to_borrow = Utilities.get_user_choice("Select the ID of the book you want to borrow (Cancel: 1): ", 100000, 999999, 1)
                if id_to_borrow:
                    library_system.borrow_book(id_to_borrow, current_user)
        elif choice == 6:
            if current_user.display_books_info(False):
                id_to_return = Utilities.get_user_choice("Select the ID of the book you want to return (Cancel: 1): ", 100000, 999999, 1)
                if id_to_return:
                    book_to_return = library_system.find_book(id_to_return)
                    library_system.return_book(book_to_return, current_user)
        elif choice == 7:
            library_system.generate_report()
        elif choice == 8:
            current_user.display_info()
            current_user.display_books_info(True)
        elif choice == 9:
            if not current_user.display_users():
                print(f"Your ID: {current_user.id}")
            id_to_remove = Utilities.get_user_choice("Select the ID of the user you want to delete (Cancel: 1): ", 100000, 999999, 1)
            if str(id_to_remove) == current_user.id:
                print("Are you sure you want to delete your account?")
                sure = Utilities.get_user_choice("1. Yes\n2. No\n3. Cancel\n: ", 1, 2, 3)
                if sure == 1:
                    User.delete_user(id_to_remove)
                    exit()
                elif sure == 2:
                    main_menu()
            if id_to_remove:
                User.delete_user(id_to_remove)
                current_user.load_info()
        elif choice == 10:
            User.display_all_users_info()
        elif choice == 11:
            Utilities.display_log()
        elif choice == 12:
            print("Exiting the program")
            login_menu()
    else:
        # Regular user menu
        print("1. Display all books")
        print("2. Sort books")
        print("3. User information")
        print("4. Borrow a book")
        print("5. Return a book")
        print("6. Most popular book")
        print("7. Exit")

        choice = Utilities.get_user_choice("Enter the action number: ", 1, 7)

        # Handling regular user choices
        if choice == 1:
            library_system.display_all_books()
        elif choice == 2:
            library_system.request_sorted_books()
        elif choice == 3:
            current_user.display_info()
            current_user.display_books_info(True)
        elif choice == 4:
            if library_system.display_all_books():
                id_to_borrow = Utilities.get_user_choice("Select the ID of the book you want to borrow (Cancel: 1): ", 100000, 999999, 1)
                if id_to_borrow:
                    library_system.borrow_book(id_to_borrow, current_user)
        elif choice == 5:
            if current_user.display_books_info(False):
                id_to_return = Utilities.get_user_choice("Select the ID of the book you want to return (Cancel: 1): ", 100000, 999999, 1)
                if id_to_return:
                    book_to_return = library_system.find_book(id_to_return)
                    library_system.return_book(book_to_return, current_user)
        elif choice == 6:
            library_system.generate_report()
        elif choice == 7:
            print("Exiting the program")
            login_menu()

    # Recursively call to display the menu again
    main_menu()

# Start the program
login_menu()

