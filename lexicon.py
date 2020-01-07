#!/usr/bin/env python3
""" Data Structures and Algorithms for CL III, Assignment 4
    See <https://dsacl3-2019.github.io/a4/> for detailed instructions.
    Course:      Data Structures and Algorithms for CL III - WS1920
    Assignment:  lab 04, ex 02
    Author:      Jinghua Xu
    Description: An Lexicon class reads a list of words from a given file, uses the FSA class as a way to insert all words into a trie.
 
    Honor Code:  I pledge that this program represents my own work.
"""

import argparse
from fsa import FSA

def insert_words(fsa, words):
    """ E4.2: Insert given words to a finite-state automaton.

    The result of this should be trie. We will obtain a more compact
    automaton by FSA minimization.
    Parameters
    ----------
    words : set
         A set of words to be inserted to fsa.
    """
    # states are represented as ints
    # symbols ... strings
    state = 0
    for word in words:
        for symbol in word:
            if symbol in fsa._alphabet:
                # !!!
                continue
            else:
                # last symbol in word
                if symbol == word[-1]:
                    accepting = True
                else:
                    accepting = False
                next_state = fsa.add_arc(state, symbol, None, accepting)
                state = next_state


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
    m.write_att()
    

'''
    if args.compact:
        m.minimize()

    words_fsa = set()
    if args.test:
        for w in m.generate():
            words_fsa.add(w)
        if words != words_fsa:
            print("Test failed. {} missed, {} extra".format(
                len(words - words_fsa), len(words_fsa, words)))
'''