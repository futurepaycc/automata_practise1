""" 
确定状态机系列:
https://www.geeksforgeeks.org/designing-deterministic-finite-automata-set-1/?ref=lbp
 """

#check string in 
#in state A 
def checkStateA(n): 
	
	#if length of 
	#string is one 
	#print not accepted 
	if(len(n)==1): 
		print("string not accepted") 
	else: 
		#pass string to stateB to 
		#to check further transitions 
		if(n[0]=='a' or n[0]=='b'): 
			stateB(n[1:]) 
			
			
def stateB(n): 
	#here if length 
	#is not 1 print#string not accepted 
	if(len(n)!=1): 
		print("string not accepted") 
	else: 
		#else pass string 
		#to state c 
		stateC(n[1:]) 
def stateC(n): 
	#here if length 
	#becomes zero 
	#print accepted 
	#else not accepted 
	if (len(n)==0): 
		print("string accepted") 
	else: 
		print("string not accepted") 
	
	
#take input	 
n=input() 
checkStateA(n) 
