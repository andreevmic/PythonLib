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
