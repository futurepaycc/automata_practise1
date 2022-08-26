""" 
first集测试1:

first集 :  对非终结X, 即为由其定义出发可以派生出(直接可达(含ϵ达))的终止符号集
follow集:  对非终结X, 后可以立即出现的终结符集

https://www.geeksforgeeks.org/first-set-in-syntax-analysis/  (first)
https://www.geeksforgeeks.org/follow-set-in-syntax-analysis/ (follow)
https://www.geeksforgeeks.org/program-calculate-first-follow-sets-given-grammar/ (c语言计算示例)
"""

""" 规则:
If x is a terminal, then FIRST(x) = { ‘x’ }
If x-> Є, is a production rule, then add Є to FIRST(x).
If X->Y1 Y2 Y3...Yn is a production, 
FIRST(X) = FIRST(Y1)
If FIRST(Y1) contains Є then FIRST(X) = { FIRST(Y1) – Є } U { FIRST(Y2) }
If FIRST (Yi) contains Є for all i = 1 to n, then add Є to FIRST(X).
"""



""" 测试文法1:
A -> da | BC
B -> g | ϵ
C -> h | ϵ

计算过程: first(A)
* first(A) = first(da) U (first(BC))
           = d U g U first(ϵC)
           = d U g U ϵ U first(C)
           = d U g U ϵ U h U ϵ
           = {d,g,ϵ,h}
"""

from typing import List,Set

grammer = {
    "A":['da','BC'],
    "B":['g','ϵ'],
    "C":['h','ϵ']
}

# 暂示完成
def first_v1(key):
    ritems:List[str] = grammer[key]
    res = set()

    for item_seq in ritems:
        item_first = item_seq[0]
        # 小写终接符号直接放入
        if item_first.islower():
            res.add(item_first)
        # 非终接符情况:
        # * 如果不包含ϵ,就找它的首终结符
        # * 如果包含ϵ, TODO: 向前看并增加内层循环!
        #       * 增加ϵ_continue_flag
        else:
            child_first = first_v1(item_first)
            res = res.union( child_first  )  #union not inplace
    return res

res = first_v1('A')
print(res)