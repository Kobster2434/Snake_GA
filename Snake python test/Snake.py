import pygame
from pygame import *
import win32api, win32console, win32gui, codecs
import time, random
from pygame.sprite import Sprite
import numpy as np
import math
from pynput.keyboard import Key, Controller

class playgame:
    
    def __init__(self, pygame):
        self.score = 0
        self.keyboard = Controller()
        
        # leave out below if don't want window to show.
        win = win32console.GetConsoleWindow()
        win32gui.ShowWindow(win,0)
        
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.red = (255,0,0)
        self.green = (0,155,0)
        
        self.display_width = 800
        self.display_height = 600
        
        self.gameDisplay=pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption("Flafel")
        
        icon=pygame.image.load("apple.png")
        pygame.display.set_icon(icon)
        
        self.img=pygame.image.load("snakehead.png")
        self.appleimg=pygame.image.load("apple.png")
        
        self.clock = pygame.time.Clock()
        
        self.AppleThickness=30
        self.block_size = 20
        self.FPS = 15
        
        self.direction="right"
        
        self.smallfont = pygame.font.SysFont("comicsansms",25)
        self.medfont = pygame.font.SysFont("comicsansms",50)
        self.largefont = pygame.font.SysFont("comicsansms",80)
        
        pygame.mixer.init()
    
    def get_pixel_array(self):
        self.pixel_list = [] # 1-D.
        for i in range(800):
            for j in range(600):
                self.pix_int = self.gameDisplay.get_at((i, j))
                for k in range(len(self.pix_int)):
                    self.pixel_list.append(str(self.pix_int[k]))
        return self.pixel_list

    def pythag(self, x, y, x_n, y_n):
        width = (x - x_n)
        height = (y - y_n)
        distance = np.sqrt((width*width)+(height*height))
        angle = np.arcsin(float(height)/float(distance))
        return [distance, angle]

    def getLines(self, snakeList, x, y):
        line = [[],[]]
        for i in range(len(snakeList)):  # To make more effivient combibe this with below.
            line[0].append(snakeList[i][0])  ####
            line[1].append(snakeList[i][1])  ####
        hor_lines = []
        vert_lines = []
        #print(line)
        start1 = 0
        start2 = 0
        for i in range(len(line[0])):
            if i == 0:  ## my issue is one big line. for whole coode section
                start1 = (line[0][i], line[1][i])
                start2 = (line[0][i], line[1][i])
                continue            
            if int(line[0][i]) != int(line[0][i-1]):
                if start1[0] != line[0][i-1] or start1[1] != line[1][i-1]:
                    vert_lines.append([start1, (line[0][i-1], line[1][i-1])])  # change this to append coordinates not number. ----------------------------------------------------------------------------- and below
                start1 = (line[0][i], line[1][i])  # still want on outside.
            elif (int(line[0][i]) == int(line[0][i-1]) and i == (len(line[0])-1)):
                if start1[0] != x or start1[1] != y:
                    vert_lines.append([start1, (x, y)])
            if int(line[1][i]) != int(line[1][i-1]):  # ok b/c len(line[0] = len(line[1]))
                if start2[0] != line[0][i-1] or start2[1] != line[1][i-1]:
                    hor_lines.append([start2, (line[0][i-1], line[1][i-1])])
                start2 = (line[0][i], line[1][i])
            elif (int(line[1][i]) == int(line[1][i-1]) and i == (len(line[0])-1)):
                if start2[0] != x or start2[1] != y:
                    hor_lines.append([start2, (x, y)])
        #print("Horizontal Lines: \n", hor_lines)
        #print("Vertical Lines: \n", vert_lines)
        return hor_lines, vert_lines

    def game_details(self, x, y, direction, snakeList, randApplex, randAppley):    # Also want to add something to store snake location.         
        
        '''
        x, y coordinates of head of snake
         0 1 2 3 4 5 6 x coordinates
        -------------------------
        0|
        1|
        2|
        3|
        4|
        5|
        y coordinates
        '''
        
        ## Below to the snakes body as well.
        head_to_top = y
        head_to_bottom = 600 - y
        head_to_right = 800 - x
        head_to_left = x
        
        hor_lines, vert_lines = self.getLines(snakeList, x, y)
        #print(hor_lines)
        #print(vert_lines)
        
        
        '''
        Get current coordinates and update distance to another line in all directions.
        From this update above
        '''    
        
        for line in hor_lines:
            #head_to_top
            if line[0][1] > y and x >= min(line[0][0], line[1][0]) and x <= max(line[0][0], line[1][0]):
                #print("Reach1")
                distance =  self.pythag(x, y, x, line[0][1]) # returns a list.
                distance = distance[0]
                
                if distance < head_to_bottom:
                    #print("up: ", distance)
                    head_to_bottom = distance
            #head_to_bottom
            if line[0][1] < y and x >= min(line[0][0], line[1][0]) and x <= max(line[0][0], line[1][0]):
                #print("Reach2")
                distance =  self.pythag(x, y, x, line[1][1]) # returns a list.
                distance = distance[0]
                
                if distance < head_to_top:
                    #print("down: ", distance)
                    head_to_top = distance
        
        for line in vert_lines:
            #head_to_right
            if line[0][0] < x and y >= min(line[0][1], line[1][1]) and y <= max(line[0][1], line[1][1]):
                #print("Reach3")
                distance =  self.pythag(x, y, line[1][0], y) # returns a list.
                distance = distance[0]
                
                if distance < head_to_left:
                    #print("right: ", distance)
                    head_to_left = distance
            #head_to_left
            if line[0][0] > x and y >= min(line[0][1], line[1][1]) and y <= max(line[0][1], line[1][1]):
                #print("Reach4")
                distance =  self.pythag(x, y, line[1][0], y) # returns a list.
                distance = distance[0]
                
                if distance < head_to_right:
                    #print("left: ", distance)
                    head_to_right = distance
                
        
        # also change disrance in opposite direction to 0 as you die if you take this move.
        if direction=="right":
            head_to_left = 0
        elif direction=="left":
            head_to_right = 0
        elif direction=="up":
            head_to_bottom = 0
        elif direction=="down":
            head_to_top = 0
    
        current_direction = 0 
        if direction=="right":
            current_direction = 1
        elif direction=="left":
            current_direction = 3
        elif direction=="up":
            current_direction = 0
        elif direction=="down":
            current_direction = 2
        
        distance_angle = self.pythag(x, y, randApplex, randAppley)
        apple_dist = distance_angle[0]
        #apple_angle = distance_angle[1]
        radians = math.atan2(randAppley-y, randApplex-x)
        degrees = math.degrees(radians)
        return [current_direction, head_to_top, head_to_bottom, head_to_right, head_to_left, apple_dist, degrees] 

    def game_intro(self, pygame):
        self.intro=True
        while self.intro:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_c:
                        self.intro=False
                    if event.key==pygame.K_q:
                        pygame.quit()
                        quit()
            self.gameDisplay.fill(self.white)
            
            self.message_to_screen("Welcome to Flafel", self.green, -100,"large")
            self.message_to_screen("The objective of the game is to eat red apples", self.black,-30)
            self.message_to_screen("The more apples you eat,the longer you get",self.black,10)
            self.message_to_screen("If you run into yourself, or the edges, you die!",self.black,50)
            self.message_to_screen("Press C to play, P to pause or Q to quit",self.black,180)
            pygame.display.update()
            self.clock.tick(15)

    def pause(self, pygame):
    
        paused=True
        
        self.message_to_screen("Paused",self.black,-100,size="large")
        self.message_to_screen("Press C to continue or Q to quit",self.black,25)
    
        pygame.display.update()
    
        while paused:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_c:
                        paused=False
                    elif event.key==pygame.K_q:
                        pygame.quit()
                        quit()
            
            self.clock.tick(5)
    
    # Function that displays score in the game. Get error so removed.
    #def score(self, score):
    #    text=self.smallfont.render("Score: "+str(score),True,self.black)
    #    self.gameDisplay.blit(text,[0,0])
    
    def randAppleGen(self):
    
        self.randApplex = round(random.randrange(0,self.display_width-self.AppleThickness))#/10.0)*10.0
        self.randAppley = round(random.randrange(0,self.display_height-self.AppleThickness))#/10.0)*10.0
        

    def snake(self, block_size,snakeList, pygame):
    
        if self.direction=="right":
            head=pygame.transform.rotate(self.img,270)
        if self.direction=="left":
            head=pygame.transform.rotate(self.img,90)
        if self.direction=="up":
            head=self.img
        if self.direction=="down":
            head=pygame.transform.rotate(self.img,180)
    
        self.gameDisplay.blit(head,(snakeList[-1][0],snakeList[-1][1]))
    
        for XnY in snakeList[:-1]:
            pygame.draw.rect(self.gameDisplay, self.green, (XnY[0],XnY[1],block_size,block_size))
    
    def text_objects(self, text,color,size):
        if size=="small":
            textSurface=self.smallfont.render(text,True,color)
        elif size=="medium":
            textSurface=self.medfont.render(text,True,color)
        elif size=="large":
            textSurface=self.largefont.render(text,True,color)
        return textSurface,textSurface.get_rect()
    
    def message_to_screen(self, msg,color,y_displace=0,size="small"):
        textSurf,textRect=self.text_objects(msg,color,size)
        textRect.center=(self.display_width/2),(self.display_height/2)+y_displace
        self.gameDisplay.blit(textSurf,textRect)
    
    
    def play_game(self):    
        self.direction="right"
        self.running = True
        self.gameOver= False
        
        self.lead_x = self.display_width/2
        self.lead_y = self.display_height/2
        
        self.lead_x_change = 10
        self.lead_y_change = 0
        
        self.snakeList=[]
        self.snakeLength=1

        self.randAppleGen()

        
    def next_game_state(self, pygame, move):  # add move back in 3rd for GA.
        if self.gameOver==True:
            pygame.init()
            self.message_to_screen("Game over",self.red,-50,size="large")
            self.message_to_screen("Press C to play again or Q to quit",self.black,50,size="medium")
            pygame.display.update()
            self.keyboard.press('q')
            self.keyboard.release('q')
            self.endGame(pygame)
        
        try:
            self.keyboard.press(move)  # move should already be in a string in the correct format
            self.keyboard.release(move)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.snakeLength <= 2:
                            if self.direction == "right":
                                self.gameOver = True
                        self.direction="left"
                        self.lead_x_change = -self.block_size
                        self.lead_y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        if self.snakeLength <= 2:
                            if self.direction == "left":
                                self.gameOver = True
                        self.direction="right"
                        self.lead_x_change = self.block_size
                        self.lead_y_change = 0
                    elif event.key == pygame.K_UP:
                        if self.snakeLength <= 2:
                            if self.direction == "down":
                                self.gameOver = True
                        self.direction="up"
                        self.lead_y_change = -self.block_size
                        self.lead_x_change = 0
                    elif event.key == pygame.K_DOWN:
                        if self.snakeLength <= 2:
                            if self.direction == "up":
                                self.gameOver = True
                        self.direction="down"
                        self.lead_y_change = self.block_size
                        self.lead_x_change = 0
                    elif event.key==pygame.K_p:
                        self.pause()
        except RuntimeError:
            print("Error!")
        
        if self.lead_x>=self.display_width or self.lead_x<0 or self.lead_y<0 or self.lead_y>=self.display_height:
           self.gameOver=True
        self.lead_x += self.lead_x_change
        self.lead_y += self.lead_y_change
        self.gameDisplay.fill(self.white)

        self.gameDisplay.blit(self.appleimg,(self.randApplex,self.randAppley))

        
        self.snakeHead=[]
        self.snakeHead.append(self.lead_x)
        self.snakeHead.append(self.lead_y)
        self.snakeList.append(self.snakeHead)

        if len(self.snakeList)>self.snakeLength:
            del self.snakeList[0]
        for eachSegment in self.snakeList[:-1]:
            if eachSegment==self.snakeHead:
                self.gameOver=True
                #dead_sound.play()
                
                
        self.snake(self.block_size,self.snakeList, pygame)
        #print(snakeList)

        #self.score(int(self.snakeLength)-1)
        
        details = self.game_details(self.lead_x, self.lead_y, self.direction, self.snakeList, self.randApplex, self.randAppley)
        #print(details)
       
        pygame.display.update()
        

       
        if self.lead_x>self.randApplex and self.lead_x <self.randApplex+self.AppleThickness or self.lead_x+self.block_size>self.randApplex and self.lead_x+self.block_size<self.randApplex+self.AppleThickness:
            if self.lead_y>self.randAppley and self.lead_y <self.randAppley+self.AppleThickness:
                self.randAppleGen()
                self.snakeLength+=1
            elif self.lead_y+self.block_size > self.randAppley and self.lead_y+self.block_size<self.randAppley+self.AppleThickness:
                self.randAppleGen()
                self.snakeLength+=1

        self.clock.tick(self.FPS)
        self.score = self.snakeLength-1
        return details
        
    def return_score(self):
        return self.score
    
    def endGame(self, pygame):
        pygame.quit()
        quit()
    
    def gameOver(self):
        return self.gameOver
    
    def gameRunning(self):
        return self.running

'''
def main():
    pygame.init()
    playg = playgame(pygame)
    playg.play_game()
    while playg.gameRunning() and playg.gameOver == False:
        details = playg.next_game_state(pygame)
        print(details)
    #playg.endGame(pygame)
    score = playg.return_score()
    print(score)

main()
'''