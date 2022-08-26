""" 
first集测试1:

first集 :  对非终结X, 即为由其定义出发可以派生出(直接可达(含ϵ达))的终止符号集, 一般针对左项
follow集:  对非终结X, 后可以立即出现的终结符集, 一般针对右项

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



""" 示例文法1:
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


""" 示例2
S -> ACB | Cbb | Ba
A -> da | BC
B -> g | Є
C -> h | Є

计算过程: 
FIRST(S) = FIRST(ACB) U FIRST(Cbb) U FIRST(Ba)
         = { d, g, h, b, a, Є}
FIRST(A) = { d } U FIRST(BC) 
         = { d, g, h, Є }
FIRST(B) = { g , Є }
FIRST(C) = { h , Є }
"""


from typing import List,Set

# ------------------------------------------------------------------------p1: 版本1
grammer1 = {
    "A":['da','BC'],
    "B":['g','ϵ'],
    "C":['h','ϵ']
}

def first_v1(key):
    ritems:List[str] = grammer1[key]
    res = set()

    # NOTE 这里嵌套循环 + 递归 如何表达啊!, 感觉不直观，不确定啊
    for item_seq in ritems:
        # 如果首项是小写=> 终结符或ϵ, 直接添加不再循环
        if item_seq[0].islower():
            res.add( item_seq[0] )
        # 首项大写非终解符, 因为第一个可能直接只是ϵ的非终接符，不排除它
        else:
            for item in item_seq:
                if item.isupper():
                    child_res = first_v1( item )
                    res = res.union( child_res )
                    # key: 如果当前这个不含ϵ不进行下一个
                    if 'ϵ' not in child_res:
                        break
    return res


def _test_v1():
    res = first_v1('A')
    print(res)    
            
# ------------------------------------------------------------------------p1: 版本2
grammer2 = {
    "S":["Cbb","ACB","Ba" ],
    "A":['da','BC'],
    "B":['g','ϵ'],
    "C":['h','ϵ']
}

# NOTE ‘S’的结果与示例不一致，加上了重复add逻辑，解决了，代码自己快看不懂了!
# 思路: 三层嵌套有点多，可以考虑数据结构扁平点吧
def first_v2(key):
    ritems:List[str] = grammer2[key]
    res = set()

    # NOTE 这里嵌套循环 + 递归 如何表达啊!, 感觉不直观，不确定啊
    for item_seq in ritems:
        # 如果首项是小写=> 终结符或ϵ, 直接添加不再循环
        if item_seq[0].islower():
            res.add( item_seq[0] )
        # 首项大写非终解符,循环
        else:
            # 因为第一个可能直接只是ϵ的非终接符，不排除它
            for item in item_seq:
                # key2: 这里不怕重复,靠set语义吧
                if item.islower():
                    res.add(item)
                else:
                    child_res = first_v2( item )
                    res = res.union( child_res )
                    # key1: 如果当前这个非终结符不含ϵ不进行下一个，断链
                    if 'ϵ' not in child_res:
                        break
    return res

def _test_v2():
    res = first_v2('B')
    assert( res == {'g', 'ϵ'} )

    res = first_v2('A')
    assert( res == {'h', 'ϵ',  'd', 'g'} )

    res = first_v2('S')
    assert( res == {'h', 'ϵ', 'a', 'd', 'b', 'g'} )    

if __name__ == "__main__":
    _test_v2()