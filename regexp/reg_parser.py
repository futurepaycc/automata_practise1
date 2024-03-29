""" 
来源: https://xysun.github.io/posts/regex-parsing-thompsons-algorithm.html 
优点: 比regexp1, 词法、语法分析更加规范化,有compile阶段,代码少点
缺点: 有些特殊处理，不如regexp1易读
"""

""" 1. 词法 """
class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name + ":" + self.value

class Lexer:
    def __init__(self, pattern):
        self.source = pattern
        self.symbols = {'(':'LEFT_PAREN', ')':'RIGHT_PAREN', '*':'STAR', '|':'ALT', '\x08':'CONCAT', '+':'PLUS', '?':'QMARK'}
        self.current = 0
        self.length = len(self.source)
       
    def get_token(self): 
        if self.current < self.length:
            c = self.source[self.current]
            self.current += 1
            if c not in self.symbols.keys(): # CHAR
                token = Token('CHAR', c)
            else:
                token = Token(self.symbols[c], c)
            return token
        else:
            return Token('NONE', '')

class ParseError(Exception):pass

'''
Grammar for regex:

regex = exp $

exp      = term [|] exp      {push '|'}
         | term
         |                   empty?

term     = factor term       chain {add \x08} #NOTE: 这里的chain指的是concat的吧，\x08 ascii: Sending '\x04' will send EOF . Sending '\x08' is a backspace
         | factor

factor   = primary [*]       star {push '*'}
         | primary [+]       plus {push '+'}
         | primary [?]       optional {push '?'}
         | primary

primary  = \( exp \)
         | char              literal {push char}
'''
""" 2. 文法 """
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.lookahead = self.lexer.get_token()
    
    def consume(self, name):
        if self.lookahead.name == name:
            self.lookahead = self.lexer.get_token()
        elif self.lookahead.name != name:
            raise ParseError

    def parse(self):
        self.exp()
        return self.tokens
    
    def exp(self):
        self.term()
        if self.lookahead.name == 'ALT':
            t = self.lookahead
            self.consume('ALT')
            self.exp()
            self.tokens.append(t)

    def term(self):
        self.factor()
        if self.lookahead.value not in ')|':
            self.term()
            self.tokens.append(Token('CONCAT', '\x08'))
    
    def factor(self):
        self.primary()
        if self.lookahead.name in ['STAR', 'PLUS', 'QMARK']:
            self.tokens.append(self.lookahead)
            self.consume(self.lookahead.name)

    def primary(self):
        if self.lookahead.name == 'LEFT_PAREN':
            self.consume('LEFT_PAREN')
            self.exp()
            self.consume('RIGHT_PAREN')
        elif self.lookahead.name == 'CHAR':
            self.tokens.append(self.lookahead)
            self.consume('CHAR')
"""3. NFA状态机 """
class State:
    def __init__(self, name):
        self.epsilon = [] # epsilon-closure
        self.transitions = {} # char : state
        self.name = name
        self.is_end = False
    
class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end # start and end states
        end.is_end = True
    
    def addstate(self, state, state_set): # add state + recursively add epsilon transitions
        if state in state_set:
            return
        state_set.add(state)
        for eps in state.epsilon:
            self.addstate(eps, state_set)
    
    def pretty_print(self):
        '''
        print using Graphviz
        '''
        pass
    
    # NOTE: 运行核心，这里才像制作状态转移表啊
    def match(self,s):
        current_states = set()
        self.addstate(self.start, current_states)
        for c in s:
            next_states = set()
            for state in current_states:
                if c in state.transitions.keys():
                    trans_state = state.transitions[c]
                    self.addstate(trans_state, next_states)
           
            current_states = next_states

        for s in current_states:
            if s.is_end:
                return True
        return False
""" 4. 把parttern当做表达处理，制作状态转移表么? 
    这里更像一个基于栈的虚拟机！(也类似基于栈的表达式求值)
    TODO: 对测试代码进行debug!
"""
class Handler:
    def __init__(self):
        self.handlers = {'CHAR':self.handle_char, 'CONCAT':self.handle_concat,
                         'ALT':self.handle_alt, 'STAR':self.handle_rep,
                         'PLUS':self.handle_rep, 'QMARK':self.handle_qmark}
        self.state_count = 0

    def create_state(self):
        self.state_count += 1
        return State('s' + str(self.state_count))
    
    def handle_char(self, t, nfa_stack):
        s0 = self.create_state()
        s1 = self.create_state()
        s0.transitions[t.value] = s1
        nfa = NFA(s0, s1)
        nfa_stack.append(nfa)
    
    def handle_concat(self, t, nfa_stack):
        n2 = nfa_stack.pop()
        n1 = nfa_stack.pop()
        n1.end.is_end = False
        n1.end.epsilon.append(n2.start)
        nfa = NFA(n1.start, n2.end)
        nfa_stack.append(nfa)
    
    def handle_alt(self, t, nfa_stack):
        n2 = nfa_stack.pop()
        n1 = nfa_stack.pop()
        s0 = self.create_state()
        s0.epsilon = [n1.start, n2.start]
        s3 = self.create_state()
        n1.end.epsilon.append(s3)
        n2.end.epsilon.append(s3)
        n1.end.is_end = False
        n2.end.is_end = False
        nfa = NFA(s0, s3)
        nfa_stack.append(nfa)
    
    def handle_rep(self, t, nfa_stack):
        n1 = nfa_stack.pop()
        s0 = self.create_state()
        s1 = self.create_state()
        s0.epsilon = [n1.start]
        if t.name == 'STAR':
            s0.epsilon.append(s1)
        n1.end.epsilon.extend([s1, n1.start])
        n1.end.is_end = False
        nfa = NFA(s0, s1)
        nfa_stack.append(nfa)

    def handle_qmark(self, t, nfa_stack):
        n1 = nfa_stack.pop()
        n1.start.epsilon.append(n1.end)
        nfa_stack.append(n1)

def compile(p, debug = False):
    
    def print_tokens(tokens):
        for t in tokens:
            print(t)

    lexer = Lexer(p)
    parser = Parser(lexer)
    tokens = parser.parse()

    handler = Handler()
    
    if debug:
        print_tokens(tokens) 

    nfa_stack = []
    
    # 对每个token创建对应的迷你NFA,然后多个NFA进行栈求值操作?
    for t in tokens:
        handler.handlers[t.name](t, nfa_stack)
    
    assert len(nfa_stack) == 1
    return nfa_stack.pop() 


# ---------------------------------------------------------------------
#  test 
# ---------------------------------------------------------------------
if __name__ == "__main__":
    debug=True
    nfa = compile('ab?', debug)
    if debug:
        nfa.pretty_print()
    print(nfa.match('ab'))