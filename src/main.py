# coding: utf-8
'''
Created on 01-03-2013

@author: Szymon
'''
import pygame
from game import Game

def main():
    gra = Game(1280, 720)
    #gra = Game(640, 480)
    #gra = Game(1440, 900)
    
    gra.play()

if __name__ == "__main__": 
    main()