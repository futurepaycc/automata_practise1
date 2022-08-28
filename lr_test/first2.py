# https://www.geeksforgeeks.org/first-set-in-syntax-analysis/  (first)
from typing import List
from pprint import pprint

ENDING_SYM = None


rules = [
    {"left":"E", "right":["T","E'"]},
    {"left":"E'","right":["+","T","E'"]},
    {"left":"E'","right":[ENDING_SYM]},
    {"left":"T", "right":["F","T'"]},
    {"left":"T'","right":["*","F","T'"]},
    {"left":"T'","right":[ENDING_SYM]},
    {"left":"F", "right":["id"]},
    {"left":"F", "right":["(","E",")"]},
]    

firstSets = {}

# def isNoTerm(item): return item.isupper()

all_no_term = set([item['left'] for item in rules])
def isNoTerm(item): return item in all_no_term

def getSet(dict, key) -> set:
    if key not in dict:
        dict[key] = set()
    return dict[key]

# set_:         旧的目标fristSet
# items:        右侧项集
# additionSet:  [ϵ]
def collectFirstSet(firset: set, items: List[str], additionSet: List[str]) -> set:
    # 下面的continue和break模仿的是js的every语义
    for idx, item in enumerate(items):
        # 如非终接符 循环处理
        if isNoTerm(item):
            item_first_set = getSet(firstSets, item)
            firset = firset.union( [sym for sym in item_first_set if sym != ENDING_SYM] )
            # 如果这个ϵ能一直串接下去
            if ENDING_SYM in item_first_set:
                # 后面还有字符继续
                if len(items) > idx + 1 and items[idx + 1]:
                    continue
                # 后面没有字符，对first集就加上ϵ
                firset = firset.union(additionSet)
            else:
                break
        # 如终接符 只取一个
        else:
            firset = firset.union([item])
            break
    return firset

def makeFirstSets():
    isSetChanged: bool = True
    while isSetChanged:
        isSetChanged = False
        for rule in rules:
            left, right = rule['left'], rule['right']
            firstSet = getSet(firstSets, left)
            firstSet = collectFirstSet(firstSet, right, [ENDING_SYM])
            if len(firstSets[left]) != len(firstSet):
                firstSets[left] = firstSet
                isSetChanged = True

makeFirstSets()      
pprint(firstSets)          