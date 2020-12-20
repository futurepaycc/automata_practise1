# https://www.bilibili.com/video/BV1oE4116794?p=5 4:30

""" 
dfa描述，在语言{0...1}中,含 '01'序列合法
TODO:
1. 多次匹配(reset,save result_list)
2. 查找、生成成dfa_table算法
    根据base_text, pattern_生成笛卡尔积?
"""

dfa = {
    1: {'0':2,'1':1},
    2: {'0':2,'1':3},
    3: {'0':3,'1':3}
}
input = '111110'

def getNextState(currentState,input):
    return dfa[currentState][input]

def accept(dfa,input):
    current_state = 1 #1注意： 1.dfa的下标自1始, 这种语句块定义的是全局变量
    for index,c in enumerate(input):
        current_state = getNextState(current_state,c)
        if(current_state == 3):
            print("首次匹配结尾位置{0}".format(index))
            return True
    return False

print(accept(dfa,"0110"))
print(accept(dfa,"1110"))
