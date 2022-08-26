""" 
first集测试1:

first集 :  对非终结X, 即为由其定义出发可以派生出(直接可达(含ϵ达))的终止符号集, 一般针对左项
follow集:  对非终结X, 后可以立即出现的终结符集, 一般针对右项

https://www.geeksforgeeks.org/follow-set-in-syntax-analysis/ (follow)
https://www.geeksforgeeks.org/first-set-in-syntax-analysis/  (first)
https://www.geeksforgeeks.org/program-calculate-first-follow-sets-given-grammar/ (c语言计算示例)
"""

""" 规则en:
1) FOLLOW(S) = { $ }   // where S is the starting Non-Terminal
2) If A -> pBq is a production, where p, B and q are any grammar symbols,
   then everything in FIRST(q)  except Є is in FOLLOW(B).
3) If A->pB is a production, then everything in FOLLOW(A) is in FOLLOW(B).
4) If A->pBq is a production and FIRST(q) contains Є, 
   then FOLLOW(B) contains { FIRST(q) – Є } U FOLLOW(A) 
"""

""" 规则中:
* Follow(S) = {$}
* 右项中对非终结α,所有ϵ可达的终结符, 不包含ϵ, 可以包含 $
"""


""" 示例文法1:
    S -> ACB | Cbb | Ba
    A -> da  | BC
    B -> g   | Є
    C -> h   | Є
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


def follow_v1(key):
    pass