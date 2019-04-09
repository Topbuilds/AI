1. The homework assignment is developed under Anaconda3

2(with Python 3.6). Using Anaconda3 or ohter IDEs to open AI_hw2.py, 
   then run the file to get the result. 

2. In the main(), there is a variable fileName = "hw2dataset_30.txt" by default; Changing the file name to get different missing rate results.
   For picking the starting parameters, they can be set in the various init_v vector

    	#init vector = 
    	#        [P(G=0), P(W=0/G=0), P(W=0/G=1), P(H=0/G=0),  P(H=0/G=1)]
    	init_v = [0.7,       0.8,         0.4,       0.7,         0.3]

3. Result will be printed:
	(1) The starting points of the learning
	(2) The final conditional probability parameters(tables) for each iteration(learning)
	(3) Plots of the likelihood (y axis) vs number of iterations(x axis) to demonstrate the convergence of the algorithm

	Choosing the starting parameters:
	P(gender=M)=0.7;
	P(weight=greater_than_130|gender=M)=0.8;
	P(weight=greater_than_130|gender=F)=0.4;
	P(height= greater_than_55|gender=M)=0.7;
	P(height= greater_than_55|gender=F)=0.3; 



