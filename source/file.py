def open_file(file_path, option):
    try:
        file_return = open(file_path, option)
    except FileNotFoundError:
        print(f"FILE: ({file_path}) not found, creating new...")
        file_temp = open(file_path, "w")
        file_temp.close()
        file_return = open(file_path, option)
    return file_return


def clean_lines(data):
    big_list = []
    for item in data:
        if item != data[-1]:
            big_list.append(item[:-1])
        else:
            big_list.append(item)
    return big_list


class File:
    people_file_path = "documentation/people.txt"
    drinks_file_path = "documentation/drinks.txt"
    favourites_file_path = "documentation/favourites.txt"
    test_file_path = "tests/text.txt"
    file_list = [people_file_path, drinks_file_path, favourites_file_path, test_file_path]

    def __init__(self):
        pass

    def clean_file(self, file_list_choice):
        long_string = ""
        lines_list = self.read_file(file_list_choice, True)
        for line in lines_list:
            if line.strip() != "":
                long_string += line
        self.rewrite_file(long_string, file_list_choice)

    def get_people(self):
        self.clean_file(0)
        return clean_lines(self.read_file(0, True))

    def get_drinks(self):
        self.clean_file(1)
        return clean_lines(self.read_file(1, True))

    def get_favourites(self):
        self.clean_file(2)
        return clean_lines(self.read_file(2, True))

    def rewrite_file(self, data, file_list_choice):
        file_path = self.file_list[file_list_choice]
        file = open_file(file_path, "w")
        file.write(data)
        file.close()

    def append_file(self, data, file_list_choice):
        file_path = self.file_list[file_list_choice]
        file = open_file(file_path, "a")
        file.write(data)
        file.close()

    def read_file(self, file_list_choice, lines=False):
        file_path = self.file_list[file_list_choice]
        file = open_file(file_path, "r")
        if lines:
            return file.readlines()
        else:
            return file.read()
