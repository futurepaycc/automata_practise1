# -*- encoding: utf-8 -*-
"""
    parsergen Rev.3 (with modifications)
    ~~~~~~~~~~~~~~~

    Note the parsing tables have changed a bit from the Rev.2
"""
import argparse, sys, pprint

# This is the syntax that this script understands for now.
grammar_syntax = """
grammar: 
grammar: grammar VALIGN WFB declaration
declaration:
    identifier ":" rhs_block
    "lexemes" identifiers
rhs_block:
rhs_block: rhs_block VALIGN WFB rhs
rhs: 
rhs: rhs symbol
symbol: "VALIGN" symbol
        "WFB" symbol
        identifier
        string
identifiers: identifier
             identifiers "," identifier
lexemes identifier, string
"""
grammar_state = [
  { None: (1, 'grammar_0', 0, 1),
    '"lexemes"': (0, 16, 0),
    '^identifier': (0, 1, 0),
    'declaration': (0, 23, 0),
    'grammar': (0, 22, 0),
    'grammar_0': (0, 21, 0)},
  { '":"': (0, 2, 0)},
  { None: (1, 'declaration', 2, 6),
    '"VALIGN"': (0, 8, 0),
    '"WFB"': (0, 5, 0),
    '"lexemes"': (1, 'declaration', 2, 6),
    '^identifier': (1, 'declaration', 2, 6),
    'identifier': (0, 7, 0),
    'rhs': (0, 4, 0),
    'rhs_1': (0, 10, 0),
    'rhs_block': (0, 13, 0),
    'string': (0, 3, 0),
    'symbol': (0, 12, 0)},
  { None: (1, 'symbol', 1, 16),
    '"VALIGN"': (1, 'symbol', 1, 16),
    '"WFB"': (1, 'symbol', 1, 16),
    '"lexemes"': (1, 'symbol', 1, 16),
    '"|"': (1, 'symbol', 1, 16),
    '^identifier': (1, 'symbol', 1, 16),
    'identifier': (1, 'symbol', 1, 16),
    'string': (1, 'symbol', 1, 16)},
  { None: (1, 'rhs_block', 1, 8),
    '"lexemes"': (1, 'rhs_block', 1, 8),
    '"|"': (1, 'rhs_block', 1, 8),
    '^identifier': (1, 'rhs_block', 1, 8)},
  { '"VALIGN"': (0, 8, 0),
    '"WFB"': (0, 5, 0),
    'identifier': (0, 7, 0),
    'string': (0, 3, 0),
    'symbol': (0, 6, 0)},
  { None: (1, 'symbol', 2, 14),
    '"VALIGN"': (1, 'symbol', 2, 14),
    '"WFB"': (1, 'symbol', 2, 14),
    '"lexemes"': (1, 'symbol', 2, 14),
    '"|"': (1, 'symbol', 2, 14),
    '^identifier': (1, 'symbol', 2, 14),
    'identifier': (1, 'symbol', 2, 14),
    'string': (1, 'symbol', 2, 14)},
  { None: (1, 'symbol', 1, 15),
    '"VALIGN"': (1, 'symbol', 1, 15),
    '"WFB"': (1, 'symbol', 1, 15),
    '"lexemes"': (1, 'symbol', 1, 15),
    '"|"': (1, 'symbol', 1, 15),
    '^identifier': (1, 'symbol', 1, 15),
    'identifier': (1, 'symbol', 1, 15),
    'string': (1, 'symbol', 1, 15)},
  { '"VALIGN"': (0, 8, 0),
    '"WFB"': (0, 5, 0),
    'identifier': (0, 7, 0),
    'string': (0, 3, 0),
    'symbol': (0, 9, 0)},
  { None: (1, 'symbol', 2, 13),
    '"VALIGN"': (1, 'symbol', 2, 13),
    '"WFB"': (1, 'symbol', 2, 13),
    '"lexemes"': (1, 'symbol', 2, 13),
    '"|"': (1, 'symbol', 2, 13),
    '^identifier': (1, 'symbol', 2, 13),
    'identifier': (1, 'symbol', 2, 13),
    'string': (1, 'symbol', 2, 13)},
  { None: (1, 'rhs', 1, 10),
    '"VALIGN"': (0, 8, 0),
    '"WFB"': (0, 5, 0),
    '"lexemes"': (1, 'rhs', 1, 10),
    '"|"': (1, 'rhs', 1, 10),
    '^identifier': (1, 'rhs', 1, 10),
    'identifier': (0, 7, 0),
    'string': (0, 3, 0),
    'symbol': (0, 11, 0)},
  { None: (1, 'rhs_1', 2, 12),
    '"VALIGN"': (1, 'rhs_1', 2, 12),
    '"WFB"': (1, 'rhs_1', 2, 12),
    '"lexemes"': (1, 'rhs_1', 2, 12),
    '"|"': (1, 'rhs_1', 2, 12),
    '^identifier': (1, 'rhs_1', 2, 12),
    'identifier': (1, 'rhs_1', 2, 12),
    'string': (1, 'rhs_1', 2, 12)},
  { None: (1, 'rhs_1', 1, 11),
    '"VALIGN"': (1, 'rhs_1', 1, 11),
    '"WFB"': (1, 'rhs_1', 1, 11),
    '"lexemes"': (1, 'rhs_1', 1, 11),
    '"|"': (1, 'rhs_1', 1, 11),
    '^identifier': (1, 'rhs_1', 1, 11),
    'identifier': (1, 'rhs_1', 1, 11),
    'string': (1, 'rhs_1', 1, 11)},
  { None: (1, 'declaration', 3, 5),
    '"lexemes"': (1, 'declaration', 3, 5),
    '"|"': (0, 14, 0),
    '^identifier': (1, 'declaration', 3, 5)},
  { '"VALIGN"': (0, 8, 0),
    '"WFB"': (0, 5, 0),
    'identifier': (0, 7, 0),
    'rhs': (0, 15, 0),
    'rhs_1': (0, 10, 0),
    'string': (0, 3, 0),
    'symbol': (0, 12, 0)},
  { None: (1, 'rhs_block', 3, 9),
    '"lexemes"': (1, 'rhs_block', 3, 9),
    '"|"': (1, 'rhs_block', 3, 9),
    '^identifier': (1, 'rhs_block', 3, 9)},
  { 'identifier': (0, 20, 0), 'identifiers': (0, 17, 0)},
  { None: (1, 'declaration', 2, 7),
    '","': (0, 18, 0),
    '"lexemes"': (1, 'declaration', 2, 7),
    '^identifier': (1, 'declaration', 2, 7)},
  { 'identifier': (0, 19, 0)},
  { None: (1, 'identifiers', 3, 18),
    '","': (1, 'identifiers', 3, 18),
    '"lexemes"': (1, 'identifiers', 3, 18),
    '^identifier': (1, 'identifiers', 3, 18)},
  { None: (1, 'identifiers', 1, 17),
    '","': (1, 'identifiers', 1, 17),
    '"lexemes"': (1, 'identifiers', 1, 17),
    '^identifier': (1, 'identifiers', 1, 17)},
  { None: (1, None, 1, 0)},
  { None: (1, 'grammar_0', 1, 2)},
  { None: (1, 'grammar', 1, 3),
    '"lexemes"': (0, 16, 0),
    '^identifier': (0, 1, 0),
    'declaration': (0, 23, 0),
    'grammar': (0, 24, 0)},
  { None: (1, 'grammar', 2, 4)}]

parser = argparse.ArgumentParser(
    description='Generate decision tables for LR(1) parser')
parser.add_argument('grammar',type=str,
    help='The input grammar to use, the syntax is described inside this script.')
parser.add_argument('--lalr',
    dest='flavor', default='lr', action='store_const', const='lalr',
    help='Generate LALR tables instead of LR')
parser.add_argument('-p', '--printsets',
    action='store_const', const=True, default=False,
    help='Print the itemset table to stdout')
parser.add_argument('-m', '--printmore',
    action='store_const', const=True, default=False,
    help='Print more details to stdout')
parser.add_argument('-o', '--output',type=str,
    help='Python-formatted output of the parsing tables.')

args = parser.parse_args()
input_filename = args.grammar
python_output = args.output
parser_flavor = args.flavor
print_itemsets_to_stdout = args.printsets
print_more_to_stdout = args.printmore

# When the grammar file is obtained, it gets tokenized and parsed.
class Tokenizer:
    def __init__(self):
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
    elif ch == " " or ch == "\n" or ch == "\t" or ch == "\r" or ch is "":
        pass
    elif ch == "#":
        tok.state = 'st_comment'
    elif ch == ",":
        advance('","', ch, (tok.column, tok.line), (tok.column+1, tok.line))
    elif ch == ":":
        advance('":"', ch, (tok.column, tok.line), (tok.column+1, tok.line))
    elif ch == "|":
        advance('"|"', ch, (tok.column, tok.line), (tok.column+1, tok.line))
    elif ch == '"':
        tok.pos = (tok.column, tok.line)
        tok.state = 'st_string'
    else:
        print(("error token: {} at {}".format(ch, tok.line)))
        advance('error', ch,
            (tok.column, tok.line), (tok.column+1, tok.line))

def st_comment(tok, ch):
    if ch == "\n":
        tok.state = 'st_0'

def st_word(tok, ch):
    if ch.isalpha() or ch == "_" or ch.isdigit():
        tok.inp.append(ch)
    else:
        text = "".join(tok.inp)
        if text == "lexemes":
            advance('"' + text + '"', text, tok.pos, (tok.column+1, tok.line))
        elif text in ("WFB", "VALIGN"):
            advance('"' + text + '"', text, tok.pos, (tok.column+1, tok.line))
        elif tok.pos[0] == 1:
            advance('^identifier', text, tok.pos, (tok.column+1, tok.line))
        else:
            advance('identifier', text, tok.pos, (tok.column+1, tok.line))
        tok.inp = []
        tok.state = 'st_0'
        st_0(tok, ch)

def st_digits(tok, ch):
    if ch.isdigit():
        tok.inp.append(ch)
    else:
        advance('digits', "".join(tok.inp),
            tok.pos, (tok.column+1, tok.line))
        tok.inp = []
        tok.state = 'st_0'
        st_0(tok, ch)

def st_string(tok, ch):
    if ch == '"':
        advance('string', "".join(tok.inp),
            tok.pos, (tok.column,tok.line))
        tok.inp = []
        tok.state = 'st_0'
    else:
        tok.inp.append(ch)

# Collects every 'st_' into a dictionary.
tokenize_n = dict((k,v) for k,v in list(globals().items())
    if k.startswith('st_'))

def tokenize(tok, ch):
    tokenize_n[tok.state](tok, ch)
    if ch == "\n":
        tok.line += 1
        tok.column = 1
    else:
        tok.column += 1

# The parsing step
class Parser:
    def __init__(self):
        self.stack = []
        self.forest = []
        self.top = 0
        #self.layout = 0
p = Parser()

def advance(item, text, start, stop):
    arg = grammar_state[p.top][item]
    while arg[0] == 1:
        lhs = arg[1]
        count = arg[2]
        items = []
        for _ in range(arg[2]):
            p.top = p.stack.pop()
            items.append(p.forest.pop())
        items.reverse()
        reduced_item = reduction(arg[3], items)
        if lhs is None:
            p.stack = []
            p.forest = []
            p.top = 0
            return
        else:
            arg = grammar_state[p.top][lhs]
            assert arg[0] == 0
            p.stack.append(p.top)
            p.forest.append(reduced_item)
            p.top = arg[1]
            arg = grammar_state[p.top][item]
    #if arg[2] & 1 != 0: # VALIGN
    #    print action, arg1, arg2
    #    sys.exit(1)
    p.forest.append(text)
    p.stack.append(p.top)
    p.top = arg[1]
    #if arg[2] & 2 != 0: # WFB
    #    p.layout = start[0]
    # print((item, text, start, stop))
    # print "shift to", p.top

class InputGrammar:
    def __init__(self):
        self.lexemes = set()
        self.keywords = set()
        self.grammar = []
        self.wfb = set()
        self.valign = set()
        self.ok = False
input_grammar = InputGrammar()

# The reduction table needs to be changed if grammar changes.
def reduction(arg, items):
    if arg == 0:                            # ⊤ → grammar_0
        input_grammar.ok = True
    elif arg == 1:                            # grammar_0 → 
        pass
    elif arg == 2:                            # grammar_0 → grammar
        pass
    elif arg == 3:                            # grammar → declaration
        pass
    elif arg == 4:                            # grammar → declaration grammar
        pass
    elif arg == 5:                            # declaration → ^identifier ":" rhs_block
        if len(input_grammar.grammar) == 0:
            input_grammar.grammar.append((None, [items[0]]))
        for annotated_rhs in items[2]:
            rule = len(input_grammar.grammar)
            rhs = []
            for index, (item, flags) in enumerate(annotated_rhs):
                rhs.append(item)
                if 'WFB' in flags:
                    input_grammar.wfb.add((rule, index))
                if 'VALIGN' in flags:
                    input_grammar.valign.add((rule, index))
            input_grammar.grammar.append((items[0], rhs))
    elif arg == 6:                            # declaration → ^identifier ":"
        if len(input_grammar.grammar) == 0:
            input_grammar.grammar.append((None, [items[0]]))
        input_grammar.grammar.append((items[0], []))
    elif arg == 7:                            # declaration → "lexemes" identifiers
        input_grammar.lexemes.update(items[1])
    elif arg == 8:                            # rhs_block → rhs
        return [items[0]]
    elif arg == 9:                            # rhs_block → rhs_block "|" rhs
        return items[0] + [items[2]]
    elif arg == 10:                           # rhs → rhs_1
        return items[0]
    elif arg == 11:                           # rhs_1 → symbol
        return [items[0]]
    elif arg == 12:                           # rhs_1 → rhs_1 symbol
        return items[0] + [items[1]]
    elif arg == 13:                           # symbol → "VALIGN" symbol
        items[1][1].add('VALIGN')
        return items[1] # These probably do not even appear because
                        # tokenizer doesn't recognize these keywords yet.
    elif arg == 14:                           # symbol → "WFB" symbol
        items[1][1].add('WFB')
        return items[1]
    elif arg == 15:                           # symbol → identifier
        return (items[0], set())
    elif arg == 16:                           # symbol → string
        # Add each of these into keywords and lexeme sets.
        input_grammar.keywords.add(items[0])
        input_grammar.lexemes.add('"' + items[0] + '"')
        return ('"' + items[0] + '"', set())
    elif arg == 17:                           # identifiers → identifier
        return [items[0]]
    elif arg == 18:                           # identifiers → identifiers "," identifier
        return items[0] + [items[2]]
    else:
        print(("unknown reduction rule: {} {}".format(arg, items)))

tok = Tokenizer()
with open(input_filename, "r") as fd:
    for ch in fd.read():
        tokenize(tok, ch)
tokenize(tok, "")
advance(None, "", (0,0), (0,0))

grammar = input_grammar.grammar
lexemes = input_grammar.lexemes
keywords = input_grammar.keywords
wfb_constraints = input_grammar.wfb
valign_constraints = input_grammar.valign

def print_grammar():
    for lhs, rhs in grammar:
        print(("{} → {}".format(lhs or '⊤', " ".join(rhs))))

def print_item(prefix, xxx_todo_changeme, fd=sys.stdout):
    (rule, index) = xxx_todo_changeme
    lhs, rhs = grammar[rule]
    fd.write("{}{} → {}\n".format(prefix, lhs or '⊤',
        " ".join(rhs[:index] + ['∘'] + rhs[index:])))

def print_itemset(index, items, fd=sys.stdout):
    prefix = "{}: ".format(index)
    for item in items:
        print_item(prefix, item, fd)
        prefix = " " * len(prefix)

# The following routine builds the LR0 itemsets
def after_dot(xxx_todo_changeme1):
    (rule, index) = xxx_todo_changeme1
    lhs, rhs = grammar[rule]
    if index < len(rhs):
        return rhs[index]

def predict(items):
    visited = set(items)
    prediction = set()
    while len(items) > 0:
        sym = after_dot(items.pop())
        for index, (lhs,rhs) in enumerate(grammar):
            if sym == lhs and sym is not None:
                item = (index, 0)
                if item not in visited:
                    items.append(item)
                    prediction.add(item)
                    visited.add(item)
    return prediction

def partition(items):
    groups = {}
    for item in items:
        sym = after_dot(item)
        # The items to be shifted are already shifted here,
        # so they won't need the treatment later.
        if sym is not None:
            item = (item[0], item[1]+1)
        try:
            groups[sym].append(item)
        except KeyError as _:
            groups[sym] = [item]
    return [(sym, frozenset(items)) for sym,items in list(groups.items())]

seed_itemsets = [ frozenset([(0,0)]) ]
prediction_itemsets = []
itemsets_index = dict((s,i) for i,s in enumerate(seed_itemsets))
shifts = []
reductions = []
vectors = []
for k, seed_itemset in enumerate(seed_itemsets):
    prediction_itemset = predict(list(seed_itemset))
    itemset = seed_itemset | prediction_itemset
    prediction_itemsets.append(prediction_itemset)
    k_shifts = []
    k_reductions = set()
    for sym, items in partition(itemset):
        if sym is None:
            k_reductions.update(items)
        else:
            # If the seed itemset is not already in the table,
            # it'll be added to the table.
            try:
                j = itemsets_index[items]
            except KeyError as _:
                j = len(seed_itemsets)
                itemsets_index[items] = j
                seed_itemsets.append(items)
            k_shifts.append((sym, j))
    # The reductions and shifts are recorded
    # this way they don't need to be recorded later.
    shifts.append(k_shifts)
    reductions.append(k_reductions)
    # Vectors are used for memoizing itemsets later.
    # It is sorted so that lookahead vectors appear in same order
    # as what the itemsets are printed in.
    vectors.append(tuple(sorted(seed_itemset)))
    # Separating and sorting the itemsets provides easy, cleaner printout.
    if print_itemsets_to_stdout:
        print_itemset(k, list(vectors[k]) + list(sorted(prediction_itemset)))

# This is a good point to warn if the grammar did not parse completely.
exit_status = 0
if not input_grammar.ok:
    exit_status = 1
    sys.stderr.write("warning: The parsing encountered errors\n")

# Compute the set of empty symbols in the grammar.
def empty_symbols():
    symbols = set()
    for lhs,rhs in grammar:
        if len(rhs) == 0:
            symbols.add(lhs)
    m = 0
    n = len(symbols)
    while m < n:
        for lhs, rhs in grammar:
            if all(x in symbols for x in rhs):
                symbols.add(lhs)
        m = n
        n = len(symbols)
    return symbols
empty = empty_symbols()

# Check the constraints are well-formed.
empty_valign_wfb = set()
for point in wfb_constraints | valign_constraints:
    sym = after_dot(point)
    if sym in empty:
        empty_valign_wfb.add(sym)

if len(empty_valign_wfb) > 0:
    exit_status = 1
    sys.stderr.write(
        "warning: Constraints in empty symbols\n"
        "    Constraints will end up dangling if their rules are empty\n"
        "    constrained empty symbols:\n"
        "    {}\n".format(",".join(map(repr,sorted(empty_valign_wfb)))))

# FIRST & VFIRST -sets construction
def first_lexemes():
    symbols = dict()
    routes = set()
    for sym in lexemes:
        symbols[sym] = set([sym])
    for lhs, rhs in grammar:
        if lhs not in symbols:
            symbols[lhs] = set([])
    for rule, (lhs, rhs) in enumerate(grammar):
        for index, rhsN in enumerate(rhs):
            if (rule,index) not in valign_constraints:
                routes.add((lhs,rhsN))
            if rhsN not in empty:
                break
    rep = True
    while rep:
        rep = False
        for lhs, rhs0 in routes:
            n = len(symbols[lhs])
            symbols[lhs].update(symbols[rhs0])
            rep |= n < len(symbols[lhs])
    return symbols
first = first_lexemes()

def vfirst_lexemes():
    symbols = dict()
    routes = set()
    for sym in lexemes:
        symbols[sym] = set([])
    for lhs, rhs in grammar:
        if lhs not in symbols:
            symbols[lhs] = set([])
    for rule, (lhs, rhs) in enumerate(grammar):
        for index, rhsN in enumerate(rhs):
            if (rule,index) in valign_constraints:
                symbols[lhs].update(first[rhsN])
            if rhsN not in empty:
                break
    rep = True
    while rep:
        rep = False
        for lhs, rhs0 in routes:
            n = len(symbols[lhs])
            symbols[lhs].update(symbols[rhs0])
            rep |= n < len(symbols[lhs])
    return symbols
vfirst = vfirst_lexemes()

# FOLLOW -sets
def examine(xxx_todo_changeme2):
    (rule,index) = xxx_todo_changeme2
    s = set()
    w = set()
    rhs = grammar[rule][1]
    for i in range(index+1, len(rhs)):
        w.update(vfirst[rhs[i]])
        if (rule,i) in valign_constraints:
            w.update(first[rhs[i]])
        else:
            s.update(first[rhs[i]])
        if rhs[i] not in empty:
            return s,w,False
    return s,w,True

def follow_lexemes(seedset, predictionset):
    seeds   = {}
    symbols = {}
    vsymbols = {}
    routes = set()
    for item in seedset | predictionset:
        sym0 = after_dot(item)
        if sym0 not in symbols and sym0 is not None:
            symbols[sym0] = set()
            vsymbols[sym0] = set()
            seeds[sym0] = set()
    for item in seedset:
        sym0 = after_dot(item)
        if sym0 is None:
            continue
        syms, vsyms, reductive = examine(item)
        symbols[sym0].update(syms)
        vsymbols[sym0].update(vsyms)
        if reductive:
            seeds[sym0].add(item)
    for item in predictionset:
        sym0 = after_dot(item)
        if sym0 is None:
            continue
        syms, vsyms, reductive = examine(item)
        symbols[sym0].update(syms)
        vsymbols[sym0].update(vsyms)
        if reductive:
            lhs = grammar[item[0]][0]
            routes.add((lhs, sym0))
    rep = True
    while rep:
        rep = False
        for lhs, sym in routes:
            n = symbols[sym]
            symbols[sym].update(symbols[lhs])
            rep |= len(n) < len(symbols[sym])
            n = vsymbols[sym]
            vsymbols[sym].update(vsymbols[lhs])
            rep |= len(n) < len(vsymbols[sym])
            n = len(seeds[sym])
            seeds[sym].update(seeds[lhs])
            rep |= n < len(seeds[sym])
    return seeds, symbols, vsymbols

def wfb_sets(seedset, predictionset):
    sym_routes = dict()
    for item in predictionset:
        lhs = grammar[item[0]][0]
        if lhs is None:
            continue
        try:
            sym_routes[lhs].add(item)
        except KeyError as _:
            sym_routes[lhs] = set([item])
    routes = []
    nwfb_items = set()
    wfb_items = set()
    for item in predictionset:
        sym0 = after_dot(item)
        for sym_item in sym_routes.get(sym0, ()):
            if item in wfb_constraints:
                wfb_items.add(sym_item)
            else:
                routes.append((item, sym_item))
    for item in seedset:
        sym0 = after_dot(item)
        if item in wfb_constraints:
            wfb_items.update(sym_routes.get(sym0, ()))
        else:
            nwfb_items.update(sym_routes.get(sym0, ()))
    n = 0
    m = len(nwfb_items) + len(wfb_items)
    while n < m:
        n = m
        for item, sym_item in routes:
            if item in wfb_items:
                wfb_items.add(sym_item)
            if item in nwfb_items:
                nwfb_items.add(sym_item)
        m = len(nwfb_items) + len(wfb_items)
    return wfb_items, nwfb_items

def valign_sets(seedset, predictionset):
    routes = []
    valign_syms = set()
    nvalign_syms = set()
    for item in predictionset:
        lhs = grammar[item[0]][0]
        sym0 = after_dot(item)
        if sym0 is not None:
            if item in valign_constraints:
                valign_syms.add(sym0)
            else:
                routes.append((lhs, sym0))
    for item in seedset:
        sym0 = after_dot(item)
        if sym0 is not None:
            if item in valign_constraints:
                valign_syms.add(sym0)
            else:
                nvalign_syms.add(sym0)
    n = 0
    m = len(valign_syms) + len(nvalign_syms)
    while n < m:
        n = m
        for item, sym_item in routes:
            if item in valign_syms:
                valign_syms.add(sym_item)
            if item in nvalign_syms:
                nvalign_syms.add(sym_item)
        m = len(nvalign_syms) + len(valign_syms)
    valign_syms &= lexemes
    nvalign_syms &= lexemes
    return valign_syms, nvalign_syms

follow_seeds = []
follow_syms = []
follow_vsyms = []
wfbs = []
nwfbs = []
valigns = []
nvaligns = []

for i in range(len(seed_itemsets)):
    seeds,syms,vsyms = follow_lexemes(seed_itemsets[i], prediction_itemsets[i])
    wfb,nwfb = wfb_sets(seed_itemsets[i], prediction_itemsets[i])
    valign,nvalign = valign_sets(seed_itemsets[i], prediction_itemsets[i])
    follow_seeds.append(seeds)
    follow_syms.append(syms)
    follow_vsyms.append(vsyms)
    wfbs.append(wfb)
    nwfbs.append(nwfb)
    valigns.append(valign)
    nvaligns.append(nvalign)

def wfb_rules():
    bitmap = []
    for rule, (lhs,rhs) in enumerate(grammar):
        if (rule,len(rhs)-1) not in wfb_constraints:
            is_wfb = False
        else:
            is_wfb = all((((rule,index) in valign_constraints)
                          or (len(first[rhs[index]]) == 0))
                         for index in range(1, len(rhs)))
        bitmap.append(is_wfb)
    return bitmap
wfbr = wfb_rules()

if print_more_to_stdout: # Print FIRST/VFIRST -sets
    print('FIRST')
    for sym in first:
        print(("  {}: {}".format(sym, ",".join(map(repr, first[sym])))))
    print('VFIRST')
    for sym in vfirst:
        print(("  {}: {}".format(sym, ",".join(map(repr, vfirst[sym])))))
    print('FOLLOW (SEED)')
    for k, items in enumerate(follow_seeds):
        print(("  {}: {}".format(k, items)))
    print('FOLLOW')
    for k, items in enumerate(follow_syms):
        print(("  {}: {}".format(k, items)))
    print('FOLLOW (VALIGN)')
    for k, items in enumerate(follow_vsyms):
        print(("  {}: {}".format(k, items)))
    print('WFB ITEMS')
    for k, items in enumerate(wfbs):
        print_itemset(k, sorted(items))
    print('NWFB ITEMS')
    for k, items in enumerate(nwfbs):
        print_itemset(k, sorted(items))
    print('VALIGN LEXEMES')
    for k, items in enumerate(valigns):
        print(("  {}: {}".format(k, items)))
    print('NVALIGN LEXEMES')
    for k, items in enumerate(nvaligns):
        print(("  {}: {}".format(k, items)))
    print('WFBR RULES')
    for index, (lhs,rhs) in enumerate(grammar):
        if wfbr[index]:
            print(("  {} → {}".format(lhs or '⊤', " ".join(rhs))))

def followup(k, seed_lookahead, item):
    if item in seed_lookahead:
        return seed_lookahead[item]
    else:
        # The default resolution
        sym = grammar[item[0]][0]
        lookahead = set(follow_syms[k][sym])
        vlookahead = set(follow_vsyms[k][sym])
        for seeditem in follow_seeds[k][sym]:
            lookahead.update(seed_lookahead[seeditem])
        if (item in wfbs[k]) or wfbr[item[0]]:
            if len(vlookahead) > 0:
                lookahead.add('wfb')
            return lookahead
        else:
            return lookahead | vlookahead

def previous(items):
    for rule,index in items:
        yield (rule, index-1)

lr_mapping = [(0, frozenset([None]))]
lr_index = dict((s,i) for i,s in enumerate(lr_mapping))
lr_tabs = []
lr_conflicts = {}

for mapping in lr_mapping:
    k = mapping[0]
    tab = {}
    lr_tabs.append(tab)
    assert 1 + len(vectors[k]) == len(mapping)
    seed_lookahead = dict(list(zip(vectors[k], mapping[1:])))
    for sym, j in shifts[k]:
        to_mapping = (j,) + tuple(
            frozenset(followup(k, seed_lookahead, s_item))
            for s_item in previous(vectors[j]))
        flags = 0
        if sym in valigns[k]:
            if sym in nvaligns[k]:
                sys.stderr.write("error: VALIGN conflict at {} {}\n".format(k, sym))
                exit_status = 1
            else:
                flags |= 4
        wfb  = False
        nwfb = False
        for (rule, index) in previous(vectors[j]):
            if wfbr[rule] and index + 1 == len(grammar[rule][1]):
                wfb = True
            else:
                if (rule,index) in wfbs[k]:
                    wfb = True
                if (rule,index) in nwfbs[k]:
                    nwfb = True
        if wfb:
            if nwfb:
                sys.stderr.write("error: WFB conflict at {} {}\n".format(k, sym))
                exit_status = 1
            else:
                flags |= 2
        if to_mapping in lr_index:
            tab[sym] = (flags, lr_index[to_mapping])
        else:
            tab[sym] = (flags, len(lr_mapping))
            lr_index[to_mapping] = len(lr_mapping)
            lr_mapping.append(to_mapping)
    had_conflicts = []
    for item in reductions[k]:
        for sym in followup(k, seed_lookahead, item):
            action = (1, item[0])
            if sym not in tab:
                tab[sym] = action
            else:
                if (mapping,sym) in lr_conflicts:
                    lr_conflicts[(mapping,sym)].append(item)
                elif tab[sym][0] == 1:
                    lr_conflicts[(mapping,sym)] = [
                        (tab[sym][1], len(grammar[tab[sym][1]][1])),
                        item ]
                    had_conflicts.append(sym)
                else:
                    lr_conflicts[(mapping,sym)] = (
                        list(previous(vectors[lr_mapping[tab[sym][1]][0]]))
                        + [item])
                    had_conflicts.append(sym)
    if len(had_conflicts) > 0:
        sys.stderr.write('LR conflicts: {}\n'.format(mapping))
        for sym in had_conflicts:
            print_itemset('  {}'.format(sym), lr_conflicts[(mapping,sym)],
                sys.stderr)
            if tab[sym][0] != 1:
                sys.stderr.write("  {}: shift to {}\n".format(sym,
                    lr_mapping[tab[sym][1]][0]))

if parser_flavor == 'lr':
    if python_output is not None:
        with open(python_output, 'w') as fd:
            pw = pprint.PrettyPrinter(indent=2, stream=fd)
            fd.write("state = ")
            pw.pprint(lr_tabs)
            fd.write("rstate = ")
            pw.pprint([(lhs, len(rhs)) for lhs,rhs in grammar])
            fd.write("\nkeywords = ")
            pw.pprint(list(keywords))
            fd.write("\nlexemes = ")
            pw.pprint(list(lexemes))
elif parser_flavor == 'lalr':
    lalr_tabs = [{} for _ in seed_itemsets]
    for i, vec in enumerate(lr_mapping):
        row = lalr_tabs[vec[0]]
        for key, action in list(lr_tabs[i].items()):
            if action[0] == 1:
                rw_action = action
            else:
                to = lr_mapping[action[1]][0]
                rw_action = (action[0], to)
            if key not in row:
                row[key] = rw_action
            else:
                assert row[key] == rw_action, (
                    "LALR table collision"
                    "\nstate: {}"
                    "\nrow[key]: {}"
                    "\nrw_action: {}"
                    ).format(vec[0], row[key], rw_action)
    if python_output is not None:
        with open(python_output, 'w') as fd:
            pw = pprint.PrettyPrinter(indent=2, stream=fd)
            fd.write("state = ")
            pw.pprint(lalr_tabs)
            fd.write("rstate = ")
            pw.pprint([(lhs, len(rhs)) for lhs,rhs in grammar])
            fd.write("\nkeywords = ")
            pw.pprint(list(keywords))
            fd.write("\nlexemes = ")
            pw.pprint(list(lexemes))

sys.exit(exit_status)

# Actually the WFB-lexemes probably don't do anything bad.
#bad_wfb = set()
#for point in wfb_constraints:
#    sym = after_dot(point)
#    if sym in lexemes:
#        bad_wfb.add(sym)
#
#if len(bad_wfb) > 0:
#    exit_status = 1
#    sys.stderr.write(
#        "warning: WFB-constrained lexemes\n".format()
#        "   {}\n".format(",".join(map(repr,sorted(bad_wfb)))))
#    # They may confuse the follow-set buildup
#    # Because we continue from here,
#    # it's better to remove the bad constraints.
#    for point in bad_wfb:
#        wfb_constraints.discard(point) 