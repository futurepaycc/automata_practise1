# https://github.com/MikeDevice/first-follow

""" 
follow集算法: 更多参考虎书，龙书太笼统
"""

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
predictSets = {}

isNoTerm = lambda item:item.isupper()

def getSet(dict,key)->set:
    if key not in dict:
        dict[key] = set()
    return dict[key]


# set_:         旧的目标fristSet
# items:        右侧项集
# additionSet:  [ϵ]
def collectFirstSet(firset:set,items:List[str],additionSet:List[str])->set:
    # 下面的continue和break模仿的是js的every语义
    for idx,item in enumerate(items):
        # 如非终接符 循环处理
        if isNoTerm(item):
            item_first_set = getSet(firstSets,item)
            firset = firset.union( [sym for sym in item_first_set if sym != 'ϵ'] ) 
            # 如果这个ϵ能一直串接下去
            if 'ϵ' in item_first_set:
                # 后面还有字符继续
                if len(items) > idx + 1 and items[idx + 1]: 
                    continue
                # 后面没有字符，对first集就加上ϵ
                firset = firset.union( additionSet )
            # 这里不能省, 出现过bug !!!
            else:
                break                
        # 如终接符 只取一个
        else:
            firset = firset.union( [item] ) 
            break
    return firset

def makeFirstSets():
    isSetChanged:bool = True
    while isSetChanged:
        isSetChanged = False
        for rule in rules:
            left,right = rule['left'],rule['right']
            firstSet = getSet(firstSets,left)
            firstSet = collectFirstSet( firstSet, right, ['ϵ'] )
            if len( firstSets[left] ) != len( firstSet ):
                firstSets[left] = firstSet
                isSetChanged = True
    # return firstSets

# item_followSet:       待更新的非终结符的follow集
# items:                右侧项集算递减子集
# additionSet:          follow->右侧完整项集
def collectFollowSet(item_followSet:set,sub_r_items:List[str],left_followSet:List[str])->set:
    # 下面的continue和break模仿的是js的every语义
    for idx,r_item in enumerate(sub_r_items):
        # 如非终接符 循环处理 (这个循环有递归的感脚)
        if isNoTerm(r_item):
            # 先加上下一项的first集
            item_first_set = getSet(firstSets,r_item)
            item_followSet = item_followSet.union( [sym for sym in item_first_set if sym != 'ϵ'] ) 

            # 如果上面计算的下项first集中有ϵ
            if 'ϵ' in item_first_set:
                # 后面还有字符继续
                if len(sub_r_items) > idx + 1 and sub_r_items[idx + 1]: 
                    continue
                # 后面没有字符，加上左部的followset
                item_followSet = item_followSet.union( left_followSet )
        # 如终接符 只取一个
        else:
            item_followSet = item_followSet.union( [r_item] ) 
            break
    return item_followSet

def makeFollowSets():
    getSet(followSets,rules[0]['left']).add('$') # 为起始项添加 '$'

    isSetChanged:bool = True
    # 外层循环: 相当于epoch，直到大轮次都没有任何变化才停止
    while isSetChanged:
        isSetChanged = False
        # 处理所有rule
        for rule in rules:
            left,right = rule['left'],rule['right']
            # 处理一条rule直至不变化
            for idx,item in enumerate(right):
                if not isNoTerm(item): continue
                left_followSet = getSet(followSets,left)

                item_followSet = getSet(followSets,item)
                if idx + 1 < len(right):
                    temp = collectFollowSet( item_followSet , right[idx+1:], left_followSet )
                else:
                    temp = left_followSet
                item_followSet = item_followSet.union( temp )

                if len( followSets[item] ) != len( item_followSet ):
                    followSets[item] = item_followSet
                    isSetChanged = True
    # return followSets                



# stat_predictSet:      产生式的预测分析集
# r_items:              右侧项集
# additionSet:          左部follow集
def collectPredictSet(stat_predictSet:set,r_items:List[str],left_followSet:List[str])->set:
    # 下面的continue和break模仿的是js的every语义
    for idx,r_item in enumerate(r_items):
        # 如非终接符 循环处理 (这个循环有递归的感脚)
        if isNoTerm(r_item):
            # 先加上下一项的first集
            item_first_set = getSet(firstSets,r_item)
            stat_predictSet = stat_predictSet.union( [sym for sym in item_first_set if sym != 'ϵ'] ) 

            # 如果上面计算的下项first集中有ϵ
            if 'ϵ' in item_first_set:
                # 后面还有字符继续
                if len(r_items) > idx + 1 and r_items[idx + 1]: 
                    continue
                # 后面没有字符，加上左部的followset
                stat_predictSet = stat_predictSet.union( left_followSet )
        # 如终接符 只取一个
        else:
            stat_predictSet = stat_predictSet.union( [r_item] ) 
            break
    return stat_predictSet

def makePredictSets():
    for ruleIndex,rule in enumerate(rules):
        left,right = rule['left'],rule['right']
        firstItem = right[0]
        set_ = set()

        if isNoTerm(firstItem):
            temp = collectPredictSet(set_,right,getSet(followSets,left))
            set_ = set_.union( temp )
        elif firstItem == 'ϵ':
            set_ = getSet(followSets,left)
        else:
            set_.add(firstItem)
        predictSets[str(ruleIndex+1)] = set_


makeFirstSets()
pprint(firstSets)
makeFollowSets()
pprint(followSets)
makePredictSets()
pprint(predictSets)