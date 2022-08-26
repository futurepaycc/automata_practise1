# https://blog.reilkay.com/UsePythonTofindSelectCollection/

# BUG: 自定义文法也没有解释正确!

""" Follow集计算：
A -> ...Bc...型：根据定义，c ∈ Follow(B)。

A -> ...BC...型：根据定义，First(C) ⊆ Follow(B)。

A -> ...C型：文法左部的Follow集包含于串尾非终结符的Follow集。本例中Follow(A) ⊆ Follow(C)。

A -> ...BC这一类较为特殊，处理方法如下：
    该类型是A->...BC...型和A->...C型的特例情况，除了要按A->...BC...型的情况处理，将First(C) ⊆ Follow(B)，还要进行以下操作：
    第一步：看串尾C能否推导出ε。
    若不能推导出空，则同A->...C型操作，将Follow(A)Follow(C)。
    若能推导出空，则Follow(A)也属于Follow(B)，即Follow(A)Follow(B)，并进行下一步。
    第二步：若串尾非终结符能推导出ε，当其推空时，符号串将变为A->...B。
    重复第一步操作，即判断当前串尾符号B能否推导出ε，并按第一步操作。
    若不能推出ε则结束循环。
"""


# 判断非终结符的函数
def isnonterminal(symbol):
    if symbol[0] == '<' and symbol[-1] == '>':
        return True
    return False

class CalSelect(object):
    def __init__(self):
        # 初始化集合字典
        self.FIRST = {}
        self.FOLLOW = {}
        self.SELECT = {}
        # 初始化文法
        self.grammar = [
			# 文法填在此处
			"<E>-><T> <E'>",
			"<E'>->+ <T> <E'>",
			"<E'>->ε",
			"<T>-><F> <T'>",
			"<T'>->* <F> <T'>",
			"<T'>->ε",
			"<F>->( <E> )",
			"<F>->i"
        ]

        # BUG: 自定义文法也没有解释正确!
        self.grammar = [
            "<S>-><A> <C> <B>",
            "<S>-><C> b b",
            "<S>-><B> a",
            "<A>->d a",
            "<A>-><B> <C>",
            "<B>->g",
            "<B>->ϵ",
            "<C>->h",
            "<C>->ϵ"
        ]

        # 初始化终结符
        for i in range(0, len(self.grammar)):
            self.grammar[i] = self.grammar[i].replace('函数名', 'FT')
            self.grammar[i] = self.grammar[i].replace('变量名', 'iT')
            self.grammar[i] = self.grammar[i].replace('常数', 'CT')
            self.grammar[i] = self.grammar[i].replace('字符串', 'sT')
            self.grammar[i] = self.grammar[i].replace('字符', 'cT')

        # 初始化first集、follow集和select集字典的键值对中的值为空
        for line in self.grammar:
            part_begin = line.split("->")[0]
            part_end_temp = line.split("->")[1]
            part_end = part_end_temp.split(" ")
            self.FIRST[part_begin] = []
            self.FOLLOW[part_begin] = []
            self.SELECT[line] = []
        self.FOLLOW[self.grammar[0].split("->")[0]].append('#')

    # 求first集中第一部分：针对->直接推出第一个字符为终结符部分
    def getFirst(self):
        for line in self.grammar:
            part_begin = line.split("->")[0]
            part_end_temp = line.split("->")[1]
            part_end = part_end_temp.split(" ")
            if not isnonterminal(part_end[0]):
                self.FIRST[part_begin].append(part_end[0])

    # 求first第二部分：针对A -> B型，把B的first集加到A的first集合中
    def getFirst_2(self):
        for line in self.grammar:
            part_begin = line.split("->")[0]
            part_end_temp = line.split("->")[1]
            part_end = part_end_temp.split(" ")
            # 如果型如A -> B：则把B的first集加到A的first集中去
            if isnonterminal(part_end[0]):
                for i in range(0, len(part_end)):
                    if not isnonterminal(part_end[i]):
                        self.FIRST[part_begin].append(part_end[i])
                        break
                    list_remove = self.FIRST.get(part_end[i]).copy()
                    if 'ε' in list_remove and i is not len(part_end) - 1:
                        list_remove.remove('ε')
                    self.FIRST[part_begin].extend(list_remove)
                    if 'ε' not in self.FIRST[part_end[i]]:
                        break

    def getFirst_3(self):
        while 1:
            test = self.FIRST
            self.getFirst_2()
            # 去除重复项
            for i, j in self.FIRST.items():
                temp = []
                for word in list(set(j)):
                    temp.append(word)
                self.FIRST[i] = temp
            if test == self.FIRST:
                break

    def getFOLLOW_3(self):
        while 1:
            test = self.FOLLOW
            self.getFollow()
            # 去除重复项
            for i, j in self.FOLLOW.items():
                temp = []
                for word in list(set(j)):
                    temp.append(word)
                self.FOLLOW[i] = temp
            if test == self.FOLLOW:
                break

    # 计算follow集的第一部分，先计算 S -> A b 类型的
    def getFollow(self):
        for line in self.grammar:
            part_begin = line.split("->")[0]
            part_end_temp = line.split("->")[1]
            part_end = part_end_temp.split(" ")
            if part_begin == "<G>":
                pass
            # 如果是 S->a 直接推出终结符 则 continue
            if len(part_end) == 1 and not isnonterminal(part_end[0]):
                continue
            # 否则执行下面的操作
            else:
                # 将->后面的倒序
                part_end.reverse()
                # 最后一个为非终结符
                if isnonterminal(part_end[0]):

                    for i in range(0, len(part_end)):
                        if not isnonterminal(part_end[i]):
                            break
                        self.FOLLOW[part_end[i]].extend(self.FOLLOW.get(part_begin))
                        if 'ε' not in self.FIRST[part_end[i]]:
                            break

                    terminal_temp = part_end[0]
                    for item in part_end[1:]:
                        if not isnonterminal(item):
                            terminal_temp = item
                        else:
                            if isnonterminal(terminal_temp):
                                list_remove = self.FIRST.get(terminal_temp).copy()
                                if "ε" in list_remove:
                                    list_remove.remove("ε")
                                self.FOLLOW[item].extend(list_remove)
                            elif terminal_temp != 'ε':
                                self.FOLLOW[item].append(terminal_temp)
                            terminal_temp = item
                # 如果终结符在句型的末端
                else:
                    terminal_temp = part_end[0]
                    for item in part_end[1:]:
                        if not isnonterminal(item):
                            terminal_temp = item
                        else:
                            if isnonterminal(terminal_temp):
                                list_remove = self.FIRST.get(terminal_temp).copy()
                                if "ε" in list_remove:
                                    list_remove.remove("ε")
                                self.FOLLOW[item].extend(list_remove)
                            elif terminal_temp != 'ε':
                                self.FOLLOW[item].append(terminal_temp)
                            terminal_temp = item

    def getSelect(self):
        for line in self.grammar:
            part_begin = line.split("->")[0]
            part_end_temp = line.split("->")[1]
            part_end = part_end_temp.split(" ")
            line_first = []
            for item in part_end:
                if not isnonterminal(item):
                    line_first.append(item)
                    break
                else:
                    line_first.extend(self.FIRST[item])
                    if 'ε' not in self.FIRST[item]:
                        break
            line_first = list(set(line_first))
            can_derive_empty = True
            part_end.reverse()
            for item in part_end:
                if not isnonterminal(item):
                    if item != 'ε':
                        can_derive_empty = False
                        break
                else:
                    if 'ε' not in self.FIRST[item]:
                        can_derive_empty = False
                        break
            list_remove = line_first.copy()
            if "ε" in list_remove:
                list_remove.remove("ε")
            if can_derive_empty:
                self.SELECT[line].extend(list_remove)
                self.SELECT[line].extend(self.FOLLOW[part_begin])
            else:
                self.SELECT[line].extend(list_remove)
            self.SELECT[line] = list(set(self.SELECT[line]))

    def debug_out(self):
        for i, j in self.FIRST.items():
            str = j[0]
            for temp in j[1:]:
                str = str + ',' + temp
            print("FIRST(" + i + ")" + " = {" + str + "}")

        for i, j in self.FOLLOW.items():
            str = j[0]
            for temp in j[1:]:
                str = str + ',' + temp
            print("FOLLOW(" + i + ")" + " = {" + str + "}")
        for i, j in self.SELECT.items():
            str = j[0]
            for temp in j[1:]:
                str = str + ',' + temp
            print("SELECT(" + i + ")" + " = {" + str + "}")

    def run_cal(self):
        self.getFirst()
        self.getFirst_3()
        self.getFirst_3()
        self.getFOLLOW_3()
        self.getFOLLOW_3()
        self.getSelect()
        self.debug_out()


if __name__ == "__main__":
    CalSelect().run_cal()