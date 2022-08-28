# https://github.com/MikeDevice/first-follow

from typing import List
from pprint import pprint

rules = [
  { 'left': 'S', "right": [ 'A', 'C', 'B' ] },
  { 'left': 'S', "right": [ 'C', 'b', 'b' ] },
  { 'left': 'S', "right": [ 'B', 'a' ] },
  { 'left': 'A', "right": [ 'd', 'a' ] },
  { 'left': 'A', "right": [ 'B', 'C' ] },
  { 'left': 'B', "right": [ 'g' ] },
  { 'left': 'B', "right": [ 'ϵ' ] },
  { 'left': 'C', "right": [ 'h' ] },
  { 'left': 'C', "right": [ 'ϵ' ] }
]

firstSets = {}
followSets = {}
isNoTerm = lambda item:item.isupper()

def getSet(dict,key)->set:
    if key not in dict:
        dict[key] = set()
    return dict[key]


# set_:         旧的目标fristSet|followSet
# items:        右侧项集(follow会算递减子集)
# additionSet:  两种情况不同, firt->[ϵ], follow->右侧完整项集
def collectSet(set_:set,items:List[str],additionSet:List[str])->set:
    # 下面的continue和break模仿的是js的every语义
    for idx,item in enumerate(items):
        # 如非终接符 循环处理
        if isNoTerm(item):
            item_first_set = getSet(firstSets,item)
            set_ = set_.union( [sym for sym in item_first_set if sym != 'ϵ'] ) 
            # 如果这个ϵ能一直串接下去
            if 'ϵ' in item_first_set:
                # 后面还有字符继续
                if len(items) > idx + 1 and items[idx + 1]: 
                    continue
                # 后面没有字符，对first集就加上ϵ
                set_ = set_.union( additionSet )
            # 这里不能省, 出现过bug !!!
            else:
                break                   
        # 如终接符 只取一个
        else:
            set_ = set_.union( [item] ) 
            break
    return set_

def makeFirstSets():
    isSetChanged:bool = True
    while isSetChanged:
        isSetChanged = False
        for rule in rules:
            left,right = rule['left'],rule['right']
            firstSet = getSet(firstSets,left)
            firstSet = collectSet( firstSet, right, ['ϵ'] )
            if len( firstSets[left] ) != len( firstSet ):
                firstSets[left] = firstSet
                isSetChanged = True
    return firstSets

def makeFollowSets():
    getSet(followSets,rules[0]['left']).add('$') # 为起始项添加 '$'

    isSetChanged:bool = True
    while isSetChanged:
        isSetChanged = False
        for rule in rules:
            left,right = rule['left'],rule['right']
            for idx,item in enumerate(right):
                if not isNoTerm(item): continue
                followSet = getSet(followSets,item)

                if idx + 1 < len(right):
                    temp = collectSet( followSet , right[idx+1:], getSet(followSets,left) ) #注意slice语义
                else:
                    temp = getSet(followSets,left)
                followSet = followSet.union( temp )

                if len( followSets[item] ) != len( followSet ):
                    followSets[item] = followSet
                    isSetChanged = True
    return followSets                

makeFirstSets()
pprint(firstSets)
makeFollowSets()
pprint(followSets)