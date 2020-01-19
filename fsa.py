#!/usr/bin/env python3
""" Data Structures and Algorithms for CL III, Assignment 4
    See <https://dsacl3-2019.github.io/a4/> for detailed instructions.

    Course:      Data Structures and Algorithms for CL III - WS1920
    Assignment:  lab4, ex 01 + ex 03
    Author:      Jinghua Xu
    Description: an FSA class.
 
    Honor Code:  I pledge that this program represents my own work.
"""

import sys
import random
import math


class FSA:
    """ A class representing finite state automata.
    Args:
        deterministic: The automaton is deterministic
    Attributtes:
        transitions: transitions kept as a dictionary
            where keys are the tuple (source_state, symbol),
            values are the target state for DFA
            and a list of target states for NFA.
            Note that we do not require a dedicated 'sink' state.
            Any undefined transition should cause the FSA to reject the
            string immediately.
        start_state: number/name of the start state
        accepting: the set of accepting states
        is_deterministic (boolean): whether the FSA is deterministic or not
    """

    def __init__(self, deterministic=True):
        self._reset(deterministic)

    def _reset(self, deterministic):
        self.transitions = dict()
        self.start_state = None
        self.accepting = set()
        self.is_deterministic = deterministic
        self._alphabet = set()      # just for convenience, we can
        self._states = set()        # always read it off from transitions

    def add_arc(self, s1, sym, s2=None, accepting=False):
        """ Add an arc from state s1 to s2 with symbol.

        If s2 is not specified, the method creates a new state.
        The return value is s2.

        Note that we follow a convention to specify the states by
        integers. However, the method should work with other ways of
        specifying the state names/numbers.
        """
        if self.start_state is None:
            self.start_state = s1
            self._states.add(s1)
        if s2 is None:
            s2 = len(self._states)
            while s2 in self._states:
                s2 += 1
        self._states.add(s2)
        self._alphabet.add(sym)
        if (s1, sym) not in self.transitions:
            self.transitions[(s1, sym)] = set()
        self.transitions[(s1, sym)].add(s2)
        if accepting:
            self.accepting.add(s2)
        if len(self.transitions[(s1, sym)]) > 1:
            self.deterministic = False
        return s2

    def mark_accept(self, state):
        self.accepting.add(state)

    def unmark_accept(self, state):
        if state in self.accepting:
            self.accepting.remove(state)

    def toggle_accept(self, state):
        if state in self.accepting:
            self.accepting.remove(state)
        else:
            self.accepting.add(state)

    def is_accepting(self, state):
        return state in self.accepting

    def move(self, sym, s1=None):
        """ Return the state(s) reachable from 's1' on 'symbol'
        """
        if s1 is None:
            s1 = self.start_state
        if (s1, sym) not in self.transitions:
            return None
        else:
            return self.transitions[(s1, sym)]

    def _recognize_dfa(self, s):
        """ DFA recognition of 's'.
        """
        state = self.start_state
        for sym in s:
            states = self.transitions.get((state, sym), None)
            if states is None:
                return False
            else:
                state = next(iter(states))
        if state in self.accepting:
            return True
        else:
            return False

    def _recognize_nfa(self, s):
        """ NFA recognition of 's' using a stack-based agenda.
        """
        agenda = []
        state = self.start_state
        inp_pos = 0
        for node in self.transitions.get((self.start_state, s[inp_pos]), []):
            agenda.append((node, inp_pos + 1))
        while agenda:
            node, inp_pos = agenda.pop()
            if inp_pos == len(s):
                if node in self.accepting:
                    return True
            else:
                for node in self.transitions.get((node, s[inp_pos]), []):
                    agenda.append((node, inp_pos + 1))
        return False

    def recognize(self, s):
        """ Recognize the given string 's', return a boolean value
        """
        if self.is_deterministic:
            return self._recognize_dfa(s)
        else:
            return self._recognize_nfa(s)

    def write_att(self, filename=None, dot=False):
        """ Write the FSA to an AT&T formatted text file.

        Not required, but may be useful for testing.
        If the 'dot' argument is True, writes a '.dot' file rathar
        than an AT&T file.
        """
        if filename:
            fp = open(filename, 'w')
        else:
            fp = sys.stdout
        if dot:
            print("digraph {\n"
                  "  rankdir = LR;\n"
                  "  start[style=invis];\n"
                  "  node[shape=circle];", file=fp)
            fmt_transition = "  {} -> {} [label=\"{}\"];"
            fmt_accepting = "  {} [shape=doublecircle];"
        else:
            fmt_transition = "{}\t{}\t{}"
            fmt_accepting = "{}"

        # make sure the first symbol to output is the start state
        for sym in self._alphabet:
            if (self.start_state, sym) in self.transitions:
                for s2 in self.transitions[(self.start_state, sym)]:
                    print(fmt_transition.format(self.start_state, s2, sym),
                          file=fp)
        for s1, sym in self.transitions:
            if s1 != self.start_state:
                for s2 in self.transitions[(s1, sym)]:
                    print(fmt_transition.format(s1, s2, sym), file=fp)
        for st in self.accepting:
            print(fmt_accepting.format(st), file=fp)
        if dot:
            print("}", file=fp)
        if filename:
            fp.close()

    def to_dot(self, filename=None):
        """ Build a string that contains the 'dot' representation
        of the graph, and write to 'filename', or standard output
        if not specified.

        You may use this function to visualize your results and
        visualize the changes you perform on the FSA.
        The functionality is implemented in write_att(),
        this method is just a wrapper.
        """
        self.write_att(filename, dot=True)

    def generate(self, maximum_sentences=0):
        """ E4.1: Generate all string accepted by the automaton.

        The optional argument maximum_sentences specify the maximum
        number of strings to generate. If maximum_sentences=0, the
        method should print all possible strings in the language of
        the automata (note that this may run forever in case of an FSA
        with cycles).
        """

        if maximum_sentences == 0:
            maximum_sentences = float('inf')

        current_state = self.start_state
        for index, word in enumerate(self.dfs(current_state), 1):
            yield word
            if index == maximum_sentences:
                return

    def dfs(self, current_state):
        """
        A helper function of generate. Search the FSA in depth-first manner.
        Parameter
        ----------
        current_state : int
                The current state(a state in FSA) of the search.
        """
        stack = [(current_state, [])]
        while stack:
            current_state, string = stack.pop()
            for char in self._alphabet:
                next_states = self.move(char, current_state)
                if not next_states:
                    continue

                for next_state in next_states:
                    if next_state in self.accepting:
                        yield ''.join(string) + char

                    stack.append((next_state, string + [char]))

    def minimize(self, verbose=False):
        """ E4.3: Minimize the automaton.

        If verbose=True, print out the number of states and arcs
        before and after the minimization.
        """

        '''Create a state-by-state table,mark distinguishable pairs: (q1, q2) 
        such that (∆(q1, x), ∆(q2, x)) is a distinguishable pair for any x ∈ Σ'''

        distinguishable_pairs = set()

        # len(self._states) is one smaller, because start state is not in the set of states(on purpose)
        num_states = len(self._states) + 1

        # initialization: acc states are firstly partinioned
        for state1 in range(num_states-1):
            for state2 in range(state1+1, num_states):
                if state1 < state2:
                    if (state2 in self.accepting) != (state1 in self.accepting):
                        distinguishable_pairs.add((state1, state2))

        # loop termination marker
        just_updated = True

        # the loop will terminate when there is no further updates during each traversal of the state-by-state table
        while just_updated:
            just_updated = False
            # traverse the state-by-state table
            for state1 in range(num_states - 1):
                for state2 in range(state1+1, num_states):
                    if (state1, state2) not in distinguishable_pairs:
                        for sym in self._alphabet:
                            # in the case we are expected to deal with, there can be at most one next move
                            next1 = self.move(sym, state1)
                            next2 = self.move(sym, state2)
                            if next1 and next2:
                                # the only one element in set of next moves(DFA feature)
                                n1 = next(iter(next1))
                                n2 = next(iter(next2))

                                if (n1, n2) in distinguishable_pairs:
                                    distinguishable_pairs.add((state1, state2))
                                    just_updated = True

                            elif (next1 is None and next2 is not None) or (next2 is None and next1 is not None):
                                distinguishable_pairs.add((state1, state2))

        indisdinguishable_pairs = set()
        for state1 in range(num_states-1):
            for state2 in range(1, num_states):
                if state1 < state2 and (state1, state2) not in distinguishable_pairs:
                    indisdinguishable_pairs.add((state1, state2))

        # merge pair by pair
        while indisdinguishable_pairs:
            indisdinguishable_pair = indisdinguishable_pairs.pop()

            state1, state2 = indisdinguishable_pair

            # to make sure the merged state is unique(no name collision with other states)
            merged_state = state1

            # update states in fsa: replace all state2 with state1
            for key, value in self.transitions.items():
                # transition where state2 is a target state
                if state2 in value:

                    self.transitions[key].add(merged_state)

                    self.transitions[key].remove(state2)

            # transition where state2 is the origin state
            for sym in self._alphabet:
                next_move = self.move(sym, state2)
                if next_move:
                    if (merged_state, sym) in self.transitions.keys():
                        self.transitions[(merged_state, sym)].update(next_move)
                    else:
                        self.transitions[(merged_state, sym)] = next_move
                    del self.transitions[(state2, sym)]

            indisdinguishable_pairs_copy = indisdinguishable_pairs.copy()
            # update states in indistinguishable pairs
            for pair in indisdinguishable_pairs_copy:
                if pair[0] == state2:
                    indisdinguishable_pairs.add((merged_state, pair[1]))
                    indisdinguishable_pairs.remove(pair)
                elif pair[1] == state2:
                    indisdinguishable_pairs.add((pair[0], merged_state))
                    indisdinguishable_pairs.remove(pair)

            new_indisdinguishable_pairs_copy = indisdinguishable_pairs.copy()
            for pair in new_indisdinguishable_pairs_copy:
                if pair[0] == pair[1]:
                    indisdinguishable_pairs.remove(pair)

        '''delete disconnected states'''
        connected_states = set()
        for target_states in self.transitions.values():
            connected_states.update(target_states)

        states_copy = self._states.copy()
        for state in states_copy:
            if state not in connected_states:
                self._states.remove(state)
                if state in self.accepting:
                    self.accepting.remove(state)
