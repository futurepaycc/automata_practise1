""" 
实现有基本的正则表达式构造, 普通编程方法，不引入状态机结构

equ         ::= a
plus        ::= a+
start       ::= a*
or_         ::= a|b

参考:
https://deniskyashif.com/2019/02/17/implementing-a-regular-expression-engine/
"""

# lambda无法指定type hint: https://stackoverflow.com/questions/40989808/how-to-specify-argument-type-in-lambda
# equ = lambda pattern:str,input:str : pattern == input

equ = lambda pattern,input : input.startswith(pattern)


def _test_equ():
    assert( equ("a","a") )
    assert( equ("a","ab") )
    assert( not equ("a","b") )
    assert( not equ("a","ba") )
# _test_equ()

""" 
英语:
numerator   被除数
denominator 除数
quotient    商
remainder   余数
"""

""" 
算法:
* 整除
* 每段相等
"""
def plus(pattern,input):
    if not input or len(input) == 0: return False

    pattern = pattern[:-1] #去除末尾加号
    quotient,reminder = divmod( len(input),len(pattern) )

    result = True
    if reminder == 0:
        for idx in range(quotient):
            if input[len(pattern)*idx:len(pattern)*(idx+1)] != pattern:
                result = False
    return result

def _test_plus():
    p1,in1 = "a+",""
    assert( not plus(p1,in1) )

    p1,in1 = "a+","a"
    assert( plus(p1,in1) )

    p1,in1 = "a+","aa"
    assert( plus(p1,in1) )

    p1,in1 = "a+","aaaaaaaaaaaaaa"
    assert( plus(p1,in1) )

# _test_plus()


def star(pattern,input):
    # NOTE 除了这行外与plus完全相同
    if input and len(input) == 0: return True

    pattern = pattern[:-1] #去除末尾加号
    quotient,reminder = divmod( len(input),len(pattern) )

    result = True
    if reminder == 0:
        for idx in range(quotient):
            if input[len(pattern)*idx:len(pattern)*(idx+1)] != pattern:
                result = False
    return result    

def _test_star():
    p1,in1 = "a*",""
    assert( star(p1,in1) )

    p1,in1 = "a*","a"
    assert( plus(p1,in1) )

    p1,in1 = "a*","aa"
    assert( plus(p1,in1) )

    p1,in1 = "a*","aaaaaaaaaaaaaa"
    assert( plus(p1,in1) )    

# _test_star()


def or_(pattern,input):
    p_list = pattern.split("|")
    for p in p_list:
        if equ(p,input):
            return True
    return False


def _test_or_():
    p1,in1 = "a|b","a"
    assert( or_(p1,in1) )   

    p1,in1 = "a|b","c"
    assert(not or_(p1,in1) )   

# _test_or_() 