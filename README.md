# [Assignment 4: Finite-state Automata](https://dsacl3-2019.github.io/a4/)

You need to follow the link on the
[private course page](https://github.com/dsacl3-2019/dsacl3)
to work on your repository.
The deadline for this assignment is **Monday, January 20th,
8:00 CET**. 

You are strongly recommended to use git properly/productively: commit
every 'unit' of work (e.g., individual exercises) and bug fixes
separately. You do not need to worry about the mistakes in the earlier
commits. Your assignment will be evaluated based only on the final
commit before the deadline. Also, don't forget to add your information
and the honor code to each file that you modify.

This assignment covers exercises with finite state automata.

## 4.1 Generating strrings from finite state automata 

You are given a partial implementation of a finite state automata
class in [fsa.py](fsa.py).

The class keeps the FSA transition table
as a Python dictionary with `(source_state, symbol)` tuples as index,
where the value is the set of target states 
reached from the `source_state` with the `symbol`.
Naturally, if the automaton is a DFA, the value is a singleton set.

Modify the provided FSA class to implement the method `generate()`.
The method should traverse the automaton in a depth-first manner,
returning all or a limited number of strings accepted
by the automaton as specified in the template.

**+1 bonus** if you use a
[Python generator(s)](https://docs.python.org/3/howto/functional.html#generators)
to yield the results as soon as a string is generated
(an accepting state is reached during traversal).

## 4.2 Tries again!

Implement the function `insert_words()`
in file [lexicon.py](lexicon.py)
which reads a list of words from a given file,
uses the FSA class as a way to insert all words into a trie.
The resulting trie (FSA) should be a DFA,
where arc labels are letters as in the following figure
showing an example trie with words
_walk_, _walks_, _wall_, _walls_, _want_, _wants_, _work_ and _works_.

![](example-trie.png)

Test the trie lexicon implementation,
showing that it generates all and the only the words inserted.

## 4.3 Compacting the lexicon

Implement the `minimize()` method of the FSA class.
You can use any of the minimization methods discussed in the class.

Again, test the compacted lexicon,
making sure that it generates all and the only the words inserted.
