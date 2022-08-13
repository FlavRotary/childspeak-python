# /**
#  * @Author: Flavian Rotaru 
#  * @Date: 2022-08-13 13:02:14 
#  * @Last Modified by:   Flavian Rotaru 
#  * @Last Modified time: 2022-08-13 18:02:14 
#  */

import string
from typing import List
from collections import OrderedDict
from xmlrpc.client import boolean
import copy

#Global Variables
INPUT_FILE = "test.in"
OUTPUT_FILE = "test.out"
TEST_FILE = "example_big.in"
OUTPUT_TEST_FILE = "output_big.out"
TEST_OUTPUT_FILE = "example_big.out"
ALPHABET = list(string.ascii_lowercase)
VOWELS = ['a', 'e', 'i', 'o', 'u', 'y']
CONSONANTS = [letter for letter in ALPHABET if letter not in VOWELS]
DEBUG = False                # Set to false to use INPUT FILE and OUTPUT FILE


# Function which reads from input file and returns a sorted list wuithout duplicates
# with all the words inside input file
def read_input() -> list:
    global INPUT_FILE
    if DEBUG:
        INPUT_FILE = TEST_FILE
    with open(file=INPUT_FILE, encoding="utf-8") as input_file:
        return sorted(set(input_file.read().splitlines()))
    
#Function which prints from a given list of tuples to the output file.
def write_output(list_of_occurences: list) -> bool:
    global OUTPUT_FILE
    if DEBUG:
        OUTPUT_FILE = OUTPUT_TEST_FILE
    with open(file=OUTPUT_FILE, mode='w+', encoding="utf-8") as output_file:
        output_file.write("\n".join('{} {}'.format(pair[0], pair[1]) for pair in list_of_occurences))
    return True

#Function which verifies if all chars in string are vowels.
def all_vowels(input_string: str) -> boolean:
    if not any((letter in input_string) for letter in CONSONANTS):
        return True
    
# She uses exactly one unique consonant in the word -- once she comes to the first consonants,
# she replaces all the subsequent consonants with the first one.
# Example: instead of "mapa", she says "mama".
def rule1(input_string: str) -> str:
    if all_vowels(input_string):
        return input_string
    consonant_to_use = ''
    for letter in input_string:
        if letter in CONSONANTS:
            consonant_to_use = letter
            break
    return input_string.translate(str.maketrans(
        ''.join(CONSONANTS), 
        consonant_to_use.replace(
            consonant_to_use, consonant_to_use * len(CONSONANTS),1)))

# print(rule1('mapa'))

# If the word starts with a vowel, she puts the first consonant to the very beginning. 
# So instead of "alibaba" she says "lalilala"
def rule2(input_string: str) -> str:
    if all_vowels(input_string):
        return input_string
    if input_string[0] not in VOWELS:
        return input_string
    for letter in input_string:
        if letter in CONSONANTS:
            consonant_to_use = letter
            break
    return consonant_to_use + input_string
    
# print(rule2('alibaba'))

# If there is a group of consecutive consonants, she replaces the whole group 
# with just a single consonant.
# Example: instead of "lampa", she says "lala"
#          instead of "bratislava", she says "babibaba"
def rule3(input_string: str) -> str:
    if all_vowels(input_string):
        return input_string
    current = 1
    while current < len(input_string):
        if input_string[current] in CONSONANTS and input_string[current-1] in CONSONANTS:
            input_string = input_string[:current] + input_string[current+1:]
        current += 1
    return input_string

# print(rule3('mississippi'))

#If there is a group of consecutive vowels, 
# she replaces the whole group with the last vowel from the group. 
# Example: instead of "naomi", she says "noni"
#           instead of "aikido", she says "kikido"
def rule4(input_string: str) -> str:
    reversed = input_string[::-1]
    current = 1
    while current < len(reversed):
        if reversed[current] in VOWELS and reversed[current-1] in VOWELS:
            reversed = reversed[:current] + reversed[current+1:]
        current += 1
    return reversed[::-1]

# print(rule4('aikido'))

# She ignores all the consonants after the last vowel.
# Example: instead of "ahoj", she says "haho"
def rule5(input_string: str) -> str:
    if all_vowels(input_string):
        return input_string
    reversed = input_string[::-1]
    for index, letter in enumerate(reversed):
        if letter in VOWELS:
            reversed = reversed[index:]
            break
    return reversed[::-1]

# print(rule5('aardvark'))

# Fuction which applies all defined rules to an input_string and return the result.
# All rules are applied in the same order as they are defined in the rules list.
def map_word(input_string: str) -> str:
    rules = [rule1,rule2,rule3,rule4,rule5]
    current_copy = copy.deepcopy(input_string)
    inital_copy = ''
    while current_copy != inital_copy:
        inital_copy = copy.deepcopy(current_copy)
        for rule in rules:
            current_copy = rule(current_copy)
    return current_copy

# Function which creates an ordered dictionary with each word as key and its corresponding
# translation using map_word() function as value. -> This becomes the childspeak_dictionary.
def create_word_maps(input_list: List[str]) -> dict:
    new_dict = {input: map_word(input) for input in input_list}
    return OrderedDict(new_dict)

# Function which returns a list of tuples, containing each word and the number of occurences 
# for that word in the input dictionary (the one created with the above function).
# First we reverse that dictionary so that each value becomes key and each key is part of a list
# that contains all the words which translates to that value. Then we create the tuple out 
# of the new dictionary getting the number of items for each key, number which represents the total
# occurences for any given word.
def count_multiple_words(input_dict: OrderedDict) -> list:
    reversed_dictionary = {}
    list_of_occurences = []
    for key, value in input_dict.items():
        reversed_dictionary.setdefault(value, set()).add(key)
    for key in input_dict.keys():
        number_of_words = len(reversed_dictionary[input_dict[key]]) -1
        tuple_of_results = (key, number_of_words)
        list_of_occurences.append(tuple_of_results)
    return list_of_occurences
    
#Main function which invokes all the methods used and explained above.
if __name__ == "__main__":
    list_of_words = read_input()
    childspeak_dictionary = create_word_maps(list_of_words)
    list_of_occurences = count_multiple_words(childspeak_dictionary)
    write_output(list_of_occurences)





