#看来这里购造的是判断以'01'结尾的非确定状态机，和视频教程一类似

class NFA: 
	"""Class that encapsulates an NFA."""
	def __init__(self, transitionFunction, initialState, finalStates):
		self.delta = transitionFunction	
		self.q0 = initialState
		self.F = set(finalStates)

    # """ NOTE: NFA核心运行逻辑，此文件中就这个一个有价值函数 """
	def deltaHat(self, state, inputString):
		"""deltaHat is smart enough to return the empty set if no transition is defined."""
		states = set([state])
		for a in inputString: 
			newStates = set([])
			for state in states: 
				try: 
                    #self.delta[state][a]看成两部分: self.delta[state] 当前状态， [a] 作用于a输入
					newStates = newStates | self.delta[state][a] #如何前者为空，取后者(都是set)
				except KeyError: pass
			states = newStates
		return states

	def inLanguage(self, inputString):
		return len(self.deltaHat(self.q0, inputString) & self.F) > 0

    # """ 下面两个貌似输出工具函数, 不影响运行 """
	# def alphabet(self):
	# 	"""Returns the NFA's input alphabet, generated on the fly."""
	# 	Sigma = reduce(lambda a,b:set(a)|set(b), [list(x.keys()) for x in list(N.delta.values())])
	# 	return Sigma
	# def states(self):
	# 	"""Returns the NFA's set of states, generated on the fly."""
	# 	Q = set([self.q0]) | set(self.delta.keys()) | reduce(lambda a,b:a|b, reduce(lambda a,b:a+b, [list(x.values()) for x in list(self.delta.values())]))	# {q0, all states with outgoing arrows, all with incoming arrows}
	# 	return Q

if __name__ == "__main__":
    delta = {'q0':{'0':set(['q0','q1']),'1':set(['q0'])}, 'q1':{'1':set(['q2'])}}
    N = NFA(delta, 'q0', ['q2'])
    # N.deltaHat('q0', '0001') #NOTE: 这里为何要提前运行一次? 没有必要
    # print([(x, N.inLanguage(x)) for x in ['0','1','01','10','0001', '00010', '100101']])
    print(N.inLanguage("010"))
    print(N.inLanguage("0001"))
    print(N.inLanguage("1111"))