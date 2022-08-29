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

""" 状态化, 初始状态
S' -> ∙ S
S  -> ∙ B B 
B  -> ∙ a B 
B  -> ∙ b
"""


CURSOR_SYM = "∙"
nterms = ["S'","S","B"]
terms  = ["a","b"]

# ---------------------------test2: 尝试嵌套字典存储, 可以整体判断相等性
st0_hand = [
    {"left":"S'","right":["∙","S"]},
    {"left":"S","right":["∙","B","B"]},
    {"left":"B","right":["∙","a","B"]},
    {"left":"B","right":["∙","b"]},
]

def build_st0(rules):
    first_rule = rules[0]
    left0,right0 = first_rule["left"],first_rule["right"]
    res =  [] 

    res.append({"left":left0,"right":[CURSOR_SYM] + right0})

    def recClosure(rules,right0):
        for rule in rules:
            left,right = rule["left"],rule["right"]
            if left == right0[0]:
                res.append(  {"left":left,"right":[CURSOR_SYM] + right} )

                # 如果右侧首是非终结，要递归拿到所有
                if right[0] in nterms:
                    recClosure(rules,right)
    recClosure(rules[1:],right0)
    return res

def _test_build_st0():
    res = build_st0(G2)
    print(res)
    assert( st0_hand == res )



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


# TODO 整合前面st0构建逻辑并统一
# ✓ 1 有inplace修改，结果不正确!
# ✓ 2 状态空间搜索不完整，应该搜到结果集不在变化为止, 也就是每个∙要挪到最后
def gen_all_sts(rules,st0):
    for stat_rule_item in st0:
        left,right = stat_rule_item['left'],stat_rule_item['right']

        if right[-1] != CURSOR_SYM:
            new_cursor_index,right = move_cursor(right)
            # 如果∙已经移到最后，这个状态完成
            res = [ {"left":left,"right":right} ]
            if right[-1] == CURSOR_SYM:
                # all_sts[current_sts_idx] = [ {"left":left,"right":right} ]
                # res = [ {"left":left,"right":right} ]
                pass

            # 如果没有移到最后，---采用build_st0类似逻辑---，递归构造其它closure状态
            # 加入全局状态后最否要排重???
            else:
                next_sym = right[new_cursor_index + 1]
                # 下一个终结符: 和上面结束一样直接添加为新状态
                if next_sym in terms:
                    pass
                # 下一个非终结符: 递归找左部
                else:
                    # 递归处理逻辑 NOTE 与首状态处理重复
                    def recClosure(rules,next_sym):
                        for rule in rules:
                            left,right = rule["left"],rule["right"]
                            if left == next_sym:
                                res.append(  {"left":left,"right":[CURSOR_SYM] + right} )

                                # 如果右侧是非终结，要递归拿到所有
                                if right[0] in nterms:
                                    recClosure(rules,right)
                    recClosure(rules[1:],next_sym)
                # all_sts[current_sts_idx] = res
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


"""  移进状态变换
当前状态: B -> ∙ b 读入 b
切换状态: B -> b ∙ 
归约检查: 后无符可归约至左部B
"""

""" 归约流程(假设已有表)
* B -> b ∙ 已可归约
* 状态栈、符号栈双弹出
* 符号栈压入新归约符号
* 此时栈不平，找新的栈顶状态、栈顶符号查goto表，查到新状态
* 新状态压入状态栈
* 重新开始输入进符号栈
"""