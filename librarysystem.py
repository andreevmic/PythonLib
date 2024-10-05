from book import Book
import re
import random

class LibrarySystem:
    def __init__(self):
        self.generated_ids = self.load_ids()
    def load_data(self):
        file = open('all_books.txt', 'r')
        content = file.readlines()
        file.close()
        return content
    def save_data(self, book):
        file = open('all_books.txt', 'a')
        file.write(str(book) + "\n")
        file.close()
    def find_number(self, text):
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        return None
    def load_ids(self):
        with open('ids.txt', 'r') as file:
            return set(line.strip() for line in file)
    def save_id(self, new_id):
        with open('ids.txt', 'a') as file:
            file.write(f"{new_id}\n")
    def generate_unique_id(self):
        while True:
            new_id = random.randint(100000,999999)
            if str(new_id) not in self.generated_ids:
                self.generated_ids.add(str(new_id))
                self.save_id(new_id)
                return new_id
    def add_book(self, book):
        book.id = self.generate_unique_id()

        self.save_data(book)
    def remove_book(self, id):
        content = self.load_data()
        updated_content = []
        for line in content:
            id_old = self.find_number(line)
            if id != id_old:
                updated_content.append(line)
        file = open('all_books.txt', 'w')
        for line in updated_content:
            file.write(line + "\n")
        file.close()
