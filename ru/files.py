class File:
    @staticmethod
    def read_content(filename):
        """
        Читает содержимое файла и возвращает его в виде списка строк.
        
        :param filename: Имя файла для чтения.
        :return: Список строк, содержащих содержимое файла.
        """
        content = []
        try:
            with open(filename, 'r') as file:
                content = file.readlines()  # Чтение всех строк файла
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")  # Обработка ошибки, если файл не найден
        except Exception as e:
            print(f"Ошибка чтения файла {filename}: {str(e)}")  # Обработка других ошибок
        return content

    @staticmethod
    def write_content(filename, line):
        """
        Записывает строку в файл, добавляя её в конец.
        
        :param filename: Имя файла для записи.
        :param line: Строка для записи в файл.
        """
        with open(filename, 'a') as file:
            file.write(line + "\n")  # Запись строки с переводом строки

    @staticmethod
    def delete_line(filename, line):
        """
        Удаляет указанную строку из файла.
        
        :param filename: Имя файла для удаления строки.
        :param line: Строка, которую необходимо удалить.
        """
        content = File.read_content(filename)  # Чтение содержимого файла
        new_content = [old_line.strip() for old_line in content if old_line.strip() != line.strip()]  # Фильтрация строк
        with open(filename, 'w') as file:
            for new_line in new_content:
                file.write(new_line + '\n')  # Запись оставшихся строк обратно в файл

    @staticmethod
    def rewrite_content(filename, line, num_of_line):
        """
        Перезаписывает указанную строку в файле по заданному номеру строки.
        
        :param filename: Имя файла для перезаписи.
        :param line: Новая строка для замены.
        :param num_of_line: Номер строки для замены (0 - основанное).
        """
        content = File.read_content(filename)  # Чтение содержимого файла
        with open(filename, 'w') as file:
            for count, content_line in enumerate(content):
                # Перезапись строки на указанной позиции
                if count != int(num_of_line):
                    file.write(content_line.strip() + '\n')  # Запись старых строк
                else:
                    file.write(line + '\n')  # Запись новой строки
