""" 
https://www.geeksforgeeks.org/expression-evaluation/
"""

""" 优先级 """
def preceden(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    return 0

def applyOp(a,b,op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a // b

def evalute(tokens):
    #stack1: 存储整数
    values = []
    #stack2: 存储操作符
    ops = []
    i=0
    while i < len(tokens):
        
        if tokens[i] == ' ':
            i += 1
            continue

        elif tokens[i] == '(':
            ops.append(tokens[i])

        elif tokens[i].isdigit():
            val = 0
            while (i < len(tokens) and tokens[i].isdigit()):
                val = (val*10) + int(tokens[i]) #这一句没有bug么?
                i += 1
            values.append(val)
            i -= 1

        elif tokens[i] == ')':
            while len(ops) != 0 and ops[-1] != '(':
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.append(applyOp(val1,val2,op))
            ops.pop()

        else:
            while (len(ops) !=0 and preceden(ops[-1]) >= preceden(tokens[i])):
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.append(applyOp(val1,val2,op))
            ops.append(tokens[i])
        i += 1

    while len(ops) != 0:
        val2 = values.pop()
        val1 = values.pop()
        op = ops.pop()
        values.append(applyOp(val1,val2,op))

    return values[-1]

if __name__ == "__main__":
    print(evalute("10 + 2 * 6"))
    print(evalute("100 * 2 + 12"))
    print(evalute("100 * ( 2 + 12 )"))
    print(evalute("100 * ( 2 + 12 ) / 14"))