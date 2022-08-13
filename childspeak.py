INPUT_FILE = "test.in"
first_lines = []

def read_input():
    with open(file=INPUT_FILE, encoding="utf-8") as input_file:
        first_lines = input_file.readlines()
        
read_input()