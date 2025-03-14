import argparse
import time
import shutil
from itertools import permutations, product
from wordfinder import WordFinder


parser = argparse.ArgumentParser(description="Process command-line arguments.")
parser.add_argument('-min', type=int, help="min length", required=False)
parser.add_argument('-max', type=int, help="max length", required=False)
parser.add_argument('-a', type=str, help="alphabet", required=False)
parser.add_argument('-p', type=str, help="pattern", required=False)
parser.add_argument('-u', action='store_true', help="unique letters (no doubles)")
parser.add_argument('-ns', action='store_true', help="no special characters")
parser.add_argument('-stdout', action='store_true', help="Standard Output (for Piping)")
parser.add_argument('--version', action='store_true', help="version")

#parser.add_argument('-file', type=str, help="Save to given Filename", required=False)


def format_time(seconds):
    """ Converts seconds into hh:mm:ss format """
    hrs, rem = divmod(int(seconds), 3600)
    mins, secs = divmod(rem, 60)
    return f"{hrs:02}:{mins:02}:{secs:02}"


def print_status(current_word, count, start_time):
    """ Overwrites the previous output dynamically. """
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    formatted_time = format_time(elapsed_time)  # Format into hh:mm:ss
    term_width = shutil.get_terminal_size().columns  # Get terminal width dynamically
    output = f"\rWord: {current_word} | Words Generated: {count} | Time: {formatted_time}"

    # Truncate if the output is wider than the terminal
    print(output[:term_width].ljust(term_width), end="", flush=True)



min = 6
max = 8
alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()-_+=~`[]{}|\\:;\"'<>,.?/"
pattern = None
uniqueLetters = False
wordlist = set()

standardOutput = False
#saveToFile


def main():
    global min, max, alphabet, pattern, uniqueLetters, wordlist
    start_time = time.time()
    word_count = 0

    #if uniqueLetters:
    #for i in range(min, max+1):
    #    perms = (''.join(p) for p in permutations(alphabet, i))  # Generator instead of list
    #    if pattern:
    #        wf = WordFinder(length=i, wordlist=perms)
    #        wf.set_pattern(pattern)
    #        perms = wf.find_words()
    #    wordlist.update(perms)

    if uniqueLetters:
        for i in range(min, max+1):
            for word in (''.join(p) for p in permutations(alphabet, i)):
                if pattern:
                    wf = WordFinder(length=i, wordlist=[word])
                    wf.set_pattern(pattern)
                    word = wf.find_words()
                if standardOutput:
                    print(word)  # Print words for piping
                else:
                    print_status(word, word_count, start_time)
                word_count += 1
            
            
                
    else:
        for i in range(min, max+1):
            for word in (''.join(p) for p in product(alphabet, repeat=i)):
                if pattern:
                    wf = WordFinder(length=i, wordlist=[word])
                    wf.set_pattern(pattern)
                    word = wf.find_words()
                if standardOutput:
                    print(word)  # Print words for piping
                else:
                    print_status(word, word_count, start_time)
                word_count += 1





if __name__ == "__main__":
    args = parser.parse_args()

    if args.version:
        print("WordGrind v0.1")
    else:
        if args.min:
            min = args.min
        if args.max:
            max = args.max
        if args.a:
            alphabet = args.a
        if args.p:
            pattern = args.p
        if args.u:
            uniqueLetters = True
        if args.ns:
            alphabet = alphabet[:62]
        if args.stdout:
            standardOutput = True
        
        main()


    
