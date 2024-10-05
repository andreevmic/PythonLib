import re
import random

class File:
    @staticmethod
    def read_content(filename):
        with open(filename, 'r') as file:
            content = file.readlines()
        return content

    @staticmethod
    def write_content(filename, line):
        with open(filename, 'a') as file:
            file.write(line + "\n")

    @staticmethod
    def find(line, substring):
        match = re.search(rf'{substring}\s*(\w+)', line)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def generate_unique_id(generated_ids):
        while True:
            new_id = random.randint(100000,999999)
            if str(new_id) not in generated_ids:
                generated_ids.append(str(new_id))
                return new_id