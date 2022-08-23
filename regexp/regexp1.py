""" 
来源: https://github.com/ofey404/blogCode 
原理: https://deniskyashif.com/2019/02/17/implementing-a-regular-expression-engine/
优点: NFA代码易读，有状态输出
缺点: 词法、文法非典型算法，基于栈和组合虚拟机
"""

""" 
理解:
* ϵ equ  : 基础匹配
* . * |  : 运算匹配

参《计算的本质:ch3.3》
"""

from typing import List # for mypy return list type declare
# ---------------------------------------------------------------------
#  parser 
# ---------------------------------------------------------------------
def parse_regex_to_postfix(exp: str) -> str:
    return to_postfix(insert_explicit_concate_operator(exp))

not_end_of_trunk = [".", "(", "|"]
not_start_of_trunk = [")", ".", "*", "|"]

# Insert . (concatenation operator) in two trunks which have no operators between.
# Trunks:
# 1. character. ab -> a.b
# 2. bracked expression. (!$#)a -> (!$#).a
# 3. The unary operator * together with its operand.  a*b -> a*.b
# 显式插入连接符号
def insert_explicit_concate_operator(exp: str) -> str:
    output = ""
    for i, token in enumerate(exp):
        output += token
        if token in not_end_of_trunk:
            continue
        
        # If nothing to peek, break.
        if i == len(exp) - 1:
            continue
        peek_next = exp[i+1]

        if peek_next not in not_start_of_trunk:
            output += "."
        
    return output


# Postfix: Read from right to left, imagine a stack that hold operators until
# enough operands are given.

operators = [".", "|", "*"]

parenthesis = ["(", ")"]

# '或|并' 的优先级最低
precedence = {
    "|": 0,
    ".": 1,
    "*": 2,
}

# Postfix => 后缀表达式，逆波兰表达式
def to_postfix(explicited_concate_exp: str) -> str:
    def stack_top_is_poppable(stack, token):
        return (len(stack) > 0) and (stack[-1] != "(") and (precedence[stack[-1]] >= precedence[token])

    output = ""
    operator_stack = []
    
    for token in explicited_concate_exp:
        if (token not in operators) and (token not in parenthesis):
            output += token
        if token in operators:
            while stack_top_is_poppable(operator_stack, token):
                output += operator_stack.pop()
            operator_stack.append(token)
        if token == "(":
            operator_stack.append(token)
        if token == ")":
            while (operator_stack[-1] != "("):
                output += operator_stack.pop()
            operator_stack.pop()
        
    while operator_stack:
        output += operator_stack.pop()
        
    return output

# ---------------------------------------------------------------------
#  NFA: 基于栈和状态组合实现，含ε
# ---------------------------------------------------------------------    
class State:
    global_id = 0
    def __init__(self, is_end: bool = False):
        self.is_end = is_end
        # NOTE 普通状态转移与空状态转移分开声明
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
        return output

# NFA, 类和闭包混写，代码习惯有问题吧 ???
class FiniteAutomata:
    def __init__(self, start: State, end: State):
        self.start = start
        self.end = end

    def __str__(self):
        def all_transitions(come_from: State) -> List[State]:
            output = list(come_from.transition.values())
            output.extend(come_from.epsilon_transition)
            return output

        # Perform depth-first search from given state, print them.
        # NOTE 构建状态转移表!
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
        return "Start on state {}\n".format(self.start.id) + traverse_state(self.start)


# Use Thompson's construciton to build a DFA:
# Base rules:
# 1. from --epsilon--> to
# 2. from --a--> to  (single character)
# Inductive rules:
# 1. union
# 2. concatenation
# 3. closure

# Main workhorse function.
def to_NFA(postfix_exp: str) -> FiniteAutomata:
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
def from_epsilon() -> FiniteAutomata:
    start = State(is_end=False)
    end = State(is_end=True)
    add_epsilon_transition(start, end)
    return FiniteAutomata(start, end)

# 基本2: From a single symbol.
def from_symbol(symbol: str) -> FiniteAutomata:
    start = State(is_end=False)
    end = State(is_end=True)
    add_transition(start, end, symbol)
    return FiniteAutomata(start, end)


# 组合1: 链接 a.b -> ab.
def concat(first: FiniteAutomata, second: FiniteAutomata) -> FiniteAutomata:
    add_epsilon_transition(first.end, second.start)
    first.end.is_end = False
    return FiniteAutomata(first.start, second.end)

# 组合2. 合并 a|b -> ab|
def union(first: FiniteAutomata, second: FiniteAutomata) -> FiniteAutomata:
    start = State(is_end=False)
    add_epsilon_transition(start, first.start)
    add_epsilon_transition(start, second.start)

    end = State(is_end=True)
    add_epsilon_transition(first.end, end)
    first.end.is_end = False
    add_epsilon_transition(second.end, end)
    second.end.is_end = False

    return FiniteAutomata(start, end)

# 组合3. 闭包 a* -> a*
def closure(nfa: FiniteAutomata) -> FiniteAutomata:
    start = State(is_end=False)
    end = State(is_end=True)
    
    add_epsilon_transition(start, end)
    add_epsilon_transition(start, nfa.start)

    add_epsilon_transition(nfa.end, end)
    add_epsilon_transition(nfa.end, nfa.start)
    nfa.end.is_end = False

    return FiniteAutomata(start, end)

# ---------------------------------------------------------------------
#  matcher 
# ---------------------------------------------------------------------      
# Workhorse function.
# Create a matcher function which return match or not from given regex.
from typing import Callable  # for lambda type hint
def create_matcher(regex: str = "") -> Callable[[FiniteAutomata, str], bool]:
    postfix_exp = parse_regex_to_postfix(regex)
    nfa = to_NFA(postfix_exp)

    return lambda word: search(nfa, word)


# Follow the automata step by step.
def search(nfa: FiniteAutomata, word: str) -> bool:
    current_states = []
    current_states.extend(all_next_states_from(nfa.start))

    for character in word:
        next_states = []

        for state in current_states:
            if character not in state.transition:
                continue
            next = state.transition[character]
            next_states.extend(all_next_states_from(next))

        current_states = next_states

    # Check after len(word) step, whether there are any end state.
    has_end_state = False
    for final_state in current_states:
        if final_state.is_end:
            has_end_state = True
            break
    return has_end_state
    

# Return the list of given state and all possible states can be reach by any
# epsilon transition chain from given state.
# Visited 
def all_next_states_from(state: State) -> List[State]:
    visited = set()
    output = []
    if len(state.epsilon_transition) > 0:
        for st in state.epsilon_transition:
            if st not in visited:
                visited.add(st)
                output.extend(all_next_states_from(st))
    else:  # DEBUG, If this `else` should be deleted?
        output.append(state)
    return output


# ---------------------------------------------------------------------
#  test 
# ---------------------------------------------------------------------
import unittest  
# NOTE 宏观流程: 原始pattern -> 插入链接运算符 -> 构建逆波兰表达式 -> 构建NFA
def create_matcher1(regex):
    postfix_exp = to_postfix(insert_explicit_concate_operator(regex))
    nfa = to_NFA(postfix_exp)
    return lambda word: search(nfa, word) #NOTE εNFA的使用

class Test_hello1(unittest.TestCase):
    def test_single(self):
        #单符号
        matcher = create_matcher1('a')
        self.assertEqual(matcher("a"),True)
        self.assertEqual(matcher("b"),False)

        #链接
        matcher = create_matcher1('ab')
        self.assertEqual(matcher("ab"),True)
        self.assertEqual(matcher("ba"),False)

        #闭包
        matcher = create_matcher1('a*')
        self.assertEqual(matcher("a"),True)
        self.assertEqual(matcher("aaa"),True)
        self.assertEqual(matcher("ba"),False)

        #或
        matcher = create_matcher1('a|b')
        self.assertEqual(matcher("a"),True)
        self.assertEqual(matcher("b"),True)
        self.assertEqual(matcher("c"),False)

        #括号组合
        matcher = create_matcher1('(a|b)*c')
        self.assertEqual(matcher("aaac"),True)
        self.assertEqual(matcher("babc"),True)
        self.assertEqual(matcher("ccc"),False)

if __name__ == "__main__":
    unittest.main()