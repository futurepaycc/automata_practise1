# 参考:
# https://www.zhihu.com/column/c_1517250860593233921 (专栏)
# https://github.com/AinsleySnow/Calculators/blob/master/tables/LR0_items.py (代码库)

from pprint import pprint

""" TODO:
* 合并初始项集与普通项集计算
* 添加不同项集的状态转换, 完成移进、归约
* 制作成为分析表
"""

""" 增广
S' -> S
S  -> B B 
B  -> a B 
B  -> b
"""
G2 = [
    {"left":"S'","right":["S"]},
    {"left":"S","right":["B","B"]},
    {"left":"B","right":["a","B"]},
    {"left":"B","right":["b"]},
]

CURSOR_SYM = "∙"
nterms = ["S'","S","B"]
terms  = ["a","b"]
# ---------------------------test2: 尝试嵌套字典存储, 可以整体判断相等性


def recClosure(rules,next_sym,res):
    for rule in rules:
        left,right = rule["left"],rule["right"]
        if left == next_sym:
            res.append(  {"left":left,"right":[CURSOR_SYM] + right} )
            # 如果右侧首是非终结，要递归拿到所有
            if right[0] in nterms:
                recClosure(rules,right,res)

def build_st0(rules):
    first_rule = rules[0]
    left0,right0 = first_rule["left"],first_rule["right"]
    res =  [{"left":left0,"right":[CURSOR_SYM] + right0}] 
    next_sym = right0[0]
    recClosure(rules[1:],next_sym,res)
    return res

all_sts = {}
st0 = build_st0(G2)
all_sts[0] = st0
current_sts_idx = 0

def move_cursor(rule_right:list):
    rule_right = rule_right[:]   #copy
    cursor_indx = rule_right.index(CURSOR_SYM)
    del rule_right[cursor_indx]
    rule_right.insert(cursor_indx+1,CURSOR_SYM)
    return cursor_indx + 1,rule_right

def check_add_st(res):
    global current_sts_idx
    if res not in all_sts.values():
        current_sts_idx += 1
        all_sts[current_sts_idx] = res

def gen_all_sts(rules,st0):
    for stat_rule_item in st0:
        left,right = stat_rule_item['left'],stat_rule_item['right']
        if right[-1] != CURSOR_SYM:
            new_cursor_index,right = move_cursor(right)
            # 如果∙已经移到最后，这个状态完成
            res = [ {"left":left,"right":right} ]
            # 如果没有移到最后，---采用build_st0类似逻辑---，递归构造其它closure状态
            # 加入全局状态后最否要排重???
            if right[-1] != CURSOR_SYM:
                next_sym = right[new_cursor_index + 1]
                # 下一个终结符: 和上面结束一样直接添加为新状态
                # 下一个非终结符: 递归找左部
                if next_sym in nterms:
                    recClosure(rules[1:],next_sym,res)
            check_add_st(res)

# ---------------------------------------- 计算项目集规范族
gen_all_sts(G2,st0)
prev_lenth = 1
changed:bool = True
while changed:
    new_length = len(all_sts.keys())
    if new_length > prev_lenth:
        for key in range(prev_lenth,new_length):
            gen_all_sts(G2,all_sts[key])
        prev_lenth = new_length
    else:
        changed = False

pprint(all_sts)
