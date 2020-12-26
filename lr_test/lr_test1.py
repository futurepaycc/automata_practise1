""" 
NOTE: 最简generator
TODO:
    1. lexer,token支持类型
    2. 运算符支持优先级
    3. 扩充表达式，使之支持语句
    4. parser尝试生成ast_json
"""

""" 
处理文法生成:
    E−> E+E
    E−> E∗E
    E−> f 
使之能分析: f*f + f

说明: 
    1. f代表factor,对应字母 f
    2. 小写字母是终结符，大写字母非终结符
    2. 输入串终结符为$
"""

grammer= "E->E+E|E*E|f"
input = "f*f+f"
token_stack = []
ops_stack = []

# lexer部分(token类型隐含)
token_list = list(set(list("".join( grammer.split("->")[1].split("|") )))) # token_list = list(set(list("".join(stmt_list))))

# grammer部分(含生成集)
stmt_list = grammer.split("->")[1].split("|")
first_set = grammer.split("->")[0] #first_set只有一条 = E
follow_mapping = dict(zip(stmt_list,[first_set]*len(stmt_list)))
def reduce_stmt():
    while len(ops_stack) > 0:
        stmt = token_stack.pop() + ops_stack.pop() + token_stack.pop()
        token_stack.append(follow_mapping[stmt])

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

i=0
while i < len(input):
    token = input[i] 
    if token in token_list:
        if token.isalpha():
            shift_token(token)
        else:
            shift_ops(token)
    i += 1

# grammer移进、归约部分
# reduce_stmt()
print(token_stack)
print(ops_stack)