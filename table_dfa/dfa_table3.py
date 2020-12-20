""" 
dfa描述，在语言{0...1}中,含 '01'序列合法
目标: 编译生成dfa表: 
    language: {'0','1'}
    parttern: '01'
=> 类似下面结果:
    1. pattern_index下标为key,充当状态
    2. lang_char为输入,与pattern_char比较，相同进入下一状态parttern_index + 1, 不同原地不变
    dfa = {
        0: {'0':1,'1':0},
        1: {'0':1,'1':2}
        //下面还可以添加一个结束的伪状态
        2: {'0':2,'1': 2}
    }    
"""

""" 
TODO:
1. 学习nfa2dfa
2. 扩充字符集，变成字符串查找
3. regexp
4. lexer
"""

""" 单一字符输入的状态变化
parttern_index: current state
pattern_char: current pattern char
lang_char: current input lang char
"""
def make_transition(pattern_index,pattern_char,lang_char):
    if pattern_char == lang_char:
        return {lang_char:pattern_index+1}
    else:
        return {lang_char:pattern_index}

""" 
构造状态转换表，生成器的核心
lang_set： 语言字符表， pattern: 待匹配的模式 
"""
def compile_dfa(lang_set,pattern):
    result = {}
    for pattern_index,pattern_char in enumerate(pattern):
        result_item = {pattern_index:{}}
        for lang_index,lang_char in enumerate(lang_set):
            iter_item = make_transition(pattern_index,pattern_char,lang_char) 
            result_item[pattern_index].update(iter_item) #update充当merge
        result.update(result_item)
    return result

def getNextState(currentState,input):
    return dfa[currentState][input]

def dfa_accept(dfa,input):
    current_state = 0 #初始状态，以0始
    for index,c in enumerate(input):
        current_state = getNextState(current_state,c)
        if(current_state == 2): #NOTE: 结束状态，这里len(parten + 1)  == 3
            print("首次匹配结尾位置{0}".format(index))
            return True
    return False    

# ---------------------------------------------------------------------
#  测试 
# ---------------------------------------------------------------------
if __name__ == "__main__":
    dfa = compile_dfa('01','01')
    print(dfa_accept(dfa,"0110"))
    print(dfa_accept(dfa,"1110"))

    dfa = compile_dfa('abcdefghijklmnopqrstuvwxyz','ab')
    print(dfa_accept(dfa,"ab"))
    print(dfa_accept(dfa,"ba"))
