""" https://stackoverflow.com/questions/35272592/how-are-finite-automata-implemented-in-code """


""" 
状态转移图 -> 状态转移表 transition table

字符串查找的状态机 -> ac状态表

核心也是生成状态转移表
"""

""" 格式: 
key: 当前状态
value: 
    key: 输入
    value: 目标状态

 """

from pprint import pp

dfa = {0:{'0':0, '1':1},
       1:{'0':2, '1':0},
       2:{'0':1, '1':2}}

def accepts(transitions,initial,accepting,s):
    state = initial
    for c in s:
        state = transitions[state][c]
    return state in accepting       

if __name__ == "__main__":
   print( accepts(dfa,0,{0},'1011101') )
   print( accepts(dfa,0,{0},'10111011') )