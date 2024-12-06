import itertools
import random

def generate_passwords(chars="abcdefghijklmnopqrstuvwxyz1234567890", max_length=4, filename="four_characters.txt"):

    all_permutations = []
    for length in range(1, max_length + 1):
        permutations = itertools.product(chars, repeat=length)
        all_permutations.extend([''.join(combination) for combination in permutations])

    random.shuffle(all_permutations)

    with open(filename, "w", encoding="utf-8") as file:
        for password in all_permutations:
            file.write(password + "\n")

if __name__ == "__main__":
    generate_passwords()
