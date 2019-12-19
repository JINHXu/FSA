#!/usr/bin/env python3
""" Data Structures and Algorithms for CL III, Assignment 4
    See <https://dsacl3-2019.github.io/a4/> for detailed instructions.

    <Please insert your name and the honor code here.>
"""

import argparse
from fsa import FSA

def insert_words(fsa, words):
    """ E4.2: Insert given words to a finite-state automaton.

    The result of this should be trie. We will obtain a more compact
    automaton by FSA minimization.
    """
    assert True, "TODO: to be implemented"

if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument('input', help="Input file containing a word list.")
    argp.add_argument('--compact', action='store_true',
            help="Compact the lexicon by minimizing the FSA.")
    argp.add_argument('--test', action='store_true',
            help=("Test the lexicon by comparing the words read from "
                  "the file and the words generated from the FSA."))
    args = argp.parse_args()


    words = set()
    with open(args.input, 'rt') as fp:
        for line in fp:
            words.add(line.strip())

    m = FSA()
    insert_words(m, words)

    if args.compact:
        m.minimize()

    words_fsa = set()
    if args.test:
        for w in m.generate():
            words_fsa.add(w)
        if words != words_fsa:
            print("Test failed. {} missed, {} extra".format(
                len(words - words_fsa), len(words_fsa, words)))
