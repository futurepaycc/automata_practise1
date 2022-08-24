# https://www.geeksforgeeks.org/conversion-from-nfa-to-dfa/
# https://viterbi-web.usc.edu/~breichar/teaching/2011cs360/NFAtoDFA.p

""" 
nfa描述，在语言{0...1}中,以01结尾的序列合法
"""

""" 
NFA状态说明(现在还未转换为dfa):
目标状态使用集合表示
下面程序中用NFA_state表示nfa的基本状态
state_set表示目标状态集

TODO:
正则表达式生成NFA转移表: NFA状态转移表需要由正则表达式生成，而不能像DFA一样穷取生成，因为NFA已经是无穷的了
ab
a|b
a*b
生成转移表
"""
NFA={
    'q0': {'0':{'q0','q1'}, '1':{'q0'}},
    'q1': {'1':{'q2'}}
}
NFA_INIT='q0'
NFA_FINAL='q2'

# 下面代码一句不能少
def NFA_accept(NFA_table,input):
    NFA_state_set = {NFA_INIT} #为了下面迭代将初始状态包装成初始状态集合
    # NOTE 本质是一颗树的分支遍历
    for input_char in input:
        next_sate_set = set()
        for NFA_state in NFA_state_set: #这个内部循环，表达每个状态路径都走一遍
            try:
                #因为一个input_char只应该取一次目标状态集, 这个其实只是if else的语法糖
                #初始netState_set为空，取一下，取到了就不取了
                next_sate_set = next_sate_set | NFA_table[NFA_state][input_char] #self.delta[state][a]看成两部分: self.delta[state] 当前状态， [a] 作用于a输入
            except KeyError: pass
        NFA_state_set = next_sate_set
    if NFA_FINAL in NFA_state_set: #接受判断，有路径到终态，判断为true
        return True
    return False

# ---------------------------------------------------------------------
#  测试: 以01结尾的序列合法
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print(  NFA_accept(NFA,"010")   )
    print(  NFA_accept(NFA,"11")    )
    print(  NFA_accept(NFA,"1101")  )
    print(  NFA_accept(NFA,"1111")  )