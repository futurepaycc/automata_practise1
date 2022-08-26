""" 最简generator，示范shift-reduce

处理文法生成:
    E−> E+E
    E−> E∗E
    E−> f 
使之能分析: f*f + f

说明: 
    1. f代表factor,对应字母 f
    2. 小写字母是终结符，大写字母非终结符
    3. 输入串终结符为$
"""

grammer = "E->E+E|E*E|f"
input   = "f*f+f"
token_stack = []    # 字符栈
ops_stack   = []    # 算符栈

# lexer部分(token类型隐含)
token_list = list(set(list("".join( grammer.split("->")[1].split("|") ))))  # ['E', 'f', '*', '+']
# grammer部分(含生成集)
stmt_list = grammer.split("->")[1].split("|")                               # ['E+E', 'E*E', 'f']
first_set = grammer.split("->")[0]                                          # 'E':  ??? 这个first集与定义不一致啊!!!
follow_mapping = dict(zip(stmt_list,[first_set]*len(stmt_list)))            # 右部到左部的反向映射

def reduce_stmt():
    while len(ops_stack) > 0:
        stmt = token_stack.pop() + ops_stack.pop() + token_stack.pop()      # 二元中缀形式表达式
        token_stack.append(follow_mapping[stmt])                            # 按mapping进行归约

# parser移进、归约部分
def reduce_token():
    token = token_stack.pop()
    stmt = follow_mapping[token]
    token_stack.append(stmt)
    reduce_stmt()

def shift_token(token):
    token_stack.append(token)
    reduce_token()

def shift_ops(token):
    ops_stack.append(token)

for i in range(0,len(input)):
    token = input[i] 
    if token in token_list:
        if token.isalpha():
            shift_token(token)
        else:
            shift_ops(token)

print(token_stack)
print(ops_stack)