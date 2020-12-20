""" 
正则表达式制作-enfa表
TODO:
1. 格式化输出
2. 理解enfa运行原理
"""

class State:
    global_id = 0
    def __init__(self, is_end: bool = False):
        self.is_end = is_end
        self.transition = {}
        self.epsilon_transition = []

        self.id = State.global_id
        State.global_id += 1

    def __str__(self):
        output = ""
        output += "State {}{}\n".format(self.id, " (END)" if self.is_end else "")
        output += "Transition:\n"
        output += str(["State {}, t={}".format(i.id, t) for t, i in self.transition.items()]) + "\n"
        output += "Epsilon transition:\n"
        output += str(["State {}".format(i.id) for i in self.epsilon_transition]) + "\n"
        output += "-----------------------\n"
        return output


class NFA:
    def __init__(self, start: State, end: State):
        self.start = start
        self.end = end

    def __str__(self):
        def all_transitions(come_from: State) -> [State]:
            output = list(come_from.transition.values())
            output.extend(come_from.epsilon_transition)
            return output

        # Perform depth-first search from given state, print them.
        def traverse_state(stand_on: State) -> str:
            output = ""
            if id(stand_on) in visited_id:
                return output

            output = str(stand_on)
            visited_id.add(id(stand_on))
            
            for t in all_transitions(stand_on):
                output += traverse_state(t)

            return output

        visited_id = set()
        # return "Start on state {}\n".format(self.start.id) + traverse_state(self.start)
        return traverse_state(self.start)


# Use Thompson's construciton to build a DFA:
# Base rules:
# 1. from --epsilon--> to
# 2. from --a--> to  (single character)
# Inductive rules:
# 1. union
# 2. concatenation
# 3. closure


# Main workhorse function.
def to_NFA(postfix_exp: str) -> NFA:
    if postfix_exp == "":
        return from_epsilon()

    stack = []

    for token in postfix_exp:
        if token == "*":
            stack.append(closure(stack.pop()))
        elif token == "|":
            second = stack.pop()
            first = stack.pop()
            stack.append(union(first, second))
        elif token == ".":
            second = stack.pop()
            first = stack.pop()
            stack.append(concat(first, second))
        else:
            stack.append(from_symbol(token))

    assert len(stack) == 1, "Should be only one element left in the stack, but have {}".format(len(stack))

    return stack.pop()

# 状态转移1: epsilon 连接
def add_epsilon_transition(come_from: State, to: State) -> None:
    come_from.epsilon_transition.append(to)

# 状态转移2: 字母符号 连接 
def add_transition(come_from: State, to: State, symbol: str) -> None:
    come_from.transition[symbol] = to

# 基本1: From epsilon.
def from_epsilon() -> NFA:
    start = State(is_end=False)
    end = State(is_end=True)
    add_epsilon_transition(start, end)
    return NFA(start, end)

# 基本2: From a single symbol.
def from_symbol(symbol: str) -> NFA:
    start = State(is_end=False)
    end = State(is_end=True)
    add_transition(start, end, symbol)
    return NFA(start, end)

# 组合1: 链接 a.b -> ab.
def concat(first: NFA, second: NFA) -> NFA:
    add_epsilon_transition(first.end, second.start)
    first.end.is_end = False
    return NFA(first.start, second.end)

# 组合2. 合并 a|b -> ab|
def union(first: NFA, second: NFA) -> NFA:
    start = State(is_end=False)
    add_epsilon_transition(start, first.start)
    add_epsilon_transition(start, second.start)

    end = State(is_end=True)
    add_epsilon_transition(first.end, end)
    first.end.is_end = False
    add_epsilon_transition(second.end, end)
    second.end.is_end = False

    return NFA(start, end)

# 组合3. 闭包 a* -> a*
def closure(nfa: NFA) -> NFA:
    start = State(is_end=False)
    end = State(is_end=True)
    
    add_epsilon_transition(start, end)
    add_epsilon_transition(start, nfa.start)

    add_epsilon_transition(nfa.end, end)
    add_epsilon_transition(nfa.end, nfa.start)
    nfa.end.is_end = False

    return NFA(start, end)

# ---------------------------------------------------------------------
#  测试，说明: 使用postfix表达式
# ---------------------------------------------------------------------
import unittest
class Test_NFA(unittest.TestCase):
    def test_pass(self):
        pass
    # def test_state(self):
    #     state = State(False)
    #     print(  state   )

    # def test_from_symbol(self):
    #     print(  from_symbol('a')    )

    # TODO: 简化输出，制成表格
    def test_concat(self):
        nfa = to_NFA("ab.")
        print(nfa)

if __name__ == "__main__":
    unittest.main()