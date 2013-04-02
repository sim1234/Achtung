# coding: utf-8

import pygame, time
#from pygame.locals import * 
from player import Player
from bony import AddBony, Invulnerability, WalkingThroughWalls
from protoobjects import GamePart, tuc
from menu import CLabel, CButton
 


class RGame(GamePart):
    def __init__(self, topgame):
        GamePart.__init__(self, topgame)
        self.a_w, self.a_h = topgame.a_w - 300, topgame.a_h
        self.background = pygame.Surface((self.a_w, self.a_h))
        self.bgcolor = (20,20,20, 255)
        self.mtim = 0 # timer
        self.wtwalls = 0
        self.wallthc = 4
        self.bony = []
        self.players = []
        self.players2 = []
        self.bexit = CButton(self.wyjdz, self.tg.config.get("m_exit", "Exit", tuc), (1000, 580, 200, 40), 30, (0,0,0), (100,100,100))
        self.bpause = CButton(self.pause, self.tg.config.get("m_pause", "Pause", tuc), (1000, 630, 200, 40), 30, (0,0,0), (100,100,100))
        self.winner = CLabel("Winn", (self.a_w / 2 - 100, self.a_h / 2 - 20, 200, 40), 30, (0,0,0), (0,0,0,0))
        
    
    def wyjdz(self):
        self.tg.ch_tryb(2)
        
    
    def start(self, data):
        GamePart.start(self, data)
        self.background.fill(self.bgcolor)
        for k, v in data.get().iteritems():
            self.players.append(Player(v[2], v[1], 200, 200, 1.0, v[3], v[4]).shuffle(self.a_w, self.a_h))
        self.update_score()
        #self.players.append(Player((200,0,0), 200, 200, 1.0, pygame.K_LEFT, pygame.K_RIGHT))
        #self.players.append(Player((0,200,0), 200, 300, 1.0, pygame.K_a, pygame.K_d))
        #self.players.append(Player((0,0,200), 200, 300, 1.0, pygame.K_a, pygame.K_d))
        #self.players.append(Player((0,200,200), 200, 300, 1.0, pygame.K_a, pygame.K_d))
        #self.unpause()
        self.tg.sound.get("in_the_hall").play(-1)
        self.start_round()
        
    def update_score(self):
        self.players2 = []
        t = self.players[:]
        def s(p1, p2):
            if p2.score >= p1.score:
                return p2.score > p1.score
            return -1
        t.sort(s)
        x = 0
        for p in t:
            self.players2.append(CLabel(tuc(p.name), (1000, 10 + 30 * x, 200, 20), 20, p.color, (100,100,100)))
            self.players2.append(CLabel(tuc(p.score), (1220, 10 + 30 * x, 40, 20), 20, p.color, (100,100,100)))
            x += 1
    
    def start_round(self):
        self.winner.bgcolor = (0,0,0,0)
        self.winner.set_text("")
        self.pause()
        self.bony = []
        self.background.fill(self.bgcolor)
        for p in self.players:
            p.shuffle(self.a_w, self.a_h)
            for b in (Invulnerability, WalkingThroughWalls):
                bb = b(500, 500, self)
                bb.typ = 0
                bb.duration = 4
                p.add_bon(bb)
            for x in xrange(30):
                p.move(self)
        self.call_after(2000, self.unpause)
        
    def end_round(self):
        self.pause()
        for x in self.players:
            if x.alive:
                self.winner.bgcolor = x.color
                self.winner.set_text(tuc(x.name))
        self.call_after(2000, self.start_round)
        
        
    def unpause(self):
        GamePart.unpause(self)
        pygame.time.set_timer(26, 1000)
        self.mtim = pygame.time.get_ticks()
        self.bpause.set_text(self.tg.config.get("m_pause", "Pause", tuc))
        self.bpause.oc = self.pause
        print "unpaused"
        
        
    def pause(self):
        GamePart.pause(self)
        pygame.time.set_timer(26, 0)
        self.mtim = 2**30
        self.bpause.set_text(self.tg.config.get("m_unpause", "Unpause", tuc))
        self.bpause.oc = self.unpause
        print "paused"
    
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
                            self.tg.sound.get("bonus").play()
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
        if (not self.wtwalls) or pygame.time.get_ticks() % 660 < 330:
            pygame.draw.rect(self.tg.bufor, (255,255,0), (0, 0, self.a_w, self.a_h), self.wallthc + 1)
        for p in self.players:
            p.rysuj(self.tg.bufor)
        for b in self.bony:
            b.draw(self.tg.bufor)
        for l in self.players2:
            l.blit(self.tg.bufor)
        self.bexit.blit(self.tg.bufor)
        self.bpause.blit(self.tg.bufor)
        self.winner.blit(self.tg.bufor)

    def event(self, event):
        GamePart.event(self, event)
        self.bexit.event(event)
        self.bpause.event(event)
        self.winner.event(event)
        if event.type == Player.DEATH:
            self.tg.sound.get("death").play()
            print "Dead", event.dead.color
            sm = 0
            for p in self.players:
                if p.alive:
                    p.score += 1
                    sm += 1
            self.update_score()
            if sm <= 1:
                self.end_round()
                    
        elif event.type == 26:
            self.bony.extend(AddBony(self.a_w, self.a_h, self))
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.wyjdz()
            if event.key == pygame.K_SPACE:
                self.bpause.oc()
            
            
    def stop(self):
        r = GamePart.stop(self)
        self.tg.sound.get("in_the_hall").stop()
        #r.add("returned", "Nothing")
        self.pause()
        self.bony = []
        self.players = []
        self.update_score()
        return r