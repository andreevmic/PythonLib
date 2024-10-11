import re
import random
from files import File

class Utilities:
    @staticmethod
    def get_user_choice(input_text, range_start, range_end, end = None):
        while True:
            try:
                choice = int(input(input_text))
                if choice == end:
                    return False
                if range_start <= choice <= range_end:
                    return choice
                else:
                    print("Неверный ввод, попробуйте снова.")
            except ValueError:
                print("Ошибка: необходимо ввести число.")

    @staticmethod
    def format_time(time):
        return time.strftime("%d-%m-%Y")
    
    @staticmethod
    def date_find(line, substring):
        match = re.search(substring, line)
        if match:
            return match.group(0)
        else: 
            return None
    
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
    def generate_unique_id(generated_ids, filename = ''):
        while True:
            new_id = random.randint(100000,999999)
            if str(new_id) not in generated_ids:
                generated_ids.append(str(new_id))
                if filename: 
                    File.write_content(filename, str(new_id))
                return new_id
        
    @staticmethod
    def log(line):
        File.write_content("log.txt", line)

    @staticmethod
    def get_log():
        content = File.read_content("log.txt")
        for line in content:
            print(line.strip())