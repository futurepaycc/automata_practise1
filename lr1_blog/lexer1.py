from collections import namedtuple
from itertools import count

Empty = namedtuple('Empty', [])
Symbol = namedtuple('Sym', ['sym'])
Union = namedtuple('Union', ['left', 'right'])
Concat = namedtuple('Concat', ['left', 'right'])
Repeat = namedtuple('Repeat', ['seq'])

def nfa(rule):
    transitions = set()
    new_state = count().__next__
    start = new_state()
    stop = new_state()
    build_nfa(start, stop, rule, new_state, transitions.add)
    return start, stop, transitions, new_state()

def build_nfa(start, stop, rule, new_state, new_transition): 
    if isinstance(rule, Empty):
        new_transition((start, stop, None))
    elif isinstance(rule, Symbol):
        new_transition((start, stop, rule.sym))
    elif isinstance(rule, Union):
        start1 = new_state()
        start2 = new_state()
        stop1 = new_state()
        stop2 = new_state()
        new_transition((start, start1, None))
        new_transition((start, start2, None))
        new_transition((stop1, stop, None))
        new_transition((stop2, stop, None))
        build_nfa(start1, stop1, rule.left, new_state, new_transition)
        build_nfa(start2, stop2, rule.right, new_state, new_transition)
    elif isinstance(rule, Concat):
        mid = new_state()
        build_nfa(start, mid, rule.left, new_state, new_transition)
        build_nfa(mid, stop, rule.right, new_state, new_transition)
    elif isinstance(rule, Repeat):
        start0 = new_state()
        stop0 = new_state()
        new_transition((start, stop, None))
        new_transition((start, start0, None))
        new_transition((stop0, stop, None))
        new_transition((stop0, start0, None))
        build_nfa(start0, stop0, rule.seq, new_state, new_transition)
    else:
        assert False

def recognize(rule, string):
    start,stop,transitions,size = nfa(rule)
    vector = [0] * size
    state = [start]
    step(state, state, transitions, vector, None, 1)
    for i, sym in enumerate(string, 2):
        next_state = []
        step(state, next_state, transitions, vector, sym, i)
        step(next_state, next_state, transitions, vector, None, i)
        state = next_state
    return (stop in state)

def step(state, next_state, transitions, vector, sym, position):
    for st in state:
        for a,b,step in transitions:
            if st == a and step == sym and vector[b] != position:
                vector[b] = position
                next_state.append(b)

if __name__=="__main__":
    empty = Empty()
    sym_a = Symbol('a')
    test_rule = Union(empty, sym_a)
    assert recognize(test_rule, "")
    assert recognize(test_rule, "a")
    assert not recognize(test_rule, "aa")        