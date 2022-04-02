# https://www.geeksforgeeks.org/conversion-from-nfa-to-dfa/
# https://viterbi-web.usc.edu/~breichar/teaching/2011cs360/NFAtoDFA.p

# %%
import pandas as pd
from io import StringIO
from graphviz import Digraph
from IPython.display import display, HTML
# %%
""" 
nfa描述，在语言{0,1}中,以01结尾的序列合法
TODO: 由基础正则表达式生成状态转移表再组合
    a*
    a|b
"""

# 这个就是正则语言|FA的核心(注意:一个状态也是集合，便于计算)
NFA_table={
    'q0': {'0':{'q0','q1'}, '1':{'q0'}},
    'q1': {'1':{'q2'}}
}
NFA_INIT='q0'
NFA_FINAL='q2'

# %%  绘图 
dot = Digraph()
dot.attr(rankdir='LR')
# 普通状态
dot.attr('node',shape='circle')
dot.node('q0')
dot.node('q1')
# 终结状态
dot.attr('node',shape='doublecircle')
dot.node('q2')
# 边
dot.edge('q0','q0',label='0,1')
dot.edge('q0','q1',label='0')
dot.edge('q1','q2',label='1')
dot

# %% 绘表
st_table_sio = StringIO("""
s;      0;          1
q0;     {q0,q1};    {q0}
q1;     ϕ;          {q2}
""")
df = pd.read_csv(st_table_sio,sep=";")
display(HTML(df.to_html(index=False)))

# %% 这个应该是自底向上算法
def NFA_accept(NFA_table,input):

    # 外层输入迭代
    current_NFA_state_set = {NFA_INIT}              #对于一次匹配，状态集初始化一次
    for input_char in input:

        # 对于一个输入字符的内层状态迭代
        # 将输入作用于 当前'可能状态集', 得到 下一步'可能状态集'
        next_sate_set = set()
        for current_NFA_state in current_NFA_state_set:
            try:
                # 右侧为 求并集运算
                # self.delta[state][a]看成两部分: self.delta[state] 当前状态， [a] 作用于a输入
                next_sate_set = next_sate_set | NFA_table[current_NFA_state][input_char] 
            except KeyError: 
                pass
        current_NFA_state_set = next_sate_set       #保存下一个输入的可选状态(这里只需保存一步，有点hmm的意思)

    # 循环结束后的 '可能状态集' 如何含有 '终结结点' 即为匹配成功
    if NFA_FINAL in current_NFA_state_set: #接受判断，有路径到终态，判断为true
        return True
    return False

# ---------------------------------------------------------------------
#  测试: 以01结尾的序列合法
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print(  NFA_accept(NFA_table,"01")   )
    # print(  NFA_accept(NFA_table,"010")   )
    # print(  NFA_accept(NFA_table,"11")    )
    # print(  NFA_accept(NFA_table,"1101")  )
    # print(  NFA_accept(NFA_table,"1111")  )