import random

alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
special_characters = ["!", "#", "$", "%", "~", "@", "^", "&", "*"]
capital_characters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
all_chars = list()
all_chars.extend(alphabets)
all_chars.extend(capital_characters)
all_chars.extend(numbers)
all_chars.extend(special_characters)


def random_text(len: int):
    return "".join([random.choice(all_chars) for i in range(len)])
