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

""" 规则en:
*) FOLLOW(S) = { $ }
*) If A -> αBβ is a production, where α, B and β are any grammar symbols,
   { FIRST(β) - ϵ } ⊆ FOLLOW(B)
*) If A-> αBβ is a production and FIRST(β) contains ϵ, --> 你妹: 如何操作?
   then FOLLOW(B) contains { FIRST(β) – ϵ } U FOLLOW(A) 
*) If A->αB is a production, then everything in FOLLOW(A) ⊆ FOLLOW(B)
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

from typing import List,Set

grammer2 = {
    "S":['ACB','Cbb','Ba'],
    "A":['da','BC'],
    "B":['g','ϵ'],
    "C":['h','ϵ']
}

from first1 import grammer2,first_v2


""" 计算思路:
* 先合并所有的右部


"""

def follow_v1(key):
    pass
