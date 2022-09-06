# https://github.com/MikeDevice/first-follow

""" 
follow集算法: 更多参考虎书，龙书太笼统
说明:
原算法使用None判断，直接改成'ϵ'字符判断结果不一致 FIXME ??? 没有发现哪里影响判断语义了

NOTE 换了表达式文法后,first(E)计算错误!-> 原first集计算少了break，不能与js的every语义完全对应
"""

from typing import List
from pprint import pprint

ENDING_SYM = None


def build_first_follow_sets(rules:list):
    # TODO 改进初始成空set
    firstSets = {}
    followSets = {}
    predictSets = {}

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
                firset = firset.union(
                    [sym for sym in item_first_set if sym != ENDING_SYM])
                # 如果这个ϵ能一直串接下去
                if ENDING_SYM in item_first_set:
                    # 后面还有字符继续
                    if len(items) > idx + 1 and items[idx + 1]:
                        continue
                    # 后面没有字符，对first集就加上ϵ
                    firset = firset.union(additionSet)
                # 这里不能省, 出现过bug !!!
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
        # return firstSets

    # item_followSet:       待更新的非终结符的follow集
    # items:                右侧项集算递减子集
    # additionSet:          follow->右侧完整项集
    def collectFollowSet(item_followSet: set, sub_r_items: List[str], left_followSet: List[str]) -> set:
        # 下面的continue和break模仿的是js的every语义
        for idx, r_item in enumerate(sub_r_items):
            # 如非终接符 循环处理 (这个循环有递归的感脚)
            if isNoTerm(r_item):
                # 先加上下一项的first集
                item_first_set = getSet(firstSets, r_item)
                item_followSet = item_followSet.union(
                    [sym for sym in item_first_set if sym != ENDING_SYM])

                # 如果上面计算的下项first集中有ϵ
                if ENDING_SYM in item_first_set:
                    # 后面还有字符继续
                    if len(sub_r_items) > idx + 1 and sub_r_items[idx + 1]:
                        continue
                    # 后面没有字符，加上左部的followset
                    item_followSet = item_followSet.union(left_followSet)
            # 如终接符 只取一个
            else:
                item_followSet = item_followSet.union([r_item])
                break
        return item_followSet

    def makeFollowSets():
        getSet(followSets, rules[0]['left']).add('$')  # 为起始项添加 '$'

        isSetChanged: bool = True
        # 外层循环: 相当于epoch，直到大轮次都没有任何变化才停止
        while isSetChanged:
            isSetChanged = False
            # 处理所有rule
            for rule in rules:
                left, right = rule['left'], rule['right']
                # 处理一条rule直至不变化
                for idx, item in enumerate(right):
                    if not isNoTerm(item):
                        continue
                    left_followSet = getSet(followSets, left)

                    item_followSet = getSet(followSets, item)
                    if idx + 1 < len(right):
                        temp = collectFollowSet(
                            item_followSet, right[idx+1:], left_followSet)
                    else:
                        temp = left_followSet
                    item_followSet = item_followSet.union(temp)

                    if len(followSets[item]) != len(item_followSet):
                        followSets[item] = item_followSet
                        isSetChanged = True
        # return followSets

    # stat_predictSet:      产生式的预测分析集
    # r_items:              右侧项集
    # additionSet:          左部follow集
    def collectPredictSet(stat_predictSet: set, r_items: List[str], left_followSet: List[str]) -> set:
        # 下面的continue和break模仿的是js的every语义
        for idx, r_item in enumerate(r_items):
            # 如非终接符 循环处理 (这个循环有递归的感脚)
            if isNoTerm(r_item):
                # 先加上下一项的first集
                item_first_set = getSet(firstSets, r_item)
                stat_predictSet = stat_predictSet.union(
                    [sym for sym in item_first_set if sym != ENDING_SYM])

                # 如果上面计算的下项first集中有ϵ
                if ENDING_SYM in item_first_set:
                    # 后面还有字符继续
                    if len(r_items) > idx + 1 and r_items[idx + 1]:
                        continue
                    # 后面没有字符，加上左部的followset
                    stat_predictSet = stat_predictSet.union(left_followSet)
            # 如终接符 只取一个
            else:
                stat_predictSet = stat_predictSet.union([r_item])
                break
        return stat_predictSet

    def makePredictSets():
        for ruleIndex, rule in enumerate(rules):
            left, right = rule['left'], rule['right']
            firstItem = right[0]
            set_ = set()

            if isNoTerm(firstItem):
                temp = collectPredictSet(set_, right, getSet(followSets, left))
                set_ = set_.union(temp)
            elif firstItem == ENDING_SYM:
                set_ = getSet(followSets, left)
            else:
                set_.add(firstItem)
            predictSets[str(ruleIndex+1)] = set_

    makeFirstSets()
    # pprint(firstSets)
    makeFollowSets()
    # pprint(followSets)
    makePredictSets()
    # pprint(predictSets)

    return firstSets, followSets, predictSets



def isNoTerm(rules,item):
    all_no_term = set([item['left'] for item in rules])
    return item in all_no_term  

def build_ll1_table(rules,first,follow):
    all_left = set([item['left'] for item in rules])
    # all_right = [item['right'] for item in rules]
    all_right = set()
    for rule in rules: all_right = all_right.union(rule["right"])
    all_sym = all_left.union(all_right) 

    all_no_term = all_left
    all_term = all_sym.difference(all_no_term)

    all_term.remove(None)
    all_term.add("$")

    print(all_no_term)
    print(all_term)


""" 
LL(1)tabel构造算法: 《龙书,算法4.31》
* 建立二维表，行index为非终符，列index为终符含结束符$不含ϵ
* 一般: 得到每个产生式的右部的first集，用产生式左部作行坐标，frist集中元素纵坐标，将产生式(或序号)填入表格
* 特殊: 若产生式A->ϵ, 则求Follow(A)集, 然后在[A,follow集]坐标序列中填入产生式 A->ϵ
"""
from tabulate import tabulate

def build_ll1_table2(rules,firstSets,followSets):
    all_term  = ["id","+","*","(",")","$"]
    all_nterm = ["E","E'","T","T'",'F']

    table = {}
    for nterm in all_nterm: table[nterm] = ['']*len(all_term)

    for rule in rules:
        left,right = rule['left'],rule['right']
        right0 = right[0]

        if isNoTerm(rules,right0):
            cols = firstSets[right0]
        else:
            if right0 == ENDING_SYM:
                cols = followSets[left]
            else:
                cols = [right0]
        
        for col_str in cols:
            if right0 == ENDING_SYM:
                table[left][all_term.index(col_str)] = left + "->" + "ϵ"
            else:
                table[left][all_term.index(col_str)] = left + "->" + "".join(right)

    
    return table


def _print_ll1_table(table):
    all_term  = ["id","+","*","(",")","$"]
    res = tabulate( [ [k] + v for k, v in table.items() ], headers=["N\T"]+all_term, tablefmt='grid')
    print(res)  


def get_production_rule(rules,rule_str):
    left_str,right_str = rule_str.split("->")
    for rule in rules:
        left,right = rule['left'],rule['right']

        # 用None表示ϵ,tricky
        if right == [None]:
            right = ['ϵ']

        if left == left_str and "".join(right) == right_str:
            return rule


""" 
LL(1)预测表的主控算法:
https://www.geeksforgeeks.org/construction-of-ll1-parsing-table/
https://www.geeksforgeeks.org/ll1-parsing-algorithm/?ref=rp
"""
term  = ["id","+","*","(",")","$"]
nterm = ["E","E'","T","T'",'F']
def test_table(table,rules):
    # 输入: 这种括号不匹配没有报错, 已解决
    input = "id + id $".split()
    # 初始化栈: 加入这个'$' 对下面的while判断有点用
    stack = ['$','E']
    # 输入指针
    ip = 0

    print("输入句子:","".join(input)[:-1])

    # while len(stack) > 1 and input[ip] != '$':

    # 《编译器设计之路:程序3-2》书中有误，这里应该是 or  => 解决括号不匹配问题
    while len(stack) > 1 or input[ip] != '$':
        stack_top = stack[-1] # 栈顶符

        input_token = input[ip]

        # 只有分析到终结符才移动 输入指针 ???
        if stack_top in term or stack_top == '$':
            if stack_top == input_token:
                temp_t = stack.pop()
                print("debug: 匹配终结符号:\t",temp_t)
                ip+=1
            else:
                raise("句子语法错误")

        elif stack_top in nterm:
            if table[stack_top][term.index(input_token)] != '':
                temp_nt = stack.pop()
                # print("debug: 弹出中间非终结符号",temp_nt)

                # 将表格中的生成式字串转回rule
                rule_str = table[stack_top][term.index(input_token)]    # 表格中定义生成式字面串
                rule = get_production_rule(rules,rule_str)              # 将字面串映射回规则，便于分割复合符如E'

                print("debug: 应用生成式:\t",rule_str)

                # 将生成式右部反序压栈
                for sym in reversed(rule['right']):
                    if sym: #这里一定要排除None|ϵ 《编译器设计之路:程序3-2》
                        stack.append(sym)

            else:
                raise("句子语法错误")
    
    print("语法正确，处理成功")



""" 测试用表达式无左递归语法, 如何看出不回溯 ???
E  -> TE'
E' -> +TE' | ε                
T  -> FT'
T' -> *FT' | ε
F  -> id | (E)
"""
if __name__ == "__main__":
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

    first,follow,predict = build_first_follow_sets(rules)

    # pprint(first)
    # pprint(follow)
    # pprint(predict)
    
    # res = build_ll1_table(rules,first,follow)
    table = build_ll1_table2(rules,first,follow)

    _print_ll1_table(table)

    test_table(table,rules)

