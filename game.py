# coding: utf-8

import pygame
from protoobjects import Return, Config, link_to_resource, tuc
from rgame import RGame
from menu import MainMenu
from soundmgr import SoundMenager

class Game(object):
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.init()
        self.config = Config(link_to_resource("config.cfg"))
        self.a_w = self.config.get("width", 640, int)
        self.a_h = self.config.get("height", 480, int)
        self.tryb = 0
        self.fps = 0
        self.keys = pygame.key.get_pressed()
        print self.config.get("fullscreen", 0, int), self.config.get("fullscreen", "e")
        if self.config.get("fullscreen", 0, int):
            self.window = pygame.display.set_mode((self.a_w, self.a_h), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((self.a_w, self.a_h))
        pygame.display.set_caption(self.config.get("caption", "Game", tuc)) 
        self.screen = pygame.display.get_surface() 
        self.bufor = pygame.Surface((self.a_w, self.a_h), pygame.HWSURFACE)
        self.fpsclock = pygame.time.Clock()
        
        self.sound = SoundMenager(["in_the_hall.ogg"])
        self.parts = [RGame(self), MainMenu(self)]
    
    def printt(self, px, py, text, bit = None, size=10, color=(0,0,0), bgcolor=(200,200,200)):
        if bit == None:
            bit = self.bufor
        font = pygame.font.Font(pygame.font.match_font('doesNotExist, Arial'), size)
        text = font.render(text, True, color, bgcolor)
        textRect = text.get_rect()
        textRect.x = px
        textRect.y = py
        bit.blit(text, textRect)
    
    def endframe(self):
        #pygame.event.pump()
        events = pygame.event.get()
        self.keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                self.ch_tryb(0)
            #elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            #    print pygame.display.toggle_fullscreen()
            #elif event.type == pygame.VIDEORESIZE:
            #    self.a_w, self.a_h = event.w, event.h
            #    self.window = pygame.display.set_mode((self.a_w, self.a_h), pygame.RESIZABLE)
            #    self.screen = pygame.display.get_surface() 
            #    self.bufor = pygame.Surface((self.a_w, self.a_h))
            else:
                if self.tryb:
                    self.parts[self.tryb - 1].event(event)
                
        if self.keys[pygame.K_BACKQUOTE]:
            self.printt(self.a_w-18, self.a_h-10, tuc(int(self.fpsclock.get_fps())))

        self.screen.blit(self.bufor, (0,0))
        pygame.display.flip()
        self.bufor.fill((0,0,0))
        self.fpsclock.tick(self.fps)
        #pygame.time.wait(1)
    
    def play(self):
        self.ch_tryb(2)
        while self.tryb:
            self.parts[self.tryb - 1].frame()
            self.endframe()
        self.config.save()

    def ch_tryb(self, nt):
        r = Return()
        if self.tryb:
            r = self.parts[self.tryb - 1].stop()
        self.tryb = nt
        if self.tryb:
            self.parts[self.tryb - 1].start(r)
        print r
                
                
                
                
                
