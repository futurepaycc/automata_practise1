# https://zhuanlan.zhihu.com/p/551197012
# https://github.com/AinsleySnow/Calculators/blob/master/tables/sets.py

# BUG: 结果不对，没有表示出空集

""" 
FIRST集:   某个非终结符展开后，可能出现在第一位的所有终结符的集合
FOLLOW集:  当这个非终结符被规约之后，可以紧跟在它后面的终结符的集合
"""


"""测试文法
S一CC
C一cC
 | d
"""

"""FOLLOW 集的求法，
1. 开始符号（比如上面的“S”）的 FOLLOW 集里面总有一个 EOF 符号。先把它放进去
2. 如果产生式形如A->αBβ,那就把 FIRST(β) 里除 ε 之外的所有符号都放到 FOLLOW(B) 里 
3. 如果产生式形如A->αB,或者虽形如A->αBβ, 但 FIRST(β) 中包含 ε，就把 FOLLOW(A) 中的符号全放到 FOLLOW(B) 中
"""

from typing import List
from copy import deepcopy # 这个记得加

"""测试文法
S一CC
C一cC
 | d
"""
nts = {
    '<S>' : [['<C>','<C>'],],
    '<C>' : [['"c"', '<C>'], ['"d"',]]
}
ts = ['"c"', '"d"'] 



""" 示例文法1:
    S -> ACB | Cbb | Ba
    A -> da  | BC
    B -> g   | Є
    C -> h   | Є
""" 
nts = {
    '<S>': [ ['<A>','<C>','<B>'],['<C>','"b"','"b"'],['<B>','"a"']],
    '<A>': [ ['"d"','"a"'],['<B>','<C>']],
    '<B>': [ ['"g"',] ],
    '<C>': [ ['"h"',] ]
}
ts = ['"a"','"b"','"d"','"g"','"h"']


def makechanging():
    length = None

    # 嵌套的函数——检查字典 d 中集合的长度是否发生变化。
    def changing(d: dict) -> bool:
        nonlocal length
        if not length:
            length = dict()
            for k in d.keys():
                length[k] = len(d[k])
            return True

        isChanging = False
        for k in d.keys():
            isChanging |= (length[k] != len(d[k]))
            length[k] = len(d[k])
        return isChanging

    return changing


def FirstSet(nts: dict, ts: List[str]) -> dict:
    # ts：终结符列表。终结符用 str 表示。
    # nts：非终结符及其对应的若干产生式体。
    # 这个字典的键为 str，表示具体的非终结符。
    # 值为列表的列表，存放对应的产生式体。
    # 比如键“C”对应的值可以是
    # [['"c"', '<C>'], ['"d"']]
    # 为了方便区分，我们把所有非终结符都用尖括号（“<>”）括起来。
    # 用双引号括起来的和没有被括起来的都是终结符。
    # 空串（ε）用 "" 表示。
    first = dict()
    # 初始化
    for (name, rules) in nts.items():
        first[name] = set()
    for terminal in ts:
        first[terminal] = {terminal}

    changing = makechanging()

    while changing(first):
        # 这两层 for 循环的作用是遍历所有产生式
        for (name, rules) in nts.items():
            for rule in rules:
                if rule != ['""',]:
                    rhs = deepcopy(first[rule[0]]) # rhs 是“right hand side”的缩写
                    rhs.discard('""')
                    # 先拷贝产生式箭头右侧第一个符号的 FIRST 集
                    # 之后遍历产生式右侧的所有符号
                    for i in range(0, len(rule) - 1):
                        if '""' not in first[rule[i]]: # 如果某个非终结符可以推出空串就继续循环
                            break
                        rhs |= first[rule[i + 1]]
                        rhs.discard('""')
                    else: # 如果上面的 for 循环正常终止就会跳到这里
                        if '""' in first[rule[-1]]:
                            rhs.add('""')
                else:
                    rhs = {'""'}
                # 最后，把本轮循环求出来的终结符集合和
                # 产生式头对应的 FIRST 集合合并到一起
                first[name] |= rhs

    return first


def FollowSet(nts: dict, first: dict, startsymbol: str) -> dict:
    # 初始化
    follow = dict()
    for (name, rules) in nts.items():
        follow[name] = set()
    if startsymbol:
        follow[startsymbol].add('eof')
        # 开始符号的 FOLLOW 集里总是有 eof。先把它放进去。
        # 其实龙书上用的是“$”。
        # 不过我觉得直接用“eof”会比用“$”看起来舒服一点。

    changing = makechanging()

    # 和上面一样，反复求 FOLLOW 集直到所有 FOLLOW 集都不再变化为止
    while changing(follow):
        for (name, rules) in nts.items():
            for rule in rules:
                trailer = deepcopy(follow[name])
                # 先初始化 trailer：相当于把 FOLLOW(A) 先存下来
                for i in range(len(rule) - 1, -1, -1):
                # 从右至左遍历产生式体中的符号
                    if rule[i][0] == '<': #“<>”括着的都是非终结符
                        follow[rule[i]] |= trailer 
                        # 如果最里层 for 循环的首轮迭代就调用这一行的话，
                        # 它能起到上面第三点的作用

                        # 以下的 if-else 语句对应上面的第二点
                        # 到了下一轮迭代就可以改 FOLLOW 集了
                        if '""' in first[rule[i]]:
                            trailer |= first[rule[i]]
                            trailer.discard('""')
                        else:
                            trailer = deepcopy(first[rule[i]])
                    else: # 否则就只修改 trailer，不修改其他非终结符的 FOLLOW 集
                        trailer = deepcopy(first[rule[i]])

    return follow

if __name__ == '__main__':
    # 不过，如果某个产生式可以产生空串（比如，消除了左递归之后的语法），
    # 这里要加上 '""'。虽然严格来说 ε 不算终结符，
    # 但是把它放到终结符列表里可以简化代码。

    first = FirstSet(nts, ts)
    print("first集:\t",first)
    follow = FollowSet(nts, first, '<S>')
    print("follow集:\t",follow)    