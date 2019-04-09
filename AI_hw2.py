# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 21:11:56 2017

@author: topbu
"""

import numpy
import math
import matplotlib.pyplot as plt
from collections import defaultdict
import copy

class EM:
    def __init__(self, threshold):
        self.likeli = 0
        self.threshold = threshold
        self.data = []
        self.col_name = []
        self.count = 0 # count number of data lines
        self.p_gender = {'0':0, '1':0}
        self.p_weight = {c: defaultdict(int) for c in self.p_gender}
        self.p_height = {c: defaultdict(int) for c in self.p_gender}
        self.itera = 0 # count iterated round
        
    def parse(self, fileName):        
        # get dataset
        with open(fileName, 'r', errors="replace") as text:
            tokens = text.readlines()
        
        # get the column name
        self.col_name = tokens[0].split()
        for i in range(1, len(tokens)):
            line_str = tokens[i].split()          
            self.data.append(line_str)  
            self.count += 1
            
        # set the missing data to be dictionry {'0':0, '1':0}
        for i in self.data:
            if i[0] is '-':
                # set dict for gender prob
                i[0] = {'0':0, '1':0}
                
        return
    
    def pickStarPot(self, init_v):        
        # set the missing data to be dictionry {'0':1, '1':0}
        self.p_gender['0'] = init_v[0]
        self.p_gender['1'] = 1 - self.p_gender['0'] 
                     
        self.p_weight['0']['0'] = init_v[1]
        self.p_weight['0']['1'] = 1 - self.p_weight['0']['0']
        self.p_weight['1']['0'] = init_v[2]
        self.p_weight['1']['1'] = 1 - self.p_weight['1']['0']

        self.p_height['0']['0'] = init_v[3]
        self.p_height['0']['1'] = 1 - self.p_height['0']['0']
        self.p_height['1']['0'] = init_v[4]
        self.p_height['1']['1'] = 1 - self.p_height['1']['0']             
        
        print("\n")
        print("Starting point of the parameters table.")
        print("-----------------------------------")
        print("P(G=0): " + str(self.p_gender['0']))
        print("P(G=1): " + str(self.p_gender['1']))
            
        print("P(W=0/G=0): " + str(self.p_weight['0']['0']))
        print("P(W=1/G=0): " + str(self.p_weight['0']['1']))
        print("P(W=0/G=1): " + str(self.p_weight['1']['0']))
        print("P(W=1/G=1): " + str(self.p_weight['1']['1']))
        
        print("P(H=0/G=0): " + str(self.p_height['0']['0']))
        print("P(H=1/G=0): " + str(self.p_height['0']['1']))
        print("P(H=0/G=1): " + str(self.p_height['1']['0']))
        print("P(H=1/G=1): " + str(self.p_height['1']['1']))  
        
        print("-----------------------------------")
        
        return
    
    def learn_params(self):
        # init all probability count 
        c_gender = {c: defaultdict(int) for c in self.p_gender}
        c_gender['0'] = 0
        c_gender['1'] = 0
        
        c_weight = {c: defaultdict(int) for c in self.p_gender}
        c_weight['0']['0'] = 0
        c_weight['0']['1'] = 0
        c_weight['1']['0'] = 0
        c_weight['1']['1'] = 0
        
        c_height = {c: defaultdict(int) for c in self.p_gender}
        c_height['0']['0'] = 0
        c_height['0']['1'] = 0
        c_height['1']['0'] = 0
        c_height['1']['1'] = 0
                
        # iterate each dataset to count
        for l in self.data:
            
            if l[0] is '0': # male
                # count gender probability P(g=0) 
                c_gender['0'] += 1 
                             
                # count weight probability P(w/g) -----p_weight[given_g=0][prob_w]
                c_weight['0'][l[1]] += 1 
                             
                # count height probability P(w/g) -----p_height[given_g=0][prob_h]   
                c_height['0'][l[2]] += 1 
                             
            elif l[0] is '1': # female
                # count gender probability P(g=1)
                c_gender['1'] += 1 
                             
                # count weight probability P(w/g) -----p_weight[given_g=1][prob_w]
                c_weight['1'][l[1]] += 1 
                             
                # count height probability P(w/g) -----p_height[given_g=1][prob_h]   
                c_height['1'][l[2]] += 1 
            
            else: # estimate parameters using the complete data     
                # count gender probability P(g=0) 
                c_gender['0'] += l[0]['0'] 
                c_gender['1'] += l[0]['1']    
                
                # count weight probability P(w/g) -----p_weight[given_g=0][prob_w]
                c_weight['0'][l[1]] += l[0]['0']
                c_weight['1'][l[1]] += l[0]['1']
                             
                # count height probability P(w/g) -----p_height[given_g=0][prob_h]   
                c_height['0'][l[2]] += l[0]['0']
                c_height['1'][l[2]] += l[0]['1']

        # calculate the parameters table  
        # store the previous parameters table
        prev_p_gender = copy.deepcopy(self.p_gender)    
        prev_p_weight = copy.deepcopy(self.p_weight)
        prev_p_height = copy.deepcopy(self.p_height)
            
        # calculate the new parameters table
        self.p_gender['0'] = c_gender['0'] / self.count 
        self.p_gender['1'] = c_gender['1'] / self.count 
                     
        self.p_weight['0']['0'] = c_weight['0']['0'] / sum(c_weight['0'].values())
        self.p_weight['0']['1'] = 1 - self.p_weight['0']['0']
        self.p_weight['1']['0'] = c_weight['1']['0'] / sum(c_weight['1'].values())
        self.p_weight['1']['1'] = 1 - self.p_weight['1']['0']

        self.p_height['0']['0'] = c_height['0']['0'] / sum(c_height['0'].values())
        self.p_height['0']['1'] = 1 - self.p_height['0']['0']
        self.p_height['1']['0'] = c_height['1']['0'] / sum(c_height['1'].values())
        self.p_height['1']['1'] = 1 - self.p_height['1']['0']
        
        print("Parameters table at iteration No." + str(self.itera))
        print("-----------------------------------")
        print("P(G=0): " + str(self.p_gender['0']))
        print("P(G=1): " + str(self.p_gender['1']))
            
        print("P(W=0/G=0): " + str(self.p_weight['0']['0']))
        print("P(W=1/G=0): " + str(self.p_weight['0']['1']))
        print("P(W=0/G=1): " + str(self.p_weight['1']['0']))
        print("P(W=1/G=1): " + str(self.p_weight['1']['1']))
        
        print("P(H=0/G=0): " + str(self.p_height['0']['0']))
        print("P(H=1/G=0): " + str(self.p_height['0']['1']))
        print("P(H=0/G=1): " + str(self.p_height['1']['0']))
        print("P(H=1/G=1): " + str(self.p_height['1']['1']))  
        
        print("-----------------------------------")
        return 
        
    def estimate_missing_data(self):        
        # estimate values of each missing dataset  
        for i in self.data:
            if i[0] is not '0' and i[0] is not '1':
                # calc the likelihood for each gender in the current dataset
                i[0]['0'] = ((self.p_weight['0'][i[1]] * self.p_height['0'][i[2]] * self.p_gender['0'] ) 
                            / (self.p_gender['0'] * self.p_weight['0'][i[1]] * self.p_height['0'][i[2]] + self.p_gender['1'] * self.p_weight['1'][i[1]] * self.p_height['1'][i[2]]))
                i[0]['1'] = 1 - i[0]['0']
                
        return

    def likeliHood(self):
        # store previous likelihood
        prev_likeli = self.likeli
        likeli = 1

        # calculate likelihood
        for i in self.data:
            if i[0] is '0':
                likeli *= self.p_gender['0']*self.p_weight['0'][i[1]]*self.p_height['0'][i[2]]
            elif i[0] is '1':
                likeli *= self.p_gender['1']*self.p_weight['1'][i[1]]*self.p_height['1'][i[2]]
            elif i[0] is not '0' and i[0] is not '1':
                likeli *= ((self.p_gender['0']*self.p_weight['0'][i[1]]*self.p_height['0'][i[2]]) 
                        + (self.p_gender['1']*self.p_weight['1'][i[1]]*self.p_height['1'][i[2]]))
             
        
        # calculate the log likelihood    
        self.likeli = math.log2(likeli)
        
        # calculate the different
        return abs(self.likeli - prev_likeli)    
           
                  
def main():
    ###################
    # parse file
    ###################
     # create a NaiveBayesian Classification object with threshold = 0.001
    model = EM(0.001)
    
    # parse the training data
    fileName = "hw2dataset_30.txt"
    print("File name: " + str(fileName))
    model.parse(fileName)
    
    ######################################
    # Pick a starting point of the parameters
    ######################################
 
    #init vector = 
    #        [P(G=0), P(W=0/G=0), P(W=0/G=1), P(H=0/G=0),  P(H=0/G=1)]
    init_v = [0.7,       0.8,         0.4,       0.7,         0.3]

    model.pickStarPot(init_v)
    
    # init diff to detect convergence
    diff = model.threshold + 1
    
    # record each iteration likelihood to plot
    li_record = []
    
    
    # Prodedure guaranteed to improve at each iteration, threshold = 0.001
    while diff > model.threshold:
        model.itera += 1
        ######################################
        # Complete the data using the current parameters
        ######################################
        model.estimate_missing_data()
        
        ######################################
        # Estimate the parameters related to data completion
        ######################################                
        model.learn_params()     
        
        # calculate log likelihood change 
        diff = model.likeliHood()
        
        # record the log likelihood value 
        li_record.append(model.likeli)
        print("Log likelihood:", model.likeli)
        
        
    print("change value at the final iteration (diff value): " + str(diff))
    

    print("Iteration round: " + str(model.itera))
    
    plt.plot(numpy.arange(1, model.itera+1, 1), li_record)
    plt.xlabel('iteration No.')
    plt.ylabel('Log likelihood')
    plt.xticks(numpy.arange(1, model.itera+1, 1))
    plt.grid()
    
if __name__ == '__main__':
    main()