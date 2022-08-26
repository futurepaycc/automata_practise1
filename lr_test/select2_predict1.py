# https://blog.csdn.net/Bamboo9999/article/details/121205051

# 处理输入的文法
def put_in():
    # 定义全局变量
    global a,vn, vt,start


    vn = ['S','T','A']          # 非终符
    vt = ['a','^','(',')',',']  # 终符
    a = [                       # 产生式
        "S->a",
        "S->^",
        "S->(T)",
        "T->SA",
        "A->,SA",
        "A->ϵ"
    ]
    start = a[0][0]             # start表示开始符

    for i in a:
        # 先保存非终结符
        if i[0] not in vn:
            vn.append(i[0])
        # 后保存终结符
        for j in range(3,len(i)):
            if not i[j].isupper() and i[j] not in vt and i[j] != 'ε':
                vt.append(i[j])

    print()
    print("非终结符为：")
    print(vn)
    print("终结符为：")
    print(vt)

# 求所有非终结符的first集
def first_all_not_terminal():
    global  f
    f = []
    for i in range(len(vn)):
        f = f + [set()]

    # 要多循环几次，不然一次循环可能会造成前面的非终结符的first集会少元素
    for num in range(len(a)):
        for s in vn:
            first_single_not_terminal(s)
    print('非终结符的FIRST集依次为：')
    print(f)

# 求单个非终结符的first集
def first_single_not_terminal(x):
    index_start = index(x)  # 非终结符x在vn的位置
    for i in a:
        if i[0] == x: # x为非终结符
            # 右边第一个为终结符
            for j in range(3,len(i)):
                if judge_terminal(i[j]):
                    # 直接添加此终结符
                    f[index_start].add(i[j])
                    break
                # 当右边第一个为非终结符时
                else:
                    # 当此first集没有空串时，直接添加此first集给开始符x
                    index_next = index(i[j])
                    if 'ε' not in f[index_next]:
                        for e in f[index_next]:
                            f[index_start].add(e)
                        break
                    # 如果此first集含有空串时
                    else:
                        if j == len(i) -1:
                            break
                        # 添加去掉空串的first集
                        for e in f[index_next]:
                            if e != 'ε':
                                f[index_start].add(e)
                        index_next_next = index(i[j+1]) # 后面的符号的位置
                        # 添加后面的符号的first集
                        for x in f[index_next_next]:
                            f[index_start].add(x)

# 求非终结符在vn的位置，即索引
def index(x):
    for n in range(len(vn)):
        if x == vn[n]:
            return n

# 求单个文法在文法a中的位置
def index_num(x):
    for n in range(len(a)):
        if x == a[n]:
            return n

# 判断是不是终结符
def judge_terminal(x):
    if x in vn:
        return False
    else:
        return True

# 求所有文法的First集
def first_all_string():
    global f1
    f1 = []
    for i in range(len(a)):
        f1 = f1 + [set()]

    for j in range(len(vn)):
        for i in range(len(a)):
            first_single_string(i)

    print('文法的FIRST集依次为：')
    print(f1)

# 求单个文法的first集
def first_single_string(num): # num表示文法的位置
    string = a[num] # 单独的一串文法
    for i in range(3,len(string)):
        # 如果遇到终结符，将终结符添加进去，并且跳出循环
        if judge_terminal(string[i]):
            f1[num].add(string[i])
            break
        # 是非终结符，则添加去掉空串的first集
        else:
            index_next = index(string[i]) # 记录此非终结符在vn的位置
            # 如果没有空串
            if 'ε' not in f[index_next]:
                for e in f[index_next]:
                    f1[num].add(e)
                break
            # 如果有空串
            else:
                for e in f[index_next]:
                    if e != 'ε':
                        f1[num].add(e)
                if i == len(string) -1 :
                    break
                index_next_next = index(string[i+1])
                for e in f[index_next_next]:
                    f1[num].add(e)

# 求所有非终结符的follow集
def follow_all():
    global follow
    follow = []
    for i in range(len(vn)):
        follow = follow + [set()]
        follow[i].add("#") # 给所有的非终结符的follow集添加 # 符号

    for num in range(len(a)):
        for s in vn: # s为非终结符
            follow_single(s)
    print('非终结符的follow集依次为：')
    print(follow)

# 求单个非终结符的follow集
def follow_single(s):
    index_vn = index(s) # 表示当前非终结符在vn的位置
    for i in a:
        index_vn_start = index(i[0]) # 表示当前非终结符所在的文法的开始符在vn的位置
        for j in range(3,len(i)):
            if s == i[j]: # j表示非终结符s在文法a中的位置
                # 如果非终结符在文法的末尾，此时非终结符的follow集为文法开始符的follow集
                if j == len(i) - 1:
                    for e in follow[index_vn_start]:
                        if e != 'ε': # follow集不能有空串
                            follow[index_vn].add(e)
                    break
                # 如果非终结符不在文法的末尾
                else:
                    # 如果后面跟着的是终结符
                    if judge_terminal(i[j+1]):
                        follow[index_vn].add(i[j+1])
                        break # 是终结符就要跳出循环
                    # 如果后面跟着的是非终结符，且first集不包含空串
                    else:
                        index_vn_next = index(i[j+1]) # 为此非终结符后面跟着的非终结符在vn的位置
                        # 如果后面的非终结符的frist集不包含空串，直接添加它的first集
                        if 'ε' not in f[index_vn_next]:
                            for e in f[index_vn_next]:
                                follow[index_vn].add(e)
                        # 如果后面的非终结符的frist集包含空串
                        else:
                            # 加上去掉first集中的空串
                            for e in f[index_vn_next]:
                                if e != 'ε':
                                    follow[index_vn].add(e)
                            # 加上此文法开始符的follow集
                            for e in follow[index_vn_start]:
                                if e != 'ε':
                                    follow[index_vn].add(e)

# 求所有文法的select集
def select_all():
    global select
    select = []
    for i in range(len(a)):
        select = select + [set()]
        select_singe(i) # 注意i为整数

    print('文法的select集依次为：')
    print(select)

# 求单个文法的select集
def select_singe(i):
    str = a[i] # 存储对应的文法
    # 当文法的first集不包含空串
    if 'ε' not in f1[i]:
        for e in f1[i]:
            select[i].add(e)
    # 当文法的first集包含空串
    else:
        # 加上去掉空串的此文法的first集
        for e in f1[i]:
            if e != 'ε':
                select[i].add(e)
        index_start = index(str[0]) # 找出此文法的开始符在vn的位置
        for e in follow[index_start]:
            select[i].add(e)

# 判断是否为LL1文法
def judge_LL1():
    global temp_set,compare_set,flag
    flag = True # false表示不是LL(1)文法，true表示是
    for x in vn: # x表示非终结符
        temp_set = set()
        compare_set = set()
        for i in a:
            if x == i[0]:
                num = index_num(i)
                if len(temp_set) == 0:
                    temp_set = temp_set | select[num]
                else:
                    compare_set = temp_set & select[num]
        if len(compare_set) != 0:
            print("不是LL(1)文法")
            flag = False
            break
    if flag:
        print("是LL(1)文法")

# 构造预测分析表
def forecast_analysis_table():
    # 行表示非终结符，列表示终结符
    global table
    # 创建空的二维列表
    table = [['' for i in range(len(vt))] for j in range(len(vn))]
    for i in range(len(vn)):
        for j in range(len(vt)):
            for n in range(len(a)):
                if vn[i] == a[n][0]:
                    if vt[j] in f1[n]:
                        table[i][j] = str_list(a[n][3:])
    print("此文法的预测分析表为：")
    print(table)

# 将列表中的元素变成字符串
def str_list(x):
    b = [str(j) for j in x]
    str2 = ''.join(b)
    return str2

# 求元素在终结符vt的位置
def index_vt(x):
    global flag1
    flag1 = False # false表示没有在vt中找到此元素
    for i in range(len(vt)):
        if x == vt[i]:
            flag1 = True
            return i
    if not flag1:
        return -1

# 将左边的文法变成终结符在末尾
def find_terminator(x,index_right):
    # 如果是终结符则直接返回列表
    left_last = x[-1]
    if judge_terminal(left_last):
        return x
    else:
        # 求左边非终结符在vn的位置
        index_left = index(left_last)
        # 删除左边最后一个元素
        x.pop()
        for e in list(table[index_left][index_right][::-1]):
            x.append(e)
        find_terminator(x,index_right)

# 匹配字符串，这里使用的是预测分析法
def match():
    # 如果是LL(1)文法
    if flag:
        # global  stack
        global stack
        # 输入待匹配的字符串，结尾一定要记得输入 #
        print("请输入待匹配的字符串：")
        string = list("(a,a)#")
        stack = ['#', start]
        # 输出
        str_stack = str_list(stack)
        str_string = str_list(string)
        print(format("%-25s%5s" % (str_stack, str_string)))
        while True:
            # 左边取最后一个元素
            left_last = stack[-1]
            # 右边取第一个元素
            right_first = string[0]
            index_right = index_vt(right_first)
            if index_right == -1:
                print("匹配错误")
                break
            # 如果左边最后一个元素不是非终结符
            if not judge_terminal(left_last):
                # 将左边的文法变成终结符在末尾，即修改stack
                find_terminator(stack,index_right)
            str_stack = str_list(stack)
            str_string = str_list(string)
            print(format("%-25s%5s" % (str_stack,str_string)))
            # 左边删除最后一个元素
            stack.pop()
            # 右边删除第一个元素
            string.pop(0)
            if stack[-1] == '#' and string[0] == '#':
                str_stack = str_list(stack)
                str_string = str_list(string)
                print(format("%-25s%5s" % (str_stack, str_string)))
                print("匹配成功")
                break

# 运行函数
def run():
    put_in()
    print()

    first_all_not_terminal()
    first_all_string()
    follow_all()
    select_all()
    print()

    print("判断是否为LL(1)文法：")
    judge_LL1()
    print()

    forecast_analysis_table()
    print()

    match()

run()
