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

*) A -> αBβ : { FIRST(β) - ϵ } ⊆ FOLLOW(B) # FIXME 这里需要first传递么?
*) A -> αB  : FOLLOW(A) ⊆ FOLLOW(B)

xxx FUCK 这句不是上面两个的合并说法么! xxx  => NOTE 可能不多余
*) A -> αBβ : FIRST(β) contains ϵ:  { FIRST(β) – ϵ } U FOLLOW(A) ⊆  FOLLOW(B)
"""

""" 示例文法1:
    S -> ACB | Cbb | Ba
    A -> da  | BC
    B -> g   | ϵ
    C -> h   | ϵ
""" 

""" first集
FIRST(S) = { d, g, h, b, a, Є}
FIRST(A) = { d, g, h, Є }
FIRST(B) = { g , Є }
FIRST(C) = { h , Є }
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
    # 含有key的右部:
    key_right_l = [item for item in noterm_right if key in item] # ['ACB', 'Ba', 'BC']
    
    # NOTE v1版本: 先忽略重复出现的非终结符产生式如 aBB
    for key_r in key_right_l:
        # 如果key在最后: 找出对应左部 递归求左部follow
        if key == key_r[-1]:
            left_key = get_left(key_r)
            left_res = follow_v1(left_key)
            res = res.union(left_res)
        else:
            # 如果key在倒2且最后为终结符: 直接加入
            if len(key_r) >= 2 and key_r[-1].islower() and key_r[-2] == key:  # >=2 判断貌似多余
                res.add(key_r[-1])
            # 普通不在最后: 求后续first => 疑问??? 这里紧邻后续必须有ϵ么???
            elif key_r[-1] != key :
                key_idx = key_r.index(key)
                # 如果下一个是终结符(调试出来的)
                if key_r[key_idx+1].islower():
                    res.add(key_r[key_idx+1])
                # 如果下一个不是终结符
                else:
                    # BUG: 这里如果出现了ϵ，应该需要循环|递归传递
                    next_res = first_v3(key_r[key_idx+1],grammer)
                    if 'ϵ' in next_res:
                        
                        # FIXME 这块的逻辑还是有问题 -- 
                        # left_key = get_left(key_r)
                        # left_res = follow_v1(left_key)
                        # res = res.union(left_res)

                        next_res.remove('ϵ')

                    res = res.union(next_res)
    return res

# res = follow_v1('A')
# print(res)


""" 尝试TODO:
Follow集的计算就相对first集稍微难一点：follow集的意义是寻找所要求字符的下一个字符可能产生的集合，所以寻找follow集应从产生式的右边进行寻找。
1. 在产生式的右边找到相应的字符，假设紧跟其后的是一个终结符，那么该终结符就是所要求的follow集；
2. 假设跟在其后的是一个非终结符，那么需要判断该非终结符是否可以为空：
    2.1 假如可以为空，那么将该产生式的左边的follow集加入到寻找集合当中，因为假如该非终结符为空的话，那么需要寻找产生这个非终结符的产生式左边的非终结符，因为产生式左边的非终结符的follow集就有可能是该非终结符的follow集；
        * 问题: 这里的空，是局部空还是空到最后?
    2.2 假如不为空，那么寻找该非终结符的first集，并将结果加入到搜索集合当中。
3.直到不再有非终结符产生，找到所有的终结符，计算结束。
"""

def follow_v2(key):
    if key == "S": return {"$"}
    res = set()
    # 含有key的右部:
    key_right_l = [item for item in noterm_right if key in item] # ['ACB', 'Ba', 'BC']
    
    # NOTE v1版本: 先忽略重复出现的非终结符产生式如 aBB
    for key_r in key_right_l:
        # 如果key在最后: 找出对应左部 递归求左部follow
        if key == key_r[-1]:
            left_key = get_left(key_r)
            left_res = follow_v2(left_key)
            res = res.union(left_res)
        else:
            # 如果key在倒2且最后为终结符: 直接加入
            if len(key_r) >= 2 and key_r[-1].islower() and key_r[-2] == key:  # >=2 判断貌似多余
                res.add(key_r[-1])
            # 普通不在最后: 求后续first => 疑问??? 这里紧邻后续必须有ϵ么???
            elif key_r[-1] != key :
                key_idx = key_r.index(key)
                # 如果下一个是终结符(调试出来的)
                if key_r[key_idx+1].islower():
                    res.add(key_r[key_idx+1])
                # 如果下一个不是终结符
                else:

                    # NOTE 尝试这里如果出现了ϵ，应该需要循环下一个, 对follow_a有改善，但结果还是不正确 
                    # BUG: 不加这循环结果少了，加了就多了个d
                    for key_idx in range(key_idx,len(key_r)):
                        # next_res = first_v3(key_r[key_idx+1],grammer)
                        next_res = first_v3(key_r[key_idx],grammer)
                        if 'ϵ' in next_res:
                            next_res.remove('ϵ')
                            res = res.union(next_res)

                            # 这个倒是能强行加上 '$'
                            if key_idx == len(key_r) -1  and get_left(key_r) == 'S':
                                res.add('$')
                        else:
                            break

    return res

res = follow_v2('A')
print(res)


