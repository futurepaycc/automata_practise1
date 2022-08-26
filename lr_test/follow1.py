""" 
first集测试1:

first集 :  对非终结X, 即为由其定义出发可以派生出(直接可达(含ϵ达))的终止符号集, 一般针对左项
follow集:  对非终结X, 后可以立即出现的终结符集, 一般针对右项

first集:   某个非终结符展开后，可能出现在第一位的所有终结符的集合
follow集:  当这个非终结符被规约之后，可以紧跟在它后面的终结符的集合

https://www.bilibili.com/video/BV17K4y1a72M?p=2 (TODO: b站视频计算)
https://www.geeksforgeeks.org/follow-set-in-syntax-analysis/ (follow)
https://www.geeksforgeeks.org/first-set-in-syntax-analysis/  (first)
https://www.geeksforgeeks.org/program-calculate-first-follow-sets-given-grammar/ (c语言计算示例)
"""
from typing import List,Set
from first1 import first_v3
""" 规则:
*) FOLLOW(S) = { $ }
*) A -> αBc : c ⊆ FOLLOW(B)

*) A -> αBβ : FIRST(β) contains ϵ: { FIRST(β) - ϵ } ⊆ FOLLOW(B)
*) A -> αB  : FOLLOW(A) ⊆ FOLLOW(B)

xxx FUCK 这句不是上面两个的合并说法么! xxx
*) A -> αBβ : FIRST(β) contains ϵ:  { FIRST(β) – ϵ } U FOLLOW(A) ⊆  FOLLOW(B)
"""

""" 示例文法1:
    S -> ACB | Cbb | Ba
    A -> da  | BC
    B -> g   | ϵ
    C -> h   | ϵ
""" 

""" follow集:
    FOLLOW(S) = { $ }
    FOLLOW(A) = { h, g, $ }
    FOLLOW(B) = { a, $, h, g }
    FOLLOW(C) = { b, g, $, h }        
"""
grammer = {
    "S":['ACB','Cbb','Ba'],
    "A":['da','BC'],
    "B":['g','ϵ'],
    "C":['h','ϵ']
}

""" 计算思路:
* 先合并所有的右部
"""

# 所有右部
all_right_part = [ item for l_inner in  list( grammer.values() ) for item in l_inner  ] # ! 双层产生式先循环外层

# 含有非终结符的右部
noterm_right = [item for item in all_right_part if any( char.isupper() for char in item )]

def get_left(r_value):
    for key,values in grammer.items():
        if r_value in values:
            return key
# TODO: 未完成
def follow_v1(key):
    if key == "S": return {"$"}
    res = set()
    # 含有key的右部: BUG: 
    key_right_l = [item for item in noterm_right if key in item] # ['ACB', 'Ba', 'BC']
    
    # NOTE v1版本: 先忽略重复出现的非终结符产生式如 aBB
    for key_r in key_right_l:
        # 如果key在最后: 找出对应左部 递归求左部follow
        if key == key_r[-1]:
            left_key = get_left(key)
            left_res = follow_v1(left_key)
            res = res.union(left_res)
        else:
            # 如果key在倒2且最后为终结符: 直接加入
            if len(key_r) >= 2 and key_r[-1].islower() and key_r[-2] == key:  # >=2 判断貌似多余
                res.add(key_r[-1])
            # 普通不在最后: 求后续first => 疑问??? 这里紧邻后续必须有ϵ么???
            elif key_r[-1] != key :
                key_idx = key_r.index(key)
                next_res = first_v3(key_r[key_idx+1],grammer)
                if 'ϵ' in next_res:
                    next_res.remove('ϵ')
                res = res.union(next_res)
    return res

follow_v1('B')

