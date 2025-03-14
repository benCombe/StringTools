import random
import sys
import argparse
from wordfinder import WordFinder

parser = argparse.ArgumentParser(description="Process command-line arguments.")
parser.add_argument('-s', type=str, help="Starting Word", required=False)
parser.add_argument('--version', action='store_true', help="version")
#parser.add_argument('--help', action='store_true', help="help")




def load_words(length):
        word_file = f"C:/Program Files/CustomPrograms/words/{length}l_words.txt"
        with open(word_file, 'r') as file:
            words = [line.strip() for line in file if len(line.strip()) == length]
        return words

def has_unique_chars(word):
    return len(set(word)) == len(word)

def main(length, start=None):
    print("== NEW WORD ==")
    wordlist = load_words(length)
    if not wordlist:
        print("No words loaded. Exiting...")
        return

    word_finder = WordFinder(length=length, wordlist=wordlist)

    include = set()  # Use a set to store unique letters
    exclude = set()
    pattern = ["#"] * length  # Correct letter positions
    omit_pattern = [set() for _ in range(length)] # Tracks incorrect positions for '1' letters

    
    while True:
        
        if not wordlist:
            print("No more possible words found.")
            break

        word_finder.update_wordlist(wordlist)

        if start is None:
            max = 3
            count = 0
            while True:
                if count == max:
                    break
                guess = random.choice(wordlist)
                if has_unique_chars(guess):
                    break
                count += 1

        else:
            guess = start
            start = None
        print(f"GUESS: {guess}")

        while True:
            user_eval = input(">: ")
            if user_eval == "exit":
                sys.exit(0)

            if len(user_eval) != length or not all(c in "012" for c in user_eval):
                print(f"Must be {length} characters long and contain only 0, 1, or 2.")
                continue
            
            if user_eval == "2" * length:
                print(f"Found word: {guess}")
                return # restart

            break  # Proceed with normal processing

        for index, c in enumerate(user_eval):
            letter = guess[index]
            if c == '0':
                exclude.add(letter)
            elif c == '1':
                include.add(letter)
                omit_pattern[index].add(letter)
            elif c == '2':  # Correct character in correct position
                pattern[index] = letter
        
        exclude.difference_update(include)
        for p in pattern:
            if p != "#":  # If the position is filled with a letter (not "#")
                exclude.discard(p) # Remove from exclude list

        word_finder.set_include("".join(include))
        word_finder.set_exclude("".join(exclude))
        word_finder.set_pattern(pattern)
        word_finder.set_omit_pattern(omit_pattern)

        wordlist = word_finder.find_words()

if __name__ == "__main__":
    args = parser.parse_args()
    if args.version:
        print("WordleSolver v0.1")
    #elif args.help:
    #    print("WordleSolver v0.1\nFor each letter in GUESS, enter 0 if the letter is not in the word, 1 if the letter is in the word but in the wrong position, and 2 if the letter is in the correct position.\nType 'exit' to quit.")
    else:
        while True:
            if args.s:
                main(5, args.s)
            else:
                main(5)