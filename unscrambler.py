from asyncio import sleep
import sys
from itertools import permutations
from wordfinder import WordFinder


def printWords(words):
    words = sorted(words)
    for i, word in enumerate(words):
        if (i+1) % 5 == 0 and i != 0:
            print(word, end="\n")
        else:
            print(word, end="\t")        
    print()
    


if __name__ == "__main__":
    if len(sys.argv) > 1:
        letters = sys.argv[1]
        length = len(sys.argv[1])
        

    else:
        letters = input("Enter Letters to Unscramble: ")
        length = len(letters)


    for i in range(4, length):
        wordset = set()
        perms = ["".join(p) for p in permutations(letters, i)]
        print(f"=== {i} Letter Words ===")
        for p in perms:
            #print(f"PERMUTATION: {p}")
            wf = WordFinder(length=i)
            wf.set_include(p)
            for w in wf.find_words():
                wordset.add(w)
        printWords(wordset)

    print(f"=== {length} Letter Words ===")
    wf = WordFinder(length=length)
    wf.set_include(letters)
    printWords(wf.find_words())