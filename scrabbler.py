from asyncio import sleep
import sys
import argparse
import threading
import time
from unscrambler import getAllUnscrabledWords

program_description = """Scrabbler:\t\t
A simple command-line tool to find scrabble words 
from a set of letters and calculate their base score.
"""
parser = argparse.ArgumentParser(description=program_description)
parser.add_argument('-top', type=int, help="Top x words based on score", required=True)
parser.add_argument('-l', type=str, help="Available Letters", required=True)

scrabble_points = {
    'A': 1, 'E': 1, 'I': 1, 'L': 1, 'N': 1, 'O': 1, 'R': 1, 'S': 1, 'T': 1, 'U': 1,
    'D': 2, 'G': 2,
    'B': 3, 'C': 3, 'M': 3, 'P': 3,
    'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4,
    'K': 5,
    'J': 8, 'X': 8,
    'Q': 10, 'Z': 10
}

stop_thread = True


def getValue(c):
    return scrabble_points.get(c.upper(), 0)

def display_searching():
    spinner = ['/', '-', '\\', '|']
    idx = 0
    while not stop_thread:
        print(f"\rSEARCHING...{spinner[idx]}", end='', flush=True)
        idx = (idx + 1) % len(spinner)
        time.sleep(0.1)


if __name__ == "__main__":
    args = parser.parse_args()

    if len(args.l) > 7:
        print("Max 7 letters allowed")
        sys.exit(1)

    stop_thread = False
    t = threading.Thread(target=display_searching)

    if args.top:
        print(f"Top {args.top} words based on score")
        print("=================================")
        t.start()

        words = getAllUnscrabledWords(args.l)
        words = sorted(words, key=lambda x: sum(getValue(c) for c in x), reverse=True)
        
        stop_thread = True
        t.join()
        print("\r", end='', flush=True)
        time.sleep(1) #TODO fix the overwriting to remove all chars from searching message
        for i, word in enumerate(words[:args.top]):
            if len(word) < 5:
                print(f"{i+1}. {word}\t\t{sum(getValue(c) for c in word)}")
            else:
                print(f"{i+1}. {word}\t{sum(getValue(c) for c in word)}")


#modify unscrabler.py for non-main usage