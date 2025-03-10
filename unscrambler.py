from asyncio import sleep
import sys
from itertools import permutations
from wordfinder import WordFinder


alphabet = "abcdefghijklmnopqrstuvwxyz"

def printWords(words):
    words = sorted(words)
    for i, word in enumerate(words):
        if (i+1) % 5 == 0 and i != 0:
            print(word, end="\n")
        else:
            print(word, end="\t")        
    print()

def getAllUnscrabledWords(letters):
    allwords = set()
    for i in range(4, len(letters)):
        wordset = set()
        perms = ["".join(p) for p in permutations(letters, i)]
        for p in perms:
            wf = WordFinder(length=i)
            filtered = alphabet.translate(str.maketrans('', '', p))
            wf.set_exclude(filtered)
            wf.set_include(p)
            for w in wf.find_words():
                wordset.add(w)
        allwords.update(wordset)

    wf = WordFinder(length=len(letters))
    filtered = alphabet.translate(str.maketrans('', '', letters))
    wf.set_include(letters)
    wf.set_exclude(filtered)
    allwords.update(wf.find_words())
    return allwords


def main(length, letters):
    wordset = set()
    if length < len(letters):
        perms = ["".join(p) for p in permutations(letters, length)]
        print(f"=== {length} Letter Words ===")
        for p in perms:
            #print(f"PERMUTATION: {p}")
            wf = WordFinder(length=length)
            filtered = alphabet.translate(str.maketrans('', '', p))
            wf.set_exclude(filtered)
            wf.set_include(p)
            for w in wf.find_words():
                wordset.add(w)
        printWords(wordset)
    else:
        print(f"=== {length} Letter Words ===")
        wf = WordFinder(length=length)
        filtered = alphabet.translate(str.maketrans('', '', letters))
        wf.set_include(letters)
        wf.set_exclude(filtered)
        printWords(wf.find_words())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        letters = sys.argv[1]
        length = len(sys.argv[1])
        
    else:
        letters = input("Enter Letters to Unscramble: ")
        length = len(letters)

    for i in range(4, length+1):
        main(i, letters)
        #sleep(1)