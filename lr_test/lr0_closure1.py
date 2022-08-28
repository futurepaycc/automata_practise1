# https://www.cnblogs.com/standby/p/6792837.html
# https://www.bilibili.com/video/BV18U4y1m7Dg 


# https://www.geeksforgeeks.org/compiler-design-slr1-parser-using-python/
# https://www.bilibili.com/video/BV1P4411e7gm?p=18 (12:00)


from pprint import pprint

""" 本例目标: lr0的action_goto表构造

"""



""" 概念
* item(项目): 加了 ∙ 的右部，代表分析状态
* 待归约: 有多个可归约路径

"""

""" 测试文法
S -> B B 
B -> a B 
B -> b
"""
G1 = [
    {"left":"S","right":["B","B"]},
    {"left":"B","right":["a","B"]},
    {"left":"B","right":["b"]},
]

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

# G3 = [
#     {"left":"S'","right":["∙","S"]},
#     {"left":"S","right":["∙","B","B"]},
#     {"left":"B","right":["∙","a","B"]},
#     {"left":"B","right":["∙","b"]},
# ]

# ---------------------------test1: 这种字串存储不方便
# st0_hand = set([
#     "S'->∙S",
#     "S->∙BB",
#     "B->∙aB",
#     "B->∙b",
# ])
CURSOR_SYM = "∙"
nterms = ["S'","S","B"]
terms  = ["a","b"]

# # 参数，文法G2 rules
# def build_st0(rules):
#     first_rule = rules[0]
#     left0,right0 = first_rule["left"],first_rule["right"]
#     res = set( [ left0 + "->" + CURSOR_SYM  + "".join(right0)] )

#     def recClosure(rules,right0):
#         for rule in rules:
#             left,right = rule["left"],rule["right"]
#             if left == right0[0]:
#                 res.add(  left + "->" + CURSOR_SYM + "".join(right) )

#                 # 如果右侧首是非终结，要递归拿到所有
#                 if right[0] in nterms:
#                     recClosure(rules,right)
#     recClosure(rules[1:],right0)
#     return res

# def _test_build_st0():
#     res = build_st0(G2)
#     print(res)
#     assert( st0_hand == res )



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



""" 迭代生成所有状态
S' -> ∙ S       -> S ∙ 
S  -> ∙ B B     -> B ∙ B    -> B B ∙ 
B  -> ∙ a B     -> a ∙ B    -> a B ∙ 
B  -> ∙ b       -> b ∙ 
"""

""" 求闭包
定义:  一个状态集， 应该是结果分析表中的一行
圆点后:
    * 非终结，找以前为左部所有产生式状态, 此过程递归，直到原点后没有非终结
    * 终结, 直接拿来

示例: closure(∙ S)

∙ S -> ∙ B B 
    -> ∙ a B
      | ∙ b
"""


""" 求项目集规范族
Item0 = CLOSURE({S' --> .S}) = {S' --> .S，S --> .BB，B --> .aB，B --> .b}
Item1 =GO(Item0,S) = CLOSURE({S' --> S.}) = {S' --> S.}
Item2 = GO(Item0,B) = CLOSURE({S --> B.B}) = {S --> B.B，B --> .aB，B --> .b}
Item3 = GO(Item0,a) = CLOSURE({B --> a.B}) = {B --> a.B，B --> .aB，B --> .b}
Item4 = GO(Item0,b) = CLOSURE({B --> b.}) = {B --> b.}
至此Item0已经遍历完，开始遍历下一个，由于Item1圆点已经到达末尾，所以跳过Item1。
Item5 = GO({Item2,B) = CLOSURE({S --> BB.}) = {S --> BB.}
由于 GO(Item2,a) 和 GO(Item2,b) 重复，所以去掉。
Item6 = GO(Item3,B) = CLOSURE({B --> aB.}) = {B --> aB.}
由于 GO(Item3,a) 和 GO(Item3,b) 重复，所以去掉。
至此，项目集闭包不再增加，所以项目集规范族构造完毕！
https://www.cnblogs.com/standby/p/6792837.html
"""

all_sts = {}
st0 = build_st0(G2)
all_sts[0] = st0
current_sts_idx = 0

def move_cursor(rule_right:list):
    cursor_indx = rule_right.index(CURSOR_SYM)
    del rule_right[cursor_indx]
    rule_right.insert(cursor_indx+1,CURSOR_SYM)
    return cursor_indx + 1

# TODO 整合前面st0构建逻辑并统一
# BUG: 1 有inplace修改，结果不正确!
# BUG: 2 状态空间搜索不完整，应该搜到结果集不在变化为止, 也就是每个∙要挪到最后
def gen_all_sts(rules,st0):
    global current_sts_idx
    for stat_rule_item in st0:
        left,right = stat_rule_item['left'],stat_rule_item['right']

        current_sts_idx += 1
        if right[-1] != CURSOR_SYM:
            new_cursor_index = move_cursor(right)
            # 如果∙已经移到最后，这个状态完成
            if right[-1] == CURSOR_SYM:
                all_sts[current_sts_idx] = [ {"left":left,"right":right} ]

            # 如果没有移到最后，---采用build_st0类似逻辑---，递归构造其它closure状态
            # 加入全局状态后最否要排重???
            else:
                res = [ {"left":left,"right":right} ]
                next_sym = right[new_cursor_index + 1]
                # 下一个终结符: 和上面结束一样直接添加为新状态
                if next_sym in terms:
                    pass
                # 下一个非终结符: 递归找左部
                else:
                    # 递归处理逻辑
                    def recClosure(rules,next_sym):
                        for rule in rules:
                            left,right = rule["left"],rule["right"]
                            if left == next_sym:
                                res.append(  {"left":left,"right":[CURSOR_SYM] + right} )

                                # 如果右侧是非终结，要递归拿到所有
                                if right[0] in nterms:
                                    recClosure(rules,right)
                    recClosure(rules[1:],next_sym)
                all_sts[current_sts_idx] = res


gen_all_sts(G2,st0)

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