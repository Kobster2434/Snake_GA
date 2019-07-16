import numpy as np
import random
#import copy 

'''
ANN for genetic algorithm.
Don't need backpropagation so it isn't included.
'''

class ANN:
    
    def __init__(self, _in, _out):
        self._in = _in
        self._out = _out
        self.input = [0] * _in 
        self.weights1 = np.random.rand(_in,7)  # 7 represents the number of hidden laysers.
        self.y = [0] * _out  ## Checks of the weights include the bias
        self.output = np.zeros(_out)
        self.weights2 = np.random.rand(7, _out)
    
    def sigmoid(self, x):
        return 1.0 / (1 + np.exp(-x))
    
    def softmax(self, scores):
        return np.exp(scores)/sum(np.exp(scores))
    
    def feed_forward(self, input_):
        self.layer1 = self.sigmoid(np.dot(input_, self.weights1))
        self.output = self.softmax(np.dot(self.layer1, self.weights2))
        return self.output
        
    #def mutate(self):
    #    self.weights1 += (np.random.rand(self._in,7) * 0.1 * random.choice([-1, 1]))
    #    self.weights2 += (np.random.rand(self.out, 7) * 0.1 * random.choice([-1, 1]))
    
    def crossover(self, other):
        child1 = ANN(self._in, self._out)
        child2 = ANN(self._in, self._out)
        
        child1.weights1 = self.weights1
        child1.weights2 = other.weights2
        
        child2.weights1 = other.weights1
        child2.weights2 = self.weights2
        return [child1, child2]
    
    def __repr__(self):
        return "ANN for genetic algorithm"
     
        
    def __str__(self):
        return "Artificial neural network for Genetic algorithm"
        
        
        
        
        
    