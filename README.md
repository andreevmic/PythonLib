# Library Management System

## Description

This project is a Library Management System that allows users (librarians and readers) to perform essential operations such as adding books, deleting them, registering readers, tracking issued books, managing returns, and handling fines. All data is stored in files, and users interact with the program through a console interface.

This program was developed using neural network techniques to enhance its functionality. It can be used by anyone as a course project or for personal use.

## Features

### Book Registration
- Each book has a unique ID, title, author, genre, publication year, and number of copies.
- Administrators can add, remove, or update book information.

### Reader Registration
- Register new users with name, phone number, email, and unique ID.
- Store history of issued books and fines for overdue returns.

### Book Issuance
- Users can borrow books if they are available. The system tracks when the book was issued and when it is due for return.

### Book Return
- Upon returning a book, the system checks the return date and applies fines if the book is returned late.

### Fines
- If a book is returned late, a fine is applied, which the user must pay before borrowing another book.

### Database Search
- Search for books by title, author, genre, and publication year.
- View the history of issued books and outstanding debts for each user.

### Reports
- Generate reports on the most popular books.
- Display a list of users with fines or unreturned books.

## Main Tasks

### File Handling
- Information about books, readers, and operations is stored in files (JSON, CSV, or text files).
- Each operation of adding, deleting, or modifying updates the relevant file.

### Functionality
- All system operations (book registration, issuance, search, reports) are organized into functions to improve code structure.

### OOP (Object-Oriented Programming)
- Classes are created for books, users, and the library management system:
  - **Book Class** with methods for adding and removing books.
  - **User Class** for registering and managing reader information.
  - **LibrarySystem Class** that integrates all functions and interacts with books and users.

### Exception Handling
- Possible errors are handled: invalid input, attempts to borrow a book when it is not available, errors in reading/writing files, etc.

### Menu (Input/Output)
- A console menu is created through which users can interact with the program, offering options to add a book, issue a book, find a book, etc.

### Algorithms and Data Structures
- Lists are used to store books and readers during program execution.
- Dictionaries and sets help organize data on fines and book tracking.

## Usage
You can use this program for educational purposes or as a course project. Feel free to adapt and modify it according to your needs.

## Installation
1. Clone this repository.
2. Make sure you have Python installed.
3. Run the main script to start using the Library Management System.

## License
This project is licensed under the MIT License.
