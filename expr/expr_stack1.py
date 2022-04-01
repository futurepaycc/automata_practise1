""" 
https://www.geeksforgeeks.org/expression-evaluation/
本质上还是用两个list来处理，通过伪装成栈，加入了优先级归约

TODO:
https://www.bilibili.com/video/BV1yk4y197nS?p=14 (22:00，改造成语法生成器)
"""

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
                val = (val*10) + int(tokens[i]) #将已分析部分的val整体*10+新分析数
                i += 1 #处理后增长，下面须复位
            values.append(val)
            i -= 1

        elif tokens[i] == ')':
            #括号结合归约
            while len(ops) != 0 and ops[-1] != '(':
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.append(applyOp(val1,val2,op))
            ops.pop()
        #当前token是运算符
        else:
            #优先级结合归约: 如果当前token的优先级小于已分析最后的运算符，左边进行归约
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

    return values[-1] #返回栈顶

if __name__ == "__main__":
    print(evalute("10 + 2 * 6"))
    print(evalute("100 * 2 + 12"))
    print(evalute("100 * ( 2 + 12 )"))
    print(evalute("100 * ( 2 + 12 ) / 14"))