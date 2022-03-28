"""
说明: 用来学习、研究，函数式编程、四则运算、表达式优先级处理,这个作者行啊
来源: https://github.com/darius/sketchbook/blob/master/regex/integrated1.py 
问题: 括号组合实现有bug{ match('(a|b)*c', 'caac') } 、代码不易读
优点: 代码少，无依赖
特点: 综合性，复杂性极高，函数式编程抽象层级多，用来学习参考，可暂不深咎
一些参考: 
    * Thompson 算法
    * https://github.com/darius/sketchbook/blob/master/regex/ (同目录下的其它文件等)
        * nfa.py
        * nfa_loopsloop.py

TODO:
* 先理解透彻常规NFA生成式的正则处理regexp1.py
* 查看原仓库简化文件，分离函数式与NFA的关注点
* 手工化简，对每个模式进行精简代码分析，如只看'ab'模式的构造

理解: 
    * 本文件是集成文件，原作者也是分步实现各种匹配方式并结合的
    * 这里的每个state_λ函数是个闭包，包装了参数为状态，lambda自身为运算，相当于一个对象实例
    * set展开时是不是用到了函子和范畴的概念?
"""

# ---------------------------------------------------------------------
#  辅助函数: 貌似都是函数式的，基本返回lambda和function
# ---------------------------------------------------------------------
import inspect 

# 接受状态
def accepting_state_λ(c): 
    return set()

# 中间状态( parse结果元素 )
# def expecting_state(char, k): return lambda c: k(set()) if c == char else set()
def expecting_state(p_char,k):
    def expecting_state_λ(in_char):
        # 运行时(匹配时)代码
        # 这里的k可以是右一个模式字串的expecting_state_λ，形成函数链表|栈
        # p='ab'外部看似一个expecting_state_λ,内则是一个expecting_state_λ串
        # res = k(set()) if in_char == p_char else set()
        if in_char == p_char:
            res = k(set())
        else:
            res = set()
        return res
    return expecting_state_λ

# 状态节点, 没有用到seen啊, 就是简单的将状态算子再包wrapp一层成通用状态算子么 => 抽像类?
# def state_node(state): return lambda seen: set([state]) 
def state_node_wrapper(state_λ):
    def state_node_inner(seen):
        res = set([state_λ])
        return res
    return state_node_inner

# | 操作
# def alt_node(k1, k2):  return lambda seen: k1(seen) | k2(seen)
def alt_node(k1,k2):
    def alt_node_λ(seen):
        res = k1(seen) | k2(seen)
        return res
    return alt_node_λ

# * 操作
# k => node_λ, make_k => parse_expr_λ
def loop_node(k, make_k):
    def loop_node_λ(seen):
        if loop_node_λ in seen: 
            return set()
        seen.add(loop_node_λ)
        res = k(seen) | looping(seen)
        return res
    looping = make_k(loop_node_λ)
    return loop_node_λ

# ---------------------------------------------------------------------
# 解析顺序: 从右向左，自顶向下
# 输入: re => 模式字符串
# 返回: state_λ_set => 状态处理函数集合
# ---------------------------------------------------------------------
def parse(re):
    p_char_list = list(re)

    # 递归解析表达式, parse_factor <--> parse_factor 会互调
    # kaleidoscope中的优先级算法，precedence初始为0, k为state_node函数返回的lamda闭包: set([state])
    # 优先级: )=>0, |=> 4, *=>6, default => 2
    def parse_expr(precedence, k):
        # 处理单个字符, 
        rhs = parse_factor(k) 
        # FIXME 循环递归?
        while p_char_list: 
            if p_char_list[-1] == '(': break #结尾不能是 '(' ??, 是不是匹配成功的意思?
            cur_prec = 2 if p_char_list[-1] == '|' else 4 # 结尾为'|'则当前优先级为2,否则为4?
            if cur_prec < precedence: break #当前优先级高,中止循环，开始处理?
            if chomp('|'):
                rhs = alt_node(parse_expr(cur_prec + 1, k), rhs)
            else:
                rhs = parse_expr(cur_prec + 1, rhs)
        return rhs

    # 解析基本元素: factor => char | (***)
    # k为state_node函数返回的lamda闭包: set([state])
    # p_char_list为模式字符列表
    def parse_factor(k):
        if not p_char_list or p_char_list[-1] in '|(':
            return k
        # 递归处理 '()'的内容
        elif chomp(')'):
            e = parse_expr(0, k)
            assert chomp('(')
            return e
        # 这里的　嵌套　+ 递归　好乱
        elif chomp('*'):
            parse_expr_λ = lambda loop: parse_expr(6, loop)
            return loop_node(k, parse_expr_λ)
        else:
            res = state_node_wrapper(expecting_state(p_char_list.pop(), k))
            return res

    # 判断结尾是(、)、*、|字符，若是就弹出
    def chomp(token):
        matches = (p_char_list and p_char_list[-1] == token)
        if matches: 
            p_char_list.pop()
        return matches

    k = parse_expr(0, state_node_wrapper(accepting_state_λ))
    assert not p_char_list
    # 这里传参似乎无意义， state_node_inner会忽略参数啊
    res = k(set())
    return res

# ---------------------------------------------------------------------
#  运行 
# ---------------------------------------------------------------------
def run(state_λ_set, text):
    for char in text:
        # 这里也在解决state_λ链，解开一个少一个
        state_λ_set = set.union(*[state_λ(char) for state_λ in state_λ_set])
    return accepting_state_λ in state_λ_set    #有一个匹配就算成功

# 外部接口
def match(re, text):
    #set不能index,只能pop
    state_λ_set = parse(re)                #生成状态表 {expecting_state_inner,accepting_state_λ}
    return run(state_λ_set, text)          #用状态表匹配，看能否发现终态

# ---------------------------------------------------------------------
#  测试 
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # result = parse('abc')
    # print( parse('ab') )
    
    # print( match('a', 'a') )
    print( match('ab', 'ab') )
    # print( match('a|b', 'c') )
    # print( match('a*', 'aaa') )
    # print( match('(a|b)*c', 'aaac') )
