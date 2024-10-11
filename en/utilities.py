import re
import random
from files import File

class Utilities:
    @staticmethod
    def get_user_choice(prompt_text, range_start, range_end, exit_value=None):
        """
        Prompts the user for a choice until valid input is received.

        :param prompt_text: The prompt text for the user.
        :param range_start: The start of the valid range for the choice.
        :param range_end: The end of the valid range for the choice.
        :param exit_value: The value to exit the loop.
        :return: User's choice or False if the exit value is entered.
        """
        while True:
            try:
                choice = int(input(prompt_text))
                if choice == exit_value:
                    return False
                if range_start <= choice <= range_end:
                    return choice
                else:
                    print("Invalid input, please try again.")
            except ValueError:
                print("Error: You must enter a number.")

    @staticmethod
    def format_date(date):
        """
        Formats a datetime object into a string in 'dd-mm-yyyy' format.

        :param date: Date in datetime format.
        :return: Formatted date string.
        """
        return date.strftime("%d-%m-%Y")
    
    @staticmethod
    def extract_date(line, pattern):
        """
        Searches for a date in a string using a regular expression.

        :param line: The string to search in.
        :param pattern: The substring pattern to search for a date.
        :return: Found date or None if not found.
        """
        match = re.search(pattern, line)
        if match:
            return match.group(0)
        return None
    
    @staticmethod
    def find_word(line, substring):
        """
        Searches for a substring in a string and returns the first matched word.

        :param line: The string to search in.
        :param substring: The substring to search for.
        :return: Found word or None if not found.
        """
        match = re.search(rf'{substring}\s*(\w+)', line)
        if match:
            return match.group(1)
        return None
    
    @staticmethod
    def find_text_until(line, substring, marker):
        """
        Searches for text following a substring until a specified marker.

        :param line: The string to search in.
        :param substring: The substring from which to start searching.
        :param marker: The marker until which to search for text.
        :return: Found text or None if not found.
        """
        escaped_marker = re.escape(marker)
        match = re.search(rf'{re.escape(substring)}\s*([^{escaped_marker}]+)', line)
        if match:
            return match.group(1).strip()
        return None
    
    @staticmethod
    def find_all_words(line, substring):
        """
        Finds all matches of a substring in a string.

        :param line: The string to search in.
        :param substring: The substring to search for.
        :return: List of found matches or None if nothing is found.
        """
        matches = re.findall(rf'{substring}\s*(\w+)', line)
        if matches:
            return matches
        return None
    
    @staticmethod
    def generate_unique_id(existing_ids, filename=''):
        """
        Generates a unique ID that does not exist in the list of generated IDs.

        :param existing_ids: List of already generated IDs.
        :param filename: The name of the file to write the new ID.
        :return: New unique ID.
        """
        while True:
            new_id = random.randint(100000, 999999)
            if str(new_id) not in existing_ids:
                existing_ids.append(str(new_id))
                if filename:
                    File.append_line(filename, str(new_id))
                return new_id
        
    @staticmethod
    def log_message(message):
        """
        Writes a message to the log file.

        :param message: The message to log.
        """
        File.append_line("log.txt", message)

    @staticmethod
    def display_log():
        """
        Retrieves and displays the contents of the log file.
        If the log is empty, displays an appropriate message.
        """
        content = File.read_lines("log.txt")
        if not content:
            print("Log is currently empty.")
            return
        for line in content:
            print(line.strip())
