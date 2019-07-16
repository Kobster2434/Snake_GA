from ANN import ANN
from Snake import playgame
import random
import numpy as np
import pygame
from pynput.keyboard import Key, Controller
import sys

class GeneticAlg:
    
    '''
    Fitness: A function to evaluate the score.  || Coded seperately in code.
    Fitness_threshold: A threshold specifying the termination criterion.
    p: The number of hypotheses to be included in the population.
    r: the fraction of the population to be replaced by crossover at each step.
    m: The mutation rate.
    '''
    
    '''
    Modifications to make:
    Have it run one iteration at a time and manually do the next one.
    Store the run of all hypothesis in an iteratoin.
    After basic implementation working add to it more complex features.
    How to implement crossover and mutation.
    Add in a neural network somewhere. Output layer is what key to press
    Input is what it is getting from the game environment.
    crossover between node connections?
    mutation of node weights?
    '''
    
    def __init__(self, fitness_threshold, p, r, m, _in, _out):
        self.fitness_t = fitness_threshold
        self.p = p
        self.r = r
        self.m = m
        self.input_node = _in  # Number of input nodes. 
        self.output_node = _out # Number of output nodes.
        self.global_best = 0
        self.global_best_ANN = None
        self.size = int(np.ceil((1-self.r)*self.p))
        self.size_lo = int(np.floor((self.p*self.r)/2))  # left over
        
        
    '''
    Creates an atrificual neural network with desired input and output nodes.
    '''    
    def create_ANN(self):  # Will have a ANN class
        return ANN(self.input_node, self.output_node)
    
    '''
    Creates the population P.
    This should call create_ANN function.
    '''
    def init_pop(self):  # Create population P.
        self.P = [0] * self.p
        for i in range(self.p):
            #name = "neural_net_" + str(i+1) # this is irrelevant.
            name = self.create_ANN()
            self.P[i] = name
        
    
    '''
    Function to compute the fitness of each hypothesis. 
    Will be highest score.
    
    Below will do each game 1 by one. But I want in parrallel. 
    Need to figure this out. The way I've done this pygame doesn't allow me to do 
    what I wan't so I can't do it in parallel.
    '''
    def compute_fitness(self):  # for each hypothesis h in population P
        self.fitness_list = []
        print(self.P)
        for neural_net in self.P:
            fitness1 = self.evaluate(neural_net)
            fitness1 += 0.25
            fitness2 = self.evaluate(neural_net)
            fitness2 += 0.25
            fitness3 = self.evaluate(neural_net)
            fitness3 += 0.25
            
            average_fitness = (fitness1 + fitness2 + fitness3) / 3
            self.fitness_list.append(average_fitness)
        self.highest_fitness()
    
    '''
    Function that creates a new generation.
    '''
    def create_new_gen(self):
        '''
        probabilistically select (1-r)*p members of P to add to PS.
        Probabillity of selecting hypothesis h_i frmo P is given by:
        P(h_i) = fitness(h_i)/sum(j=1 to p) fitness(h_j)
        '''
        P_s = [0] * self.p # change this later, apply above formula. 
        
        prob_added = []
        sum_fitness = self.sum_all_fitness()
        if sum_fitness == 0:
            sum_fitness = 1
        for i in range(len(self.fitness_list)):
            prop = self.fitness_list[i] / sum_fitness
            #sum_before = sum(prob_added)  # to make dist cumulative as that is a requirement.
            ## sum([]) = 0 so don't have to consider the case where the list is empty.
            prob_added.append(prop)
                
        draw = list(np.random.choice(a = self.P, size = self.size, 
                         p = prob_added, replace = False))
        to_add = self.crossover(prob_added)
        for i in range(len(draw)):
            P_s[i] = draw[i]
        for i in range(len(to_add)):
            P_s[len(draw)+i] = to_add[i]
        self.P = P_s  # UPDATE
        self.mutate()
                
    '''
    Function that returns the sum of all hypothesis fitness.
    '''
    def sum_all_fitness(self):
        return sum(self.fitness_list)
    
    '''
    Fucntion that performs crossover.
    select r*p/2 pairs from P according to p(h_i) for each pair produce two offprring 
    by performing the crossover oerator.
    (to get what I want I can use number representing the list location 0 to len-1)
    this makes it easier to see of they are equal or not. this allows for easy comparison.
    '''
    def crossover(self, prob_added):
        num_lst = [0] * self.p
        for i in range(self.p):
            num_lst[i] = i
        draw1 = list(np.random.choice(a = num_lst, size = self.size_lo, 
                         p = prob_added, replace = False))
        draw2 = list(np.random.choice(a = num_lst, size = self.size_lo, 
                         p = prob_added, replace = False))
        comb_lst = []
        for i in range(len(draw1)):
            boolo = True
            while boolo:
                draw = None
                if draw1[i] == draw2[i]:
                    draw = list(np.random.choice(a = num_lst, size = 1, 
                                                 p = prob_added, replace = False))
                if draw != draw2[i]:
                    boolo = False
            
            cross = self.P[draw1[i]].crossover(self.P[draw2[i]])
            for j in range(2):
                comb_lst.append(cross[j])
        return comb_lst
        
    
    '''
    Function that mutates the neural network.
    '''
    def mutate(self):
        for i in range(self.p):
            randnum = random.uniform(0, 1)
            if randnum < self.m:
                self.P[i] = self.mutate__(self.P[i])
    
    '''
    Compute fitness of a hypothesis
    '''
    def evaluate(self, hypothesis):
        pygame.init()
        playg = playgame(pygame)
        playg.play_game()
        count = 1
        move = Key.right  # used for initial move
        details = []
        while playg.gameRunning() and playg.gameOver == False:
            if count != 1:
                move_ = hypothesis.feed_forward(details)  # gets list of len 4 containing output
                '''
                list position:
                    0 -- up
                    1 -- right
                    2 -- down
                    3 -- left
                '''
                max_pos = 0
                max_num = 0
                for i in range(len(move_)):
                    if move_[i] > max_num:
                        max_pos = i
                        max_num = move_[i]
                if max_pos == 0:
                    move = Key.up
                elif max_pos == 1:
                    move = Key.right
                elif max_pos == 2:
                    move = Key.down
                elif max_pos == 3:
                    move = Key.left     
            details = playg.next_game_state(pygame, move)
            details = self.normalize(details)
            count += 1
            #playg.endGame(pygame)
        score = playg.return_score()
        return score
    
    '''
    Funciton to normalize the input from the game state.
    number represents list position
    NOTE: that distance to top, bottom, left, right will be set to zero based 
    on its corresponding 'opposite' as you die making this move in the game.
    0: direction 0 to 3 (discrete integers) For simplicity and easy access to get key input this is kept the same. out of 3.
    1: Distance to top (divide by 600)
    2: Distance to bottom  (height = 600) (divide by 600)
    3: Distance to right (divide by 800)
    4: Distance to left (width = 800) (divide by 800)
    5: Distance to apple (by pythag thm sqrt(800^2 + 600^2) = 1000) (divide by 1000)
    6: Angle to apple (from positive to negative 180 degrees) (divide by 180)
    '''
    def normalize(self, details):
        details[1] /= 600
        details[2] /= 600
        details[3] /= 800
        details[4] /= 800
        details[5] /= 1000
        details[6] /= 180
        return details
    '''
    Function that returns hypothesis with the highest fitness. 
    '''
    def highest_fitness(self):
        max_pos = 0
        max_num = 0
        for i in range(len(self.fitness_list)):
            if self.fitness_list[i] > max_num:
                max_pos = i
                max_num = self.fitness_list[i]
        if max_num > self.global_best:
            self.global_best = max_num
            self.global_best_ANN = self.P[max_pos]
    
    '''
    Function to return the highest fitness (top score).
    '''
    def ret_hf(self):
        return self.global_best
    
    '''
    Function to return the best ANN.
    '''
    def ret_best_ANN(self):
        return self.global_best_ANN
    
    def mutate__(self, ANN):
        ANN.weights1 += (np.random.rand(ANN._in,7) * 0.75 * random.choice([-1, 1]))
        ANN.weights2 += (np.random.rand(7, ANN._out) * 0.75 * random.choice([-1, 1]))
        return ANN
        
'''
Create an extra popualtion class?
'''
        

'''
For snake game need to modify to get various distances. 
Direction snake is heading.
Distance to walls.
Distance to hitting itself. Probably the one thing I need to figure out.
And distance to apple.

For snake game fitness threshold will be max score. e.g stop at 500 score.
'''

'''
Steps:
    
1. Check what I've done works as intended so far
2. Then work on evaluation fucntion (this includes modifying the game to get what I want)
(side note: keep NN with highest fitness overall. Is this score or realtive to its generation?)
'''

def main():
    # add in abililty to get the average. say average out of 5. 
    # becasue one isn't enough to get fair results.
    max_score = 100
    '''
    Note: That some populaiton numbers don't work. /// Need to redo.
    '''
    ga = GeneticAlg(max_score, 52, 0.4, 0.5, 7, 4)
    ga.init_pop()
    #print(ga.size + ga.size_lo*2)
    try:
        while ga.ret_hf() < max_score:
            ga.compute_fitness()
            print(ga.ret_hf())
            ga.create_new_gen()
    except KeyboardInterrupt:
        sys.exit()
        
    
    ## next step is to calcuate the next generation.

main()
    

