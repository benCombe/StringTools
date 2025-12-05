import random
import sys
import argparse
import numpy as np
from wordfinder import WordFinder
from wordlenn import WordleNN

parser = argparse.ArgumentParser(description="Process command-line arguments.")
parser.add_argument('-s', type=str, help="Starting Word", required=False)
parser.add_argument('--version', action='store_true', help="version")
#parser.add_argument('--help', action='store_true', help="help")



# Method to prepare input, with fixed vocab_size
def prepare_input(subset_wordlist, wordlist, vocab_size, desired_size=5749):
    """
    Prepare the one-hot encoded input for the neural network based on the subset of words,
    padding the input to a fixed size using the initial vocab_size.
    """
    X_full = np.zeros((len(subset_wordlist), vocab_size))  # Use fixed vocab_size

    for i, word in enumerate(subset_wordlist):
        if word in wordlist:
            X_full[i, wordlist.index(word)] = 1  # Ensure the word is in the original vocabulary

    # Padding if the input size is smaller than the desired size
    if X_full.shape[0] < desired_size:
        padding = np.zeros((desired_size - X_full.shape[0], vocab_size))
        X_full = np.vstack((X_full, padding))  # Pad the input on the bottom
    
    return X_full

# Method to convert a single word to a one-hot vector, using the fixed vocab_size
def word_to_vector(word, wordlist, vocab_size, desired_size=5749):
    vector = np.zeros(vocab_size)  # Use fixed vocab_size
    if word in wordlist:
        vector[wordlist.index(word)] = 1  # One-hot encoding
    
    # Padding if the input size is smaller than the desired size
    if vector.shape[0] < desired_size:
        padding = np.zeros((desired_size - vector.shape[0]))
        vector = np.concatenate((vector, padding))  # Pad the vector
    
    return vector.reshape(1, -1)  # Reshape to (1, desired_size)

def load_words(length):
        word_file = f"C:/Program Files/CustomPrograms/words/{length}l_words.txt"
        with open(word_file, 'r') as file:
            words = [line.strip() for line in file if len(line.strip()) == length]
        return words

# def has_unique_chars(word):
#     return len(set(word)) == len(word)

def main(length, start=None):
    print("== NEW WORD ==")
    all_words = wordlist = load_words(length)
    init_vocab_size = len(wordlist)
    if not wordlist:
        print("No words loaded. Exiting...")
        return

    word_finder = WordFinder(length=length, wordlist=wordlist)
    neural_net = WordleNN(len(wordlist))

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
            # Convert wordlist to one-hot encoded vectors
            #X = np.array([word_to_vector(word, wordlist) for word in wordlist])
            X_full =  prepare_input(wordlist, all_words, init_vocab_size)
            # Get the best guess from the neural network
            guess_index = neural_net.predict(X_full)
            guess = wordlist[guess_index % len(wordlist)]
        else:
            guess = start
            start = None
        print(f"GUESS: {guess}")

        while True:
            while True:
                user_eval = input(">: ")
                if user_eval == "exit":
                    neural_net.save_model()
                    sys.exit(0)

                if user_eval.lower() == "replace":
                    guess = random.choice(wordlist)
                    print(f"GUESS: {guess}")
                else:
                    break
                

            if len(user_eval) != length or not all(c in "012" for c in user_eval):
                print(f"Must be {length} characters long and contain only 0, 1, or 2.")


                continue
            
            if user_eval == "2" * length:
                    print(f"Found word: {guess}")

                    reward = 1 / len(wordlist)  # Reward smaller guesses
                    y = np.array([[reward]])  # Reshaped target to (1,1)
                    X_input = word_to_vector(guess, wordlist, init_vocab_size) #.reshape(1, -1)  # Ensure shape (1, vocab_size)
                    neural_net.train(X_input, y)  # Train with correctly shaped input

                    return

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
        print("WordleSolver v1.2")
    #elif args.help:
    #    print("WordleSolver v0.1\nFor each letter in GUESS, enter 0 if the letter is not in the word, 1 if the letter is in the word but in the wrong position, and 2 if the letter is in the correct position.\nType 'exit' to quit.")
    else:
        while True:
            if args.s:
                main(5, args.s)
            else:
                main(5)