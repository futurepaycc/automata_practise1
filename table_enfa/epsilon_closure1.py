""" 
来源: https://stackoverflow.com/questions/49226978/recursion-over-a-dictionary-for-epsilon-closure-stops-working-when-list-is-passe
将tf2中的list改成了tuple，否则出错
还可参考:
https://github.com/nvaneethm/eclosure/blob/master/eclosure.ipynb
"""

tf2 = {('q0','a') : 'q1', ('q1','eps') : ('q2', 'q3'), ('q3','eps') : 'q0', ('q2','a') : 'q4', ('q4','eps') : 'q3'}

def epsilonClosure(transition, state):
    closure = []
    if (state, 'eps') not in transition:    # epsilon transition not possible
        return closure

    elif (state, 'eps') in transition:    # epsilon transition is possible
        closure.append(state)
        state = transition[(state, 'eps')]
        epsilonClosure(transition, state)

    if state not in closure:    # adds current state to list if not visited before
        closure.append(state)
    return closure

result = epsilonClosure(tf2, 'q1')
print(result)