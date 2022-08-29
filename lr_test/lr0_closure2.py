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

# ------------------------------------------------------------------------p1: 递归计算closure并inplace更新到res中

def createProductionSets(GRAMMAR_RULES):
    CURSOR_SYM = "∙"
    nterms = ["S'","S","B"]

    all_sts = {}

    """ 
    动机: 想让closure函数无副作用, 同时减少外界参数传入
    技术问题: 设置res=[]做为默认参数时，结果完全不同，外界还必须传入空List
    TODO: 调研python引用传递在递归情况下的问题，暂时传参并使用python的list+语义
    """
    def closure(rules,next_sym,res):
        for rule in rules:
            left,right = rule["left"],rule["right"]
            if left == next_sym:
                res.append(  {"left":left,"right":[CURSOR_SYM] + right} )
                # 如果右侧首是非终结，要递归拿到所有
                if right[0] in nterms:
                    res = res + closure(rules,right[0],[])
        return res

    # ------------------------------------------------------------------------p2: 计算初始状态
    def create_st0(rules):
        first_rule = rules[0]
        left0,right0 = first_rule["left"],first_rule["right"]
        res =  [{"left":left0,"right":[CURSOR_SYM] + right0}] 
        next_sym = right0[0]
        res = res + closure(rules[1:],next_sym,[])
        return res

    
    st0 = create_st0(GRAMMAR_RULES)
    # def _test_create_st0():
    #     st0_hand = [
    #         {"left":"S'","right":["∙","S"]},
    #         {"left":"S","right":["∙","B","B"]},
    #         {"left":"B","right":["∙","a","B"]},
    #         {"left":"B","right":["∙","b"]},
    #     ]
    #     res = create_st0(rules)
    #     assert( st0_hand == res )
    # _test_create_st0()
    # ------------------------------------------------------------------------p3: 由一个状态项出发，推导出新状态
    all_sts[0] = st0
    current_sts_idx = 0

    def move_cursor(rule_right:list):
        rule_right = rule_right[:]   #copy
        cursor_indx = rule_right.index(CURSOR_SYM)
        del rule_right[cursor_indx]
        rule_right.insert(cursor_indx+1,CURSOR_SYM)
        return cursor_indx + 1,rule_right

    def check_add_st(res):
        # NOTE 使用nolocal才可以修改闭包环境
        nonlocal current_sts_idx  
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
                # 如果没有移到最后，---采用create_st0类似逻辑---，递归构造其它closure状态
                # 加入全局状态后最否要排重???
                if right[-1] != CURSOR_SYM:
                    next_sym = right[new_cursor_index + 1]
                    # 下一个终结符: 和上面结束一样直接添加为新状态
                    # 下一个非终结符: 递归找左部
                    if next_sym in nterms:
                        res = res + closure(rules[1:],next_sym,[])
                check_add_st(res)

    # ------------------------------------------------------------------------p4: 推导至 项目集规范族 不再变化为止
    gen_all_sts(GRAMMAR_RULES,st0)
    prev_lenth = 1  #从初始状态第2项开始往下
    while True:
        new_length = len(all_sts.keys())
        if new_length > prev_lenth:
            for key in range(prev_lenth,new_length):
                gen_all_sts(GRAMMAR_RULES,all_sts[key])
            prev_lenth = new_length
        else:
            break
    # pprint(all_sts)
    return all_sts

# 封装了规范项目集
productionSets = createProductionSets(G2)
pprint(productionSets)

# TODO: 尝试使用项目集直接进行文法分析
# * 尝试外部做分析表
# * 尝试将分析表移入原有逻辑
# * 使用其它文法验证