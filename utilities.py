class Utilities:
    @staticmethod
    def get_user_choice(input_text, range_start, range_end):
        while True:
            try:
                choice = int(input(input_text))
                if range_start <= choice <= range_end:
                    return choice
                else:
                    print("Неверный ввод, попробуйте снова.")
            except ValueError:
                print("Ошибка: необходимо ввести число.")

    @staticmethod
    def format_time(time):
        return time.strftime("%d-%m-%Y")