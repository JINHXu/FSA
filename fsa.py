#!/usr/bin/env python3
""" Data Structures and Algorithms for CL III, Assignment 4
    See <https://dsacl3-2019.github.io/a4/> for detailed instructions.

    Course:      Data Structures and Algorithms for CL III - WS1920
    Assignment:  lab4, ex 01 + ex 03
    Author:      Jinghua Xu
    Description: an FSA class.
 
    Honor Code:  I pledge that this program represents my own work.
"""

import sys, random

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
            while s2 in self._states: s2 += 1
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
    # ???
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
        if s1 is None: s1 = self.start_state
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
        for node in self.transitions.get((self.start_state,s[inp_pos]), []):
            agenda.append((node, inp_pos + 1))
        while agenda:
            node, inp_pos = agenda.pop()
            if inp_pos == len(s):
                if node in self.accepting:
                    return True
            else:
                for node in self.transitions.get((node,s[inp_pos]), []):
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
        string = []
        string_counter = 0
        

        if maximum_sentences == 0:
            maximum_sentences = float('inf')
        
        current_state = self.start_state
        l = []
        self.dfs(maximum_sentences, current_state, string, string_counter,l)
    
        for s in l:
            print(s)
    

    def dfs(self, maximum_sentences, current_state, string, string_counter, l):
        for char in self._alphabet:
            # set of next states or None 
            next_states = self.move(char, current_state)
            if next_states:
                for next_state in next_states:
                    string.append(char)
                    if next_state in self.accepting:
                        if string_counter < maximum_sentences:
                            s = ''.join(string)
                            print(s)
                            l.append(s)
                            # yield from l
                            # yield ''.join(string)
                            string_counter +=1
                
                    self.dfs(maximum_sentences, next_state, string, string_counter,l)
                    string.pop()


    '''
    initial idea



    for acc in self.accepting:
        self.construct_all_strings(self.start_state, acc, maximum_sentences)

    
    def construct_all_strings(self, start_state, acc_state, visited, string, maximum_sentences):
        """
        A helper function of generate(), yields the strings accepted by this FSA.
        Parameters
        ----------
        """
        visited[u] = True
        string.append(start_state)

        if start_state == acc_state:

            s = ''.join(string)
            print(s)
            yield s
        
        else:
            for i in 


        
        
        
    # other strtegy: run dfs from one node to another and reconstruct
        
    '''



        
        

    def minimize(self, verbose=False):
        """ E4.3: Minimize the automaton.

        If verbose=True, print out the number of states and arcs
        before and after the minimization.
        """
        assert True, "TODO: to be implemented"

def main():
    m = FSA()
    m.add_arc(0,'w',1)
    m.add_arc(0,'u', 0)
    m.add_arc(1,'a',2)
    m.add_arc(2,'l',3)
    m.add_arc(3,'k',4)
    m.mark_accept(4)
    s = m.add_arc(0,'c')
    m.mark_accept(5)
    m.write_att()
    m.generate()

if __name__== "__main__":
  main()
