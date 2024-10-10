import re
import random

class File:
    @staticmethod
    def read_content(filename):
        content = []
        with open(filename, 'r') as file:
            content = file.readlines()
        return content

    @staticmethod
    def write_content(filename, line):
        with open(filename, 'a') as file:
            file.write(line + "\n")

    @staticmethod
    def delete_line(filename, line):
        content = File.read_content(filename)
        new_content = []
        for old_line in content:
            if old_line.strip() != line.strip():
                new_content.append(old_line.strip())
        with open(filename, 'w') as file:
            for new_line in new_content:
                file.write(new_line + '\n')

    @staticmethod
    def log(line):
        with open("log.txt", 'a') as file:
            file.write(line + "\n")

    @staticmethod
    def get_log():
        with open("log.txt", 'r') as file:
            content = file.readlines()
            for line in content:
                print(line.strip())

    @staticmethod
    def rewrite_content(filename, line, num_of_line):
        content = File.read_content(filename)
        with open(filename, 'w') as file:
            pass
        count = 0
        for content_line in content:
            if count != int(num_of_line):
                File.write_content(filename, content_line.strip())
            else:
                File.write_content(filename, line)
            count += 1

    @staticmethod
    def find(line, substring):
        match = re.search(rf'{substring}\s*(\w+)', line)
        if match:
            return match.group(1)
        return None
    
    @staticmethod
    def find_till(line, substring, mark):
        escaped_mark = re.escape(mark)
        match = re.search(rf'{re.escape(substring)}\s*([^{escaped_mark}]+)', line)
        if match:
            return match.group(1).strip()
        return None
    
    @staticmethod
    def find_all(line, substring):
        matches = re.findall(rf'{substring}\s*(\w+)', line)
        if matches:
            return matches
        return None

    @staticmethod
    def generate_unique_id(generated_ids):
        while True:
            new_id = random.randint(100000,999999)
            if str(new_id) not in generated_ids:
                generated_ids.append(str(new_id))
                return new_id