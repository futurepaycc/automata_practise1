""" 
dfa描述，在语言{0...1}中,含 '01'序列合法
目标: 编译生成dfa表: 
    language: {'0','1'}
    parttern: '01'
=> 
    dfa = {
        1: {'0':2,'1':1},
        2: {'0':2,'1':3},
        3: {'0':3,'1':3}
    }    
"""

def make_transition(pattern_index,pattern_char,lang_char):
    if pattern_char == lang_char:
        return {lang_char:pattern_index+1}
    else:
        return {lang_char:pattern_index}

""" lang_set： 语言字符表， pattern: 待匹配的模式 """
def compile_dfa(lang_set,pattern):
    result = {}
    for pattern_index,pattern_char in enumerate(pattern):
        result_item = {pattern_index:{}}
        for lang_index,lang_char in enumerate(lang_set):
            iter_item = make_transition(pattern_index,pattern_char,lang_char) 
            result_item[pattern_index].update(iter_item)
        result.update(result_item)
    return result

if __name__ == "__main__":
    print ( compile_dfa('01','01') )