class File:
    @staticmethod
    def read_lines(filename):
        """
        Reads the contents of a file and returns them as a list of lines.
        
        :param filename: The name of the file to read.
        :return: A list of strings containing the file's contents.
        """
        content = []
        try:
            with open(filename, 'r') as file:
                content = file.readlines()  # Read all lines from the file
        except FileNotFoundError:
            print(f"File {filename} not found.")  # Handle error if the file is not found
        except Exception as e:
            print(f"Error reading file {filename}: {str(e)}")  # Handle other errors
        return content

    @staticmethod
    def append_line(filename, line):
        """
        Appends a line to a file.
        
        :param filename: The name of the file to write to.
        :param line: The line to write to the file.
        """
        with open(filename, 'a') as file:
            file.write(line + "\n")  # Write the line with a newline character

    @staticmethod
    def remove_line(filename, line):
        """
        Removes the specified line from the file.
        
        :param filename: The name of the file from which to remove the line.
        :param line: The line to be removed.
        """
        content = File.read_lines(filename)  # Read the contents of the file
        new_content = [old_line.strip() for old_line in content if old_line.strip() != line.strip()]  # Filter lines
        with open(filename, 'w') as file:
            for new_line in new_content:
                file.write(new_line + '\n')  # Write the remaining lines back to the file

    @staticmethod
    def update_line(filename, line, line_number):
        """
        Replaces the specified line in the file at the given line number.
        
        :param filename: The name of the file to update.
        :param line: The new line to replace with.
        :param line_number: The line number to replace (0-based).
        """
        content = File.read_lines(filename)  # Read the contents of the file
        with open(filename, 'w') as file:
            for count, content_line in enumerate(content):
                # Replace the line at the specified position
                if count != int(line_number):
                    file.write(content_line.strip() + '\n')  # Write old lines
                else:
                    file.write(line + '\n')  # Write the new line
