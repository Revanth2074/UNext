def write_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)

def read_file(filename):
    with open(filename, "r") as file:
        return file.read()

def search_file(filename, word):
    with open(filename, "r") as file:
        return word in file.read()