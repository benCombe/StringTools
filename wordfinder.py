import sys
import argparse


class WordFinder:
    def __init__(self, length=5, wordlist=None):
        if wordlist is None:
            self.wordlist = self.load_words(length)
        else:
            self.wordlist = wordlist
        self.length = length  # Set length based on words
        self.include = ""
        self.exclude = ""
        self.pattern = ["#"] * self.length 
        self.omit_pattern = [set() for _ in range(self.length)]  # Tracks bad placements
        
    def load_words(self, length):
        word_file = f"C:/Program Files/CustomPrograms/words/{length}l_words.txt"
        with open(word_file, 'r') as file:
            words = [line.strip() for line in file if len(line.strip()) == length]
        return words

    def set_length(self, length):
        self.length = length
        self.pattern = "#" * length  # Ensure pattern updates correctly

    def set_exclude(self, exclude_str):
        self.exclude = exclude_str

    def set_include(self, include_str):
        self.include = include_str

    def set_pattern(self, pattern_list):
        if len(pattern_list) != self.length:
            raise ValueError("Pattern length must match the word length")
        self.pattern = pattern_list  # Store as list

    def set_omit_pattern(self, omit_pattern):
        self.omit_pattern = omit_pattern  # Store the omit pattern

    def update_wordlist(self, wordlist):
        self.wordlist = wordlist

    def find_words(self):
        filtered_words = []
        for word in self.wordlist:  # Fixed incorrect variable name
            # 1. Ensure **exact positions match** if known (from '2' feedback)
            if any(self.pattern[i] != "#" and self.pattern[i] != word[i] for i in range(self.length)):
                continue

            # 2. Ensure all **required letters** (from '1' feedback) are present
            if not all(char in word for char in self.include):
                continue

            # 3. Ensure **letters in omit_pattern don't appear in those positions**
            if any(word[i] in self.omit_pattern[i] for i in range(self.length)):
                continue

            # 4. Ensure **excluded letters** do not appear anywhere in the word
            if any(char in word for char in self.exclude):
                continue
            filtered_words.append(word)
        return filtered_words

    def get_wordlist(self):
        return self.wordlist  # Fixed incorrect variable name


# Example usage
if __name__ == "__main__":

    length = 4          # Default length
    include = ""        # Default include
    exclude = ""        # Default exclude
    pattern = "#"*length  # Default pattern

    parser = argparse.ArgumentParser(description="Tool for finding words based on specific alphabets and patterns")

    parser.add_argument('-l', type=str, help="word length", required=False)
    parser.add_argument('-p', type=str, help="pattern", required=False)
    parser.add_argument('-inc', type=str, help="includes", required=False)
    parser.add_argument('-exc', type=str, help="exclude", required=False)
    parser.add_argument('--version', action='store_true', help="version")


    args = parser.parse_args()
    if args.version:
        print("WordFinder v1.2.0")
        sys.exit(0)
        

    if args.l:
        length = int(args.l)
        pattern = "#" * length

    if args.p:
        pattern = [char for char in args.p]

    if args.inc:
        include = args.inc

    if args.exc:
        exclude = args.exc

    wf = WordFinder(length)
    wf.set_include(include)
    wf.set_exclude(exclude)
    wf.set_pattern(pattern)
    words = wf.find_words()
    words.sort()
    for i, word in enumerate(words):
        if i % 3 == 0 and i != 0:
            print()
        print(word, end="\t")

    exit(0)
