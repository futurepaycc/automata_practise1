""" 
来源: https://boxbase.org/entries/2019/oct/14/lr1-parsing-tables/

TODO:
0. 文法分析移进、归约的核心也就是这样了
1. 高阶函数不易读，可以去除之
2. 尝试自已手工实现生成下面分析表
    E -> E + E
    E -> E * E
    E -> f      (f代表factor，是终结符号)

理解:
    根据文法,生成移进、归约表(状态机)
    使用这个表对代码进行分析，至accept状态
"""


class State:
    def __init__(self):
        self.stack = []
        self.top = 0


def advance(state, next_symbol):
    while GLOBAL_STACK[state.top][next_symbol](state):
        pass


def shift_closure(to_number):
    def _shift(state):
        print('shift {}'.format(to_number))
        state.stack.append(state.top)
        state.top = to_number
        return False
    return _shift


def reduce_closure(count, symbol):
    def _reduce(state):
        for _ in range(count):
            state.top = state.stack.pop()
        print('reduce {}'.format(symbol))
        GLOBAL_STACK[state.top][symbol](state)
        return True
    return _reduce


def accept_closure():
    def _accept(state):
        state.top = state.stack.pop()
        print('accepted')
        return False
    return _accept


""" 
0: program:     Shift 1 / Reduce 0 program
1: declaration: Shift 2 / Reduce 1 ⊤ 
   varDecl:     Shift 3 / Reduce 1 ⊤ 
   constDecl:   Shift 4 / Reduce 1 ⊤ 
   statement:   Shift 5 / Reduce 1 ⊤ 
2: Reduce 2 program
3: Reduce 1 declaration
4: Reduce 1 declaration
5: Reduce 1 declaration


s'      -> program
        | program declare

declare -> varDecl | constDecl | statemtment | $

varDecl -> varDecl

constDecl -> constDecl

statement -> 

"""

# 下面应该就是模拟分析表
GLOBAL_STACK = [
    #0
    {'$':           reduce_closure(0, 'program'), #归约到program
     'varDecl':     reduce_closure(0, 'program'), #归约到program 
     'constDecl':   reduce_closure(0, 'program'), #归约到program
     'statement':   reduce_closure(0, 'program'), #归约到program
     'program':     shift_closure(1)    #非终结符1
     },

    #1
    {'$':           accept_closure(),
     'declaration': shift_closure(2),   #非终结符2
     'varDecl':     shift_closure(3),   #移进到终结元素: GLOBAL_STACK[3]
     'constDecl':   shift_closure(4),   #移进到终结元素: GLOBAL_STACK[4]
     'statement':   shift_closure(5)    #移进到终结元素: GLOBAL_STACK[5]
     },

    #2
    {'$':           reduce_closure(2, 'program'),#归约到非终状态: program? 
     'varDecl':     reduce_closure(2, 'program'),#归约到非终状态: program?
     'constDecl':   reduce_closure(2, 'program'),#归约到非终状态: program?
     'statement':   reduce_closure(2, 'program') #归约到非终状态: program?
     },

# ----------------------------------------------------------这下面才是终结符，可以被分析
    #3
    {'$':           reduce_closure(1, 'declaration'), #归约到非终状态: GLOBAL_STACK[1]
     'varDecl':     reduce_closure(1, 'declaration'), #归约到非终状态: GLOBAL_STACK[1]
     'constDecl':   reduce_closure(1, 'declaration'), #归约到非终状态: GLOBAL_STACK[1]
     'statement':   reduce_closure(1, 'declaration')  #归约到非终状态: GLOBAL_STACK[1]
     },

    #4
    {'$':           reduce_closure(1, 'declaration'), #归约到非终状态: GLOBAL_STACK[1]
     'varDecl':     reduce_closure(1, 'declaration'), #归约到非终状态: GLOBAL_STACK[1]
     'constDecl':   reduce_closure(1, 'declaration'), #归约到非终状态: GLOBAL_STACK[1]
     'statement':   reduce_closure(1, 'declaration')  #归约到非终状态: GLOBAL_STACK[1]
     },

    #5
    {'$':           reduce_closure(1, 'declaration'), #归约到非终状态: GLOBAL_STACK[1]
     'varDecl':     reduce_closure(1, 'declaration'), #归约到非终状态: GLOBAL_STACK[1]
     'constDecl':   reduce_closure(1, 'declaration'), #归约到非终状态: GLOBAL_STACK[1]
     'statement':   reduce_closure(1, 'declaration')  #归约到非终状态: GLOBAL_STACK[1]
     }
    ]

if __name__ == "__main__":
    state = State()
    advance(state, 'varDecl')
    advance(state, 'varDecl')
    # advance(state, 'constDecl')
    # advance(state, '$')
    print('--------------')
    print(state.stack)
    print(state.top)
