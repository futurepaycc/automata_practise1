""" 
正则表达式制作-enfa表
FIXME:
1. 目前只是单状态制表
2. 字母表为{a,b}
"""
from box import Box
class NFA_State:
    global_id = 0
    def __init__(self, is_end: bool = False):
        self.is_end = is_end
        self.transition = {}
        self.epsilon_transition = []

        # self.id = NFA_State.global_id
        self.id = 'q'+str(NFA_State.global_id)
        NFA_State.global_id += 1


    def __str__(self):
        output = ""
        a_target =Box({'id':"ϕ"})
        b_target =Box({'id':"ϕ"})
        ε_target =Box({'id':"ϕ"})
        
        for transition_char, target_state in self.transition.items():
            if transition_char == 'a':
                a_target = target_state
            if transition_char == 'b':
                b_target = target_state
        for epsilon_target_state in self.epsilon_transition:
            ε_target = epsilon_target_state 


        output = "{}\t\t{}\t\t{}\t\t{}\n".format(self.id,a_target.id,b_target.id,ε_target.id) #NOTE:这里可能触发递归
        # print("output=".id,output,"\n")
        return output



class NFA:
    def __init__(self, start: NFA_State, end: NFA_State):
        self.start = start
        self.end = end

    def __str__(self):
        def all_transitions(from_state):
            output = list(from_state.transition.values())
            output.extend(from_state.epsilon_transition)
            # print("all_transitions=",str(output))
            return output

        # 深度优先遍历
        def traverse_state(current_state):
            # 忽略 已经访问过的state
            output = ""
            if id(current_state) in visited_id:
                return output

            
            output = str(current_state)
            visited_id.add(id(current_state))
            
            merged_transitions_target_state = all_transitions(current_state)

            for transition_target_state_item in merged_transitions_target_state:
                output += traverse_state(transition_target_state_item)

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
def add_epsilon_transition(come_from: NFA_State, to: NFA_State) -> None:
    come_from.epsilon_transition.append(to)

# 状态转移2: 字母符号 连接 
def add_transition(come_from: NFA_State, to: NFA_State, symbol: str) -> None:
    come_from.transition[symbol] = to

# 基本1: From epsilon.
def from_epsilon() -> NFA:
    start = NFA_State(is_end=False)
    end = NFA_State(is_end=True)
    add_epsilon_transition(start, end)
    return NFA(start, end)

# 基本2: From a single symbol.
def from_symbol(symbol: str) -> NFA:
    start = NFA_State(is_end=False)
    end = NFA_State(is_end=True)
    add_transition(start, end, symbol)
    return NFA(start, end)

# 组合1: 链接 a.b -> ab.
def concat(first: NFA, second: NFA) -> NFA:
    add_epsilon_transition(first.end, second.start)
    first.end.is_end = False
    return NFA(first.start, second.end)

# 组合2. 合并 a|b -> ab|
def union(first: NFA, second: NFA) -> NFA:
    start = NFA_State(is_end=False)
    add_epsilon_transition(start, first.start)
    add_epsilon_transition(start, second.start)

    end = NFA_State(is_end=True)
    add_epsilon_transition(first.end, end)
    first.end.is_end = False
    add_epsilon_transition(second.end, end)
    second.end.is_end = False

    return NFA(start, end)

# 组合3. 闭包 a* -> a*
def closure(nfa: NFA) -> NFA:
    start = NFA_State(is_end=False)
    end = NFA_State(is_end=True)
    
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
        nfa = to_NFA("ab.*") #NOTE: 这里要是postfix表达式
        print("<>\t\ta\t\tb\t\tε")
        print(nfa)

if __name__ == "__main__":
    unittest.main()