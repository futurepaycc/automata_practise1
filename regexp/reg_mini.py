"""
说明: 用来学习、研究，函数式编程、四则运算、表达式优先级处理,这个作者行啊
来源: https://github.com/darius/sketchbook/blob/master/regex/integrated1.py 
问题: 括号组合实现有bug{ match('(a|b)*c', 'caac') } 、代码不易读
优点: 代码少，无依赖
特点: 综合性，复杂性极高，用来学习参考，可暂不深咎

TODO:
模拟每个函数的输入，了解每个函数作用
"""

# ---------------------------------------------------------------------
#  辅助函数: 貌似都是函数式的，基本返回lambda和function
# ---------------------------------------------------------------------

# 接受状态
def accepting_state(c): return set()

# 中间状态( parse结果元素 )
def expecting_state(char, k): return lambda c: k(set()) if c == char else set()

# 开始节点
def state_node(state): return lambda seen: set([state]) #返回一个lambda函数: def k(seen): return set([state]), 操，没有用到seen啊

# 并联节点
def alt_node(k1, k2):  return lambda seen: k1(seen) | k2(seen)

def loop_node(k, make_k):
    def loop(seen):
        if loop in seen: return set()
        seen.add(loop)
        return k(seen) | looping(seen)
    looping = make_k(loop)
    return loop

# ---------------------------------------------------------------------
#  解析: (四则运算、计算表达式解析算法?), 嵌套函数类似js闭包
#  结果: 状态集，每个状态好像是个 expecting_state 函数(import inspect \n inspect.getsource(result.pop()))
# ---------------------------------------------------------------------
def parse(re):
    par_ch_list = list(re)

    # 解析表达式
    # kaleidoscope中的优先级算法，precedence初始为0, k为state_node函数返回的lamda闭包: set([state])
    def parse_expr(precedence, k):
        rhs = parse_factor(k)
        while par_ch_list:
            if par_ch_list[-1] == '(': break #结尾不能是 '('
            cur_prec = 2 if par_ch_list[-1] == '|' else 4 # 结尾为'|'则当前优先级为2,否则为4?
            if cur_prec < precedence: break #当前优先级不能传入优先级
            if chomp('|'):
                rhs = alt_node(parse_expr(cur_prec + 1, k), rhs)
            else:
                rhs = parse_expr(cur_prec + 1, rhs)
        return rhs

    # 解析基本元素
    # k为state_node函数返回的lamda闭包: set([state])
    def parse_factor(k):
        if not par_ch_list or par_ch_list[-1] in '|(':
            return k
        elif chomp(')'):
            e = parse_expr(0, k)
            assert chomp('(')
            return e
        elif chomp('*'):
            return loop_node(k, lambda loop: parse_expr(6, loop))
        else:
            return state_node(expecting_state(par_ch_list.pop(), k))

    # 处理 (、)、*、|，语义?
    # 结尾是(、)、*、|，从parttern_char_list弹出一个字符，并返回返回判断结果
    def chomp(token):
        matches = (par_ch_list and par_ch_list[-1] == token)
        if matches: par_ch_list.pop()
        return matches

    k = parse_expr(0, state_node(accepting_state))
    assert not par_ch_list
    return k(set())

# ---------------------------------------------------------------------
#  运行 
# ---------------------------------------------------------------------
def run(states, s):
    for c in s:
        states = set.union(*[state(c) for state in states])
    return accepting_state in states

def match(re, s): return run(parse(re), s)

# ---------------------------------------------------------------------
#  测试 
# ---------------------------------------------------------------------
if __name__ == "__main__":
    result = parse('abc')
    print( parse('ab') )
    
    # print( match('a*', 'aaa') )
    # print( match('a|b', 'c') )
    # print( match('(a|b)*c', 'aaac') )
