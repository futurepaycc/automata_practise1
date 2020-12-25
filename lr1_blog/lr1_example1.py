def analyze(self, w):
    lr_table = self.table
    w = w + "$"
    count = 0  # 记录输入字符串的索引
    a = w[count]  # 指针指向的输入的字符
    vt = self.grammar["vt"]  # vt表示终结符集合
    vn = self.grammar["vn"]  # vn表示非终结符集合
    action = lr_table[0]  # ACTION表
    goto = lr_table[1]  # GOTO表
    status_stack = [0]  # 初始状态下状态栈中只有状态0
    while True:
        s = status_stack[len(status_stack) - 1]  # 当前栈顶露出的状态
        operation = action[s][vt.index(a)][0]  # 获取当前操作
        if "s" in operation:  # 移入操作
            status_stack.append(int(operation[1:]))  # 将s后面的状态压入栈顶
            count += 1  # 输入指针指向下一个字母
            a = w[count]  # 赋值
        elif "r" in operation:  # 归约操作
            b = int(operation[1:])  # 获取对应的产生式编号
            p = self.production[b]  # 获取产生式
            right = p.get("right")
            left = p.get("left")
            num = len(right)  # 产生式右部符号个数
            for i in range(num):
                status_stack.pop()  # 弹出状态
            c = vn.index(left)
            s = status_stack[len(status_stack) - 1]
            status_stack.append(int(goto[s][c][0]))
            print(left + "→" + right)  # 输出产生式
        elif operation == "acc":  # 语法分析完成
            break
        else:  # 其他就是出错了,需要调用错误恢复函数,此处就不写错误恢复函数了
            raise Exception("语法分析错误")

def closure(self, i):
    # j是每个LR1项目,是一个列表,有两个元素,第一个元素为LR0项目(此处为了方便用{"left":"","right":""}表示),只有在遇到第二个元素时才可以使用第一个项目对应的产生式进行归约
    vn = self.grammar["vn"]
    for j in i:
        item = j[0]  # 产生式项目
        right = item.get("right")  # 产生式右部
        indx = right.index("·")
        if indx < (len(right) - 1):  # 原点不在最后
            b = right[indx + 1]
            if b in vn:  # b为非终结符
                for k in self.production:  # 遍历文法产生式的所有项目
                    if b == k.get("left"):  # b为产生式左部
                        bta = None
                        if indx < (len(right) - 2):
                            bta = right[indx + 2]
                        else:
                            bta = j[1]
                        first_b = self.multi_first(bta)
                        for li in first_b:  # li表示first_b中的一个终结符
                            f = {
                                "left": b,
                                "right": "·" + k.get("right")
                            }
                            obj = [f, li]
                            i.append(obj)
    return i        


def go_to(self, i, x):
    j = []
    for k in i:
        f = k[0]  # LR0项目
        a = k[1]  # 展望符
        left = f.get("left")  # LR0项目左部
        right = f.get("right")  # LR0项目右部
        indx = right.find("·")
        if indx == -1:
            raise Exception("非法LR1项目")
        elif indx < (len(right) - 1) and right[indx + 1] == x:  # A → α·Xβ,存在X
            if indx < (len(right) - 2):  # 存在bta
                j.append([
                    {
                        "left": left,
                        "right": right[:indx] + right[indx + 1] + "·" + right[indx + 2:]
                    },  # LR0项目
                    a  # 展望符
                ])
            else:  # 不存在bta
                j.append([
                    {
                        "left": left,
                        "right": right[:indx] + right[indx + 1] + "·"
                    },  # LR0项目
                    a  # 展望符
                ])
    return self.closure(j)    

def items(self):
    # 注意这里self.closure的参数
    start = {
        "left": self.production[0].get("left"),
        "right": "·" + self.production[0].get("right")
    }
    c = [self.closure([[start, "$"]])]
    vt = self.grammar["vt"]
    vn = self.grammar["vn"]
    all_character = []  # 文法符号集合
    for i in vt:
        all_character.append(i)
    for i in vn:
        all_character.append(i)
    for i in c:
        for x in all_character:
            temp = self.go_to(i, x)
            if len(temp) != 0 and temp not in c:
                c.append(temp)
    return c    

def analysis_table(self, c):
    status = 0
    vt = self.grammar["vt"]
    vn = self.grammar["vn"]
    len3 = len(c)  # 状态集个数
    len1 = len(self.grammar["vt"])  # 终结符个数
    action = []  # ACTION集合,可以看作二维数组,如果每个元素也是一个数组,如果数组中没有元素则表示没有对应项目,初次之外可以是rn,sn,n,acc,如果数组中存在多个元素表示有冲突
    for i in range(len3):
        temp = []
        for j in range(len1):
            temp.append([])
        action.append(temp)
    len2 = len(self.grammar["vn"])  # 非终结符个数
    goto = []  # GOTO集合
    for i in range(len3):
        temp = []
        for j in range(len2):
            temp.append([])
        goto.append(temp)
    for i in c:  # i表示一个项目集
        for j in i:  # j表示项目集中的每个项目 [A→α·aβ, b ]
            lr0 = j[0]  # 第一个元素为lr0项目
            right = lr0.get("right")
            left = lr0.get("left")
            indx = right.find("·")
            if indx == -1:
                raise Exception("LR1项目有误")
            else:
                if indx < (len(right) - 1):  # 非归约项目,存在下一个状态
                    n = right[indx + 1]  # 圆点后面的文法符号
                    ij = self.go_to(i, n)
                    if n in vt:  # 下一个符号是终结符
                        action[status][vt.index(n)].append("s" + str(c.index(ij)))
                    else:
                        goto[status][vn.index(n)].append(str(c.index(ij)))
                else:  # 归约项目或者接收项目
                    if left == "S'" and right == (self.grammar["start"] + "·") and j[1] == "$":
                        # 接收项目
                        action[status][vt.index("$")].append("acc")
                    elif left != "S'":  # 归约项目
                        count = 0  # 规约项目对应的产生式的编号
                        s = right.replace("·", "")
                        for li in self.production:
                            if left == li.get("left") and s == li.get("right"):
                                action[status][vt.index(j[1])].append("r" + str(count))
                                break
                            count += 1
        status += 1
    return [action, goto]    

def is_lr1(self):
    lr_table = self.table
    for i in lr_table:
        for j in i:
            if len(j) >= 2:
                return True
    return False    