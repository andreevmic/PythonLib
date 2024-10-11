class Book:
    def __init__(self, name="Standart book name", author="Standart book author", 
                 genre="Standart book genre", year=2024, copies=0):
        """
        Инициализирует объект книги с заданными параметрами.

        :param name: Название книги.
        :param author: Автор книги.
        :param genre: Жанр книги.
        :param year: Год выпуска книги.
        :param copies: Количество экземпляров книги.
        """
        self.id = None  # Уникальный идентификатор книги (будет присвоен позже)
        self.name = name  # Название книги
        self.author = author  # Автор книги
        self.genre = genre  # Жанр книги
        self.year = year  # Год выпуска книги
        self.copies = copies  # Количество экземпляров книги

    def get_info(self):
        """
        Возвращает строку с информацией о книге.

        :return: Строка, содержащая информацию о книге.
        """
        return (f"ID: {self.id}, Name: {self.name}, "
                f"Author: {self.author}, Genre: {self.genre}, "
                f"Year: {self.year}, Copies: {self.copies}")

    def __str__(self):
        """
        Возвращает строковое представление объекта книги.
        
        :return: Строка с информацией о книге.
        """
        return self.get_info()  # Используем метод get_info для получения информации
