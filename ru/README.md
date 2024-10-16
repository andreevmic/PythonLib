# Интерактивная система управления библиотекой

## Описание

Данный проект представляет собой систему для управления библиотекой, которая позволяет пользователям (библиотекарям и читателям) выполнять основные операции: добавлять книги, удалять их, регистрировать читателей, отслеживать выданные книги, вести учёт возвратов и штрафов. Все данные хранятся в файлах, а пользователи взаимодействуют с программой через консольный интерфейс.

## Функционал системы

### Регистрация книг
- Каждая книга имеет уникальный ID, название, автора, жанр, год выпуска и количество копий.
- Администраторы могут добавлять книги, удалять их или изменять информацию о книгах.

### Регистрация читателей
- Регистрация новых пользователей с указанием имени, номера телефона, электронной почты и уникального ID.
- Хранение истории выданных книг и штрафов за просроченные возвраты.

### Выдача книг
- Пользователь может взять книгу, если она есть в наличии. Система хранит информацию о том, когда книга была выдана и когда должна быть возвращена.

### Возврат книг
- При возврате книги система проверяет дату возврата и начисляет штрафы, если книга была возвращена с опозданием.

### Штрафы
- Если книга возвращена с задержкой, то начисляется штраф, который пользователь должен оплатить перед получением другой книги.

### Поиск по базе данных
- Возможность искать книги по названию, автору, жанру и году выпуска.
- Возможность просматривать историю выданных книг и задолженностей по каждому пользователю.

### Отчёты
- Генерация отчёта о самых популярных книгах.
- Вывод списка пользователей, у которых есть штрафы или невозвращённые книги.

## Основные задачи

### Работа с файлами
- Для хранения информации о книгах, читателях и операциях используется файлы (JSON, CSV или текстовые файлы).
- Каждая операция добавления, удаления или изменения обновляет соответствующий файл.

### Работа с функциями
- Все операции системы (регистрация книг, выдача, поиск, отчёты) организованы в функции для улучшения структуры кода.

### ООП (Объектно-ориентированное программирование)
- Созданы классы для книг, пользователей и системы управления библиотекой:
  - **Класс Book** с методами для добавления и удаления книг.
  - **Класс User** для регистрации и управления информацией о читателе.
  - **Класс LibrarySystem**, который объединяет все функции и взаимодействует с книгами и пользователями.

### Работа с исключениями
- Обрабатываются возможные ошибки: недопустимый ввод данных, попытки взять книгу, если её нет в наличии, ошибки при чтении/записи файлов и т.д.

### Меню (ввод-вывод данных)
- Создано консольное меню, через которое пользователи могут взаимодействовать с программой, предлагающее выбор: добавить книгу, выдать книгу, найти книгу и т.д.

### Алгоритмы и структуры данных
- Используются списки для хранения книг и читателей во время выполнения программы.
- Словари и множества помогают организовать данные о штрафах и учёте книг.
