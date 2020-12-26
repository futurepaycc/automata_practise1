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