""" https://www.geeksforgeeks.org/finite-automata-algorithm-for-pattern-searching/ """

# Python program for Finite Automata 
# Pattern searching Algorithm 

MAX_NO_OF_CHARS = 256 #NOTE: 这个是不是有局限呢? 性能?

def getNextState(pattern, pattern_length, pattern_index, MAX_INDEX): 
	''' 
	calculate the next state 
	'''

	# If the character c is same as next character 
	# in pattern, then simply increment state 

	if pattern_index < pattern_length and MAX_INDEX == ord(pattern[pattern_index]): 
		return pattern_index+1

	i=0
	# ns stores the result which is next state 

	# ns finally contains the longest prefix 
	# which is also suffix in "pat[0..state-1]c" 

	# Start from the largest possible value and 
	# stop when you find a prefix which is also suffix 
	for ns in range(pattern_index,0,-1): 
		if ord(pattern[ns-1]) == MAX_INDEX: 
			while(i<ns-1): 
				if pattern[i] != pattern[pattern_index-ns+1+i]: 
					break
				i+=1
			if i == ns-1: 
				return ns 
	return 0

""" 1. 生成状态转移表 -> 就是自动机的一种表达方式 """
def computeTransformTable(pattern, pattern_length): 
	''' 
	This function builds the TF table which 
	represents Finite Automata for a given pattern 
	'''
	global MAX_NO_OF_CHARS 

	transform_table = [[0 for i in range(MAX_NO_OF_CHARS)] for _ in range(pattern_length+1)] 

	for pattern_index in range(pattern_length+1): 
		for MAX_INDEX in range(MAX_NO_OF_CHARS): 
			netxState = getNextState(pattern, pattern_length, pattern_index, MAX_INDEX) 
			transform_table[pattern_index][MAX_INDEX] = netxState 

	return transform_table 

def search(pattern, base_text): 
	''' 
	Prints all occurrences of pat in txt 
	'''
	global MAX_NO_OF_CHARS 
	pattern_length = len(pattern) 
	base_text_length = len(base_text) 
	transformTable = computeTransformTable(pattern, pattern_length)	 

	# Process txt over FA. 
	state=0
	for base_text_index in range(base_text_length): 
		state = transformTable[state][ord(base_text[base_text_index])] 
		if state == pattern_length: 
			print("Pattern found at index: {}".format(base_text_index-pattern_length+1)) 

# Driver program to test above function			 
def main(): 
	base_text = "AABAACAADAABAAABAA"
	pattern = "AABA"
	search(pattern, base_text) 

if __name__ == '__main__': 
	main() 

# This code is contributed by Atul Kumar 
