import re
import random
from files import File

class Utilities:
    @staticmethod
    def get_user_choice(input_text, range_start, range_end, end=None):
        """
        Запрашивает у пользователя выбор, пока не будет получен корректный ввод.
        
        :param input_text: Текст запроса для пользователя.
        :param range_start: Начало допустимого диапазона выбора.
        :param range_end: Конец допустимого диапазона выбора.
        :param end: Значение для выхода из цикла.
        :return: Выбор пользователя или False, если введено значение end.
        """
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
        """
        Форматирует время в строку формата 'дд-мм-гггг'.
        
        :param time: Время в формате datetime.
        :return: Строка с отформатированной датой.
        """
        return time.strftime("%d-%m-%Y")
    
    @staticmethod
    def date_find(line, substring):
        """
        Ищет дату в строке с использованием регулярного выражения.
        
        :param line: Строка для поиска.
        :param substring: Подстрока для поиска даты.
        :return: Найденная дата или None, если не найдена.
        """
        match = re.search(substring, line)
        if match:
            return match.group(0)
        return None
    
    @staticmethod
    def find(line, substring):
        """
        Ищет подстроку в строке и возвращает первое найденное слово.
        
        :param line: Строка для поиска.
        :param substring: Подстрока для поиска.
        :return: Найденное слово или None, если не найдено.
        """
        match = re.search(rf'{substring}\s*(\w+)', line)
        if match:
            return match.group(1)
        return None
    
    @staticmethod
    def find_till(line, substring, mark):
        """
        Ищет текст после подстроки до заданного маркера.
        
        :param line: Строка для поиска.
        :param substring: Подстрока, от которой начинается поиск.
        :param mark: Маркер, до которого нужно искать текст.
        :return: Найденный текст или None, если не найдено.
        """
        escaped_mark = re.escape(mark)
        match = re.search(rf'{re.escape(substring)}\s*([^{escaped_mark}]+)', line)
        if match:
            return match.group(1).strip()
        return None
    
    @staticmethod
    def find_all(line, substring):
        """
        Находит все совпадения подстроки в строке.
        
        :param line: Строка для поиска.
        :param substring: Подстрока для поиска.
        :return: Список найденных совпадений или None, если ничего не найдено.
        """
        matches = re.findall(rf'{substring}\s*(\w+)', line)
        if matches:
            return matches
        return None
    
    @staticmethod
    def generate_unique_id(generated_ids, filename=''):
        """
        Генерирует уникальный ID, который не существует в списке сгенерированных ID.
        
        :param generated_ids: Список уже сгенерированных ID.
        :param filename: Имя файла для записи нового ID.
        :return: Новый уникальный ID.
        """
        while True:
            new_id = random.randint(100000, 999999)
            if str(new_id) not in generated_ids:
                generated_ids.append(str(new_id))
                if filename:
                    File.write_content(filename, str(new_id))
                return new_id
        
    @staticmethod
    def log(line):
        """
        Записывает строку в файл логов.
        
        :param line: Строка для записи в лог.
        """
        File.write_content("log.txt", line)

    @staticmethod
    def get_log():
        """
        Получает и выводит содержимое файла логов.
        Если лог пуст, выводит соответствующее сообщение.
        """
        content = File.read_content("log.txt")
        if not content:
            print("Пока пусто")
            return
        for line in content:
            print(line.strip())
