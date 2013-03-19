# coding: utf-8

import pygame, time
#from pygame.locals import * 
from player import Player
from bony import AddBony
from protoobjects import GamePart
 


class RGame(GamePart):
    def __init__(self, topgame):
        GamePart.__init__(self, topgame)
        self.a_w, self.a_h = topgame.a_w, topgame.a_h
        self.background = pygame.Surface((self.a_w, self.a_h))
        self.bgcolor = (20,20,20, 255)
        self.mtim = 0 # timer
        self.wtwalls = 0
        self.wallthc = 4
        self.bony = []
        self.players = []
        
    def start(self, data):
        GamePart.start(self, data)
        self.background.fill(self.bgcolor)
        for k, v in data.get().iteritems():
            self.players.append(Player(v[2], 200, 200, 1.0, v[3], v[4]))
        #self.players.append(Player((200,0,0), 200, 200, 1.0, pygame.K_LEFT, pygame.K_RIGHT))
        #self.players.append(Player((0,200,0), 200, 300, 1.0, pygame.K_a, pygame.K_d))
        #self.players.append(Player((0,0,200), 200, 300, 1.0, pygame.K_a, pygame.K_d))
        #self.players.append(Player((0,200,200), 200, 300, 1.0, pygame.K_a, pygame.K_d))
        self.unpause()
        
    def unpause(self):
        GamePart.unpause(self)
        pygame.time.set_timer(26, 1000)
        self.mtim = pygame.time.get_ticks()
        
    def pause(self):
        GamePart.pause(self)
        pygame.time.set_timer(26, 0)
        self.mtim = -2**30
    
    def frame(self):
        GamePart.frame(self)
        self.tg.bufor.blit(self.background, (0,0))
        
        atim = pygame.time.get_ticks()
        while self.mtim < atim: # pętla timerów
            if self.mtim < atim:
                for p in self.players:
                    p.move(self)
                    
                    x = 0 # bony
                    while x < len(self.bony):
                        if self.bony[x].colide(p):
                            b = self.bony.pop(x)
                            if b.typ:
                                for pp in self.players:
                                    pp.add_bon(b)
                                p.delete_bon(len(p.bony) - 1)
                            else:
                                p.add_bon(b)
                            continue                        
                        x += 1
                        
                self.mtim += 10                   
            atim = pygame.time.get_ticks()
        if (not self.wtwalls) or pygame.time.get_ticks() % 600 < 300:
            pygame.draw.rect(self.tg.bufor, (255,255,0), (0, 0, self.a_w, self.a_h), self.wallthc + 1)
        for p in self.players:
            p.rysuj(self.tg.bufor)
        for b in self.bony:
            b.draw(self.tg.bufor)

    def event(self, event):
        GamePart.event(self, event)
        if event.type == Player.DEATH:
            print "Dead", event.dead.color
            sm = 0
            for p in self.players:
                if p.alive:
                    p.score += 1
                    sm += 1
                    
            if sm <= 1:
                self.background.fill(self.bgcolor)
                self.bony = []
                self.pause()
                
                
                for x in self.players:
                    if x.alive:
                        font = pygame.font.Font(pygame.font.match_font('doesNotExist, Arial'), 20)
                        fb = font.render("Win: " + str(x.color), True, (0,0,0), x.color)
                        textRect = fb.get_rect()
                        textRect.x = self.a_w/2-textRect.width/2
                        textRect.y = self.a_h/2-textRect.height/2
                        self.tg.bufor.blit(fb, textRect)
                        self.tg.screen.blit(self.tg.bufor, (0,0))
                        pygame.display.flip()
                
                
                print "Wyniki:"
                for p in self.players:
                    print p.color, ":", p.score
                    p.shuffle(self.a_w, self.a_h)
                    
                
                
                
                time.sleep(3)
                self.unpause()
                    
        elif event.type == 26:
            self.bony.extend(AddBony(self.a_w, self.a_h, self))
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.tg.ch_tryb(2)
            
            
            
    def stop(self):
        r = GamePart.stop(self)
        r.add("returned", "Nothing")
        
        self.bony = []
        self.pause()
        self.players = []
        return r