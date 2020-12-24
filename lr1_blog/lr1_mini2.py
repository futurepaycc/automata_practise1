""" 
来源: https://boxbase.org/entries/2019/oct/14/lr1-parsing-tables/
"""

class State:
    def __init__(self):
        self.stack = []
        self.forest = []
        self.top = 0

def advance(st, next_symbol, value):
    while state[st.top][next_symbol](st, value):
        pass

def shift(to):
    def _shift_(st, value):
        st.stack.append(st.top)
        st.forest.append(value)
        st.top = to
        return False
    return _shift_

def reduce(count, symbol, name):
    def _red_(st, value):
        args = []
        for _ in range(count):
            st.top = st.stack.pop()
            args.append(st.forest.pop())
        args.append(":" + name)
        args.reverse()
        state[st.top][symbol](st, args)
        return True
    return _red_

def accept():
    def _accept_(st, value):
        st.top = st.stack.pop()
        item = st.forest.pop()
        print('accepted {}'.format(item))
        return False
    return _accept_

state = [
    {'$':           reduce(0, 'program', 'empty'),
     'varDecl':     reduce(0, 'program', 'empty'),
     'constDecl':   reduce(0, 'program', 'empty'),
     'statement':   reduce(0, 'program', 'empty'),
     'program':     shift(1)},
    {'$':           accept(),
     'declaration': shift(2),
     'varDecl':     shift(3),
     'constDecl':   shift(4),
     'statement':   shift(5)},
    {'$':           reduce(2, 'program', 'sequence'),
     'varDecl':     reduce(2, 'program', 'sequence'),
     'constDecl':   reduce(2, 'program', 'sequence'),
     'statement':   reduce(2, 'program', 'sequence')},
    {'$':           reduce(1, 'declaration', 'var'),
     'varDecl':     reduce(1, 'declaration', 'var'),
     'constDecl':   reduce(1, 'declaration', 'var'),
     'statement':   reduce(1, 'declaration', 'var')},
    {'$':           reduce(1, 'declaration', 'const'),
     'varDecl':     reduce(1, 'declaration', 'const'),
     'constDecl':   reduce(1, 'declaration', 'const'),
     'statement':   reduce(1, 'declaration', 'const')},
    {'$':           reduce(1, 'declaration', 'statement'),
     'varDecl':     reduce(1, 'declaration', 'statement'),
     'constDecl':   reduce(1, 'declaration', 'statement'),
     'statement':   reduce(1, 'declaration', 'statement')}]

if __name__ == "__main__":
    # Successful parse
    st = State()
    advance(st, 'statement', '123 = 4')
    advance(st, 'varDecl', 'var abc')
    advance(st, '$', None)
    print(st.stack)
    print(st.top)

    # Failing parse
    # st = State()
    # advance(st, 'statement', '123 = 4')
    # advance(st, 'foo', 'foo')