""" 
来源:https://boxbase.org/entries/2019/oct/14/lr1-parsing-tables/ 
"""
class Tokenizer:
    def __init__(self, on_output):
        self.on_output = on_output
        self.state = 'st_0'
        self.column = 1
        self.line   = 1
        self.pos = (1,1)
        self.inp = []

def st_0(tok, ch):
    if ch.isdigit():
        tok.pos = (tok.column, tok.line)
        tok.inp.append(ch)
        tok.state = 'st_digits'
    elif ch.isalpha() or ch == "_":
        tok.pos = (tok.column, tok.line)
        tok.inp.append(ch)
        tok.state = 'st_word'
    elif ch == " " or ch == "\n" or ch == "\t" or ch == "\r":
        pass
    else:
        tok.on_output('error', ch,
            (tok.column, tok.line), (tok.column+1, tok.line))

def st_word(tok, ch):
    if ch.isalpha() or ch == "_" or ch.isdigit():
        tok.inp.append(ch)
    else:
        tok.on_output('word', "".join(tok.inp),
            tok.pos, (tok.column+1, tok.line))
        tok.inp = []
        tok.state = 'st_0'
        st_0(tok, ch)

def st_digits(tok, ch):
    if ch.isdigit():
        tok.inp.append(ch)
    else:
        tok.on_output('digits', "".join(tok.inp),
            tok.pos, (tok.column+1, tok.line))
        tok.inp = []
        tok.state = 'st_0'
        st_0(tok, ch)

# Collects every 'st_' into a dictionary.
tokenize_n = dict((k,v) for k,v in globals().items()
    if k.startswith('st_'))

def tokenize(tok, ch):
    tokenize_n[tok.state](tok, ch)
    if ch == "\n":
        tok.line += 1
        tok.column = 1
    else:
        tok.column += 1

def print_on_output(item, text, start, stop):
    print((item, repr(text), start, stop))

tok = Tokenizer(print_on_output)
#说明：输入文件结尾要有空白符号
with open("/home/liunix/Documents/python/compiler_automata_ws/automata_practise1/lr1_blog/lexer_mini1.txt", "r") as fd:
    for ch in fd.read():
        tokenize(tok, ch)
