#!/usr/bin/env python3

import string

from trie import Trie


def main():
    tree = Trie(string.ascii_lowercase)

    print("Loading words...")

    with open("words.txt") as file:
        for word in file:
            tree.insert(word.strip(), None)

    print(f"Length: {len(tree)}")
    print(f"Length (computed): {tree.count()}")
    print(f"Nodes (computed): {tree.size()}")
    print(f"Depth (computed): {tree.depth()}")
    print("Ready")
    print()

    while True:
        word = input("Enter word to search for: ").strip()

        contained = word in tree
        if contained:
            print(f"The word '{word}' is contained in the tree.")
        else:
            print(f"The word '{word}' is not contained in the tree.")

        results = list("".join(result) for result in tree.keys(word))
        print(f"There are {len(results)} suffixes for '{word}' in the tree,")
        if len(results) <= 10:
            print(f"namely {results}.")
        else:
            print(f"the first 10 of which are {results[:10]}.")
        print()


if __name__ == "__main__":
    main()
