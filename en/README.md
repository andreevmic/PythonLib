# Interactive Library Management System

## Description

This project is an interactive library management system that allows users (librarians and readers) to perform essential operations: adding books, deleting them, registering readers, tracking borrowed books, managing returns, and handling fines. All data is stored in files, and users interact with the program through a console interface.

## System Functionality

### Book Registration
- Each book has a unique ID, title, author, genre, year of publication, and number of copies.
- Administrators can add books, remove them, or modify book information.

### Reader Registration
- Registration of new users with their name, phone number, email, and a unique ID.
- Storing the history of borrowed books and fines for late returns.

### Borrowing Books
- Users can borrow a book if it is available. The system keeps track of when the book was borrowed and when it should be returned.

### Returning Books
- Upon returning a book, the system checks the return date and applies fines if the book was returned late.

### Fines
- If a book is returned late, a fine is imposed, which the user must pay before borrowing another book.

### Database Search
- Ability to search for books by title, author, genre, and year of publication.
- Ability to view the history of borrowed books and outstanding debts for each user.

### Reports
- Generation of a report on the most popular books.
- Displaying a list of users with outstanding fines or unreturned books.

## Main Tasks

### File Handling
- Information about books, readers, and operations is stored in files (JSON, CSV, or text files).
- Each operation of adding, deleting, or modifying updates the corresponding file.

### Function Management
- All system operations (book registration, borrowing, searching, reports) are organized into functions to improve code structure.

### OOP (Object-Oriented Programming)
- Classes have been created for books, users, and the library management system:
  - **Book Class** with methods for adding and removing books.
  - **User Class** for registering and managing reader information.
  - **LibrarySystem Class**, which combines all functions and interacts with books and users.

### Exception Handling
- Possible errors are handled: invalid input data, attempts to borrow a book that is not available, errors in reading/writing files, etc.

### Menu (Input/Output)
- A console menu has been created through which users can interact with the program, offering choices: add a book, borrow a book, find a book, etc.

### Algorithms and Data Structures
- Lists are used to store books and readers during the program's execution.
- Dictionaries and sets help organize data on fines and book accounting.
