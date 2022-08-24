""" 
'|' 符号: 是一个非确定状态机分支运算, 如果手写:
* 需要分支递归
"""


""" 
正则表达式也可以按语言定义: 朴素解析 组合: a+(b|c)

下面是正则表达式按文法定义, 可参考原regexp2.py
equ         ::= LETTER
plus        ::= LETTER+
star        ::= LETTER*
or_         ::= LETTER|LETTER

expr ::= LETTER
    | LBRACK + LETTER + RBRACK
    | equ
    | plus
    | or_
    | expr
    | LBRACK + expr + RBRACK

LETTER ::= 'a'|'b'|'c'
"""

"""目标 
a+(b+|c*)b
"""

from typing import List
from dataclasses import dataclass

# @dataclass
# class BasePattern:
#     lang_letter:str
#     re_letter:str

LANG_LETTER = ['a','b','c']
RE_LETTER = ['+','*','|']

""" 
最基础的模式组合: 
a+b
a+b*c
"""
def expr1(pattern_str):
    letters:List = list(pattern_str)
    # while ( cur=letters.pop() ) != None: #py3.8才支持赋值表达式: https://stackoverflow.com/questions/6631128/assign-variable-in-while-loop-condition-in-python

    res_patten_l:List = []

    cur_re_letter = None
    cur_lang_letter = None
    for letter in reversed(letters) : # 用栈的思路, 先处理结尾

        if letter in RE_LETTER:
            cur_re_letter = letter
            continue
        elif letter in LANG_LETTER:
            cur_lang_letter = letter
        else:
            raise Exception("不认识的字母")
        
        if cur_lang_letter:
            if cur_re_letter:
                res_patten_l.append( (cur_lang_letter,cur_re_letter) )
            else:
                res_patten_l.append( (cur_lang_letter,None) )
    return list( reversed(res_patten_l) )



# print( expr1("a+b*c") )


""" 
把 '|' 也当做组合处理1 => 忽略
a*|b
"""
def expr2(pattern):
    letters:List = list(pattern)

    res_patten_l:List = []

    cur_re_letter = None
    cur_lang_letter = None
    for letter in reversed(letters) : # 用栈的思路, 先处理结尾

        if letter in RE_LETTER:
            if letter != '|':
                cur_re_letter = letter
            continue
        elif letter in LANG_LETTER:
            cur_lang_letter = letter
        else:
            raise Exception("不认识的字母")
        
        if cur_lang_letter:
            if cur_re_letter:
                res_patten_l.append( (cur_lang_letter,cur_re_letter) )
            else:
                res_patten_l.append( (cur_lang_letter,None) )
    return list( reversed(res_patten_l) )


# print( expr2( "a*|b" ) )
# print( expr2( "a*|b|c" ) )



""" 
把 '|' 也当做组合处理2 => 逆波兰
a*|b => [((a,'*'),(b,None),|)]
"""
def expr3(pattern):
    letters:List = list(pattern)

    res_patten_l:List = []

    cur_re_letter = None
    cur_lang_letter = None
    for letter in reversed(letters) : # 用栈的思路, 先处理结尾

        if letter in RE_LETTER:
            if letter != '|':
                cur_re_letter = letter
            continue
        elif letter in LANG_LETTER:
            cur_lang_letter = letter
        else:
            raise Exception("不认识的字母")
        
        if cur_lang_letter:
            if cur_re_letter:
                res_patten_l.append( (cur_lang_letter,cur_re_letter) )
            else:
                res_patten_l.append( (cur_lang_letter,None) )
    return list( reversed(res_patten_l) )


print( expr3( "a*|b" ) )
print( expr3( "a*|b|c" ) )