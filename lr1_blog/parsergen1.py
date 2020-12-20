# -*- coding: utf-8 -*-
grammar = [
    (None, ['program']),
    ('program', []),
    ('program', ['program', 'declaration']),
    ('declaration', ['varDecl']),
    ('declaration', ['constDecl']),
    ('declaration', ['statement']),
]
lexemes = ['varDecl', 'constDecl', 'statement']
wfb_constraints = []
valign_constraints = []

def print_grammar():
    for lhs, rhs in grammar:
        print(("{} → {}".format(lhs or '⊤', " ".join(rhs))))
    
def print_item(prefix, xxx_todo_changeme ):
    (rule, index) = xxx_todo_changeme
    lhs, rhs = grammar[rule]
    print(("{}{} → {}".format(prefix, lhs or '⊤',
        " ".join(rhs[:index] + ['∘'] + rhs[index:]))))

def print_itemset(index, items):
    prefix = "{}: ".format(index)
    for item in items:
        print_item(prefix, item)
        prefix = " " * len(prefix)

def after_dot(xxx_todo_changeme1):
    (rule, index) = xxx_todo_changeme1
    lhs, rhs = grammar[rule]
    if index < len(rhs):
        return rhs[index]

def predict(items):
    prediction = set(items)
    wfb = set()
    valign = set()
    cconflicts = []
    p = len(prediction)
    while len(items) > 0:
        this = items.pop()
        has_wfb = this in wfb_constraints or this in wfb
        has_valign = this in valign_constraints or this in valign
        sym = after_dot(this)
        for index, (lhs,rhs) in enumerate(grammar):
            if sym == lhs and sym is not None:
                prediction.add((index, 0))
                if p < len(prediction):
                    p = len(prediction)
                    items.append((index,0))
                    if has_wfb:
                        wfb.add((index,0))
                    if has_valign:
                        valign.add((index,0))
                else:
                    if ((index,0) in wfb) ^ has_wfb:
                        cconflicts.append(('wfb', (index,0)))
                    if ((index,0) in valign) ^ has_valign:
                        cconflicts.append(('valign', (index,0)))
    return prediction, wfb, valign, cconflicts

def partition(items, wfb, valign, cconflicts):
    groups = {}
    modes = {}
    for item in items:
        sym = after_dot(item)
        mode = (int(item in wfb) << 1) | int(item in valign)
        if sym is not None:
            item = (item[0], item[1]+1)
        try:
            groups[sym].append(item)
            if modes[sym] != mode:
                cconflicts.append(('shift+valign+wfb', sym))
        except KeyError as _:
            groups[sym] = [item]
            modes[sym] = mode
    return [(sym, frozenset(items), modes[sym])
        for sym, items in list(groups.items())]

itemsets = [ frozenset([(0,0)]) ]
itemsets_index = dict((s,i) for i,s in enumerate(itemsets))
vectors = []
full_itemsets = []
shifts = []
reductions = []
for k, itemset in enumerate(itemsets):
    vectors.append(tuple(itemset))
    pset, wfb, valign, cconflicts = predict(list(itemset))
    full_itemsets.append(pset)
    k_shifts = {}
    k_reductions = set()
    for sym, items, mode in partition(pset, wfb, valign, cconflicts):
        if sym is None:
            k_reductions.update(items)
        else:
            try:
                j = itemsets_index[items]
            except KeyError as _:
                j = len(itemsets)
                itemsets_index[items] = j
                itemsets.append(items)
            k_shifts[sym] = (j, mode)
    shifts.append(k_shifts)
    reductions.append(k_reductions)
    if len(cconflicts) > 0:
        print("conflict in this itemset:")
        print_itemset(k, itemset)
        print(cconflicts)

#print shifts
#print reductions

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

def first_lexemes():
    symbols = dict()
    routes = set()
    for sym in lexemes:
        symbols[sym] = set([sym])
    for lhs, rhs in grammar:
        if lhs not in symbols:
            symbols[lhs] = set([])
    for lhs, rhs in grammar:
        for rhsN in rhs:
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

def after_sym(xxx_todo_changeme2):
    (rule,index) = xxx_todo_changeme2
    lhs, rhs = grammar[rule]
    if index+1 < len(rhs):
        return rhs[index+1]

def follow_lexemes(seedset, full_itemset):
    symbols = {}
    seeds = {}
    routes = set()
    for item in full_itemset:
        sym0 = after_dot(item)
        if sym0 not in symbols:
            symbols[sym0] = set()
            seeds[sym0] = set()
    for rule,index in full_itemset:
        lhs,rhs = grammar[rule]
        has_wfb = (rule,index) in wfb_constraints
        if index < len(rhs):
            rhs0 = rhs[index]
            k = index+1
            for k in range(index+1, len(rhs)):
                if (rule,k) in valign_constraints:
                    symbols[rhs0].add('wfb')
                else:
                    symbols[rhs0].update(first[rhs[k]])
                if rhs[k] not in empty:
                    break
            if k == len(rhs):
                if (rule,index) in seedset:
                    seeds[rhs0].add((rule,index))
                else:
                    routes.add((lhs, rhs0))
    rep = True
    while rep:
        rep = False
        for lhs, sym in routes:
            n = len(symbols[lhs])
            symbols[lhs].update(symbols[rhs0])
            rep |= n < len(symbols[lhs])
            n = len(seeds[lhs])
            seeds[lhs].update(seeds[rhs0])
            rep |= n < len(seeds[lhs])
    return symbols, seeds

follow_syms = []
follow_seeds = []

for i in range(len(itemsets)):
    syms,seeds = follow_lexemes(itemsets[i], full_itemsets[i])
    follow_syms.append(syms)
    follow_seeds.append(seeds)
    #print i
    #print syms
    #print seeds

def followup(k, seed_lookahead, item):
    if item in seed_lookahead:
        return seed_lookahead[item]
    else:
        sym = grammar[item[0]][0]
        lookahead = set(follow_syms[k][sym])
        for seeditem in follow_seeds[k][sym]:
            lookahead.update(seed_lookahead[seeditem])
        return lookahead

fin_index = {}
fin_vectors = []
fin_tabs = []
conflicts = {}

def build_decision_table(k, *args):
    fin_index[(k,)+args] = tab_index = len(fin_vectors)
    fin_vectors.append((k,)+args)
    tab = {}
    fin_tabs.append(tab)
    assert len(vectors[k]) == len(args)
    seed_lookahead = dict(list(zip(vectors[k],args)))
    syms = follow_syms[k]
    seeds = follow_seeds[k]
    for sym, (j,mode) in list(shifts[k].items()):
        args = (j,) + tuple(
            frozenset(followup(k, seed_lookahead, (s_item[0], s_item[1]-1)))
            for s_item in vectors[j])
        if args in fin_index:
            tab[sym] = (0, fin_index[args], mode)
        else:
            tab[sym] = (0, build_decision_table(*args), mode)
    had_conflicts = []
    for reditem in reductions[k]:
        for sym in followup(k, seed_lookahead, reditem):
            action = ('reduce',
                grammar[reditem[0]][0],
                len(grammar[reditem[0]][1]),
                reditem[0])
            if sym in tab:
                if (k,sym) in conflicts:
                    conflicts[(k,sym)].append(action)
                else:
                    conflicts[(k,sym)] = [tab[sym], action]
                    had_conflicts.append((k,sym))
            else:
                tab[sym] = action
    if len(had_conflicts) > 0:
        print(("Conflicts:".format(had_conflicts)))
        for cnf in had_conflicts:
            print((" {}: {}".format(cnf, conflicts[cnf])))
    return tab_index

build_decision_table(0, frozenset([None]))
if len(conflicts) > 0:
    print(fin_tabs)
    print(conflicts)
else:
    print(fin_tabs)
