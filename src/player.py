# coding: utf-8

import math, random
import pygame.gfxdraw

def normaliserad(rad): # zamienia podan� liczb� radian�w na liczb� z przedzia�u <0, 2*pi)
    while rad < 0:
        rad += 2*math.pi
    while rad >= 2*math.pi:
        rad -= 2*math.pi
    return rad

def va(vx, vy): # zwraca d�ugo�� i k�t nachylania wektora (pobiera jego sk�adowe x i y)
    vx = float(vx)
    vy = float(vy)
    return (math.sqrt(vx**2 + vy**2), normaliserad(math.atan2(vy,vx)))
    
def vxy(v, a): # zwraca sk�adowe x i y wektora (pobiera jego d�ugo�� i k�t nachylania)
    a = float(a)
    return (v*math.cos(a), v*math.sin(a))


class Player:
    DEATH = 25
    
    def __init__(self, color, px = 0, py = 0, a = 0, k_l = 0, k_r = 0):
        self.px = float(px)
        self.py = float(py)
        self.size = 5
        self.v = float(1.0)
        self.a = normaliserad(a)
        self.k_l = int(k_l)
        self.k_r = int(k_r)
        self.ll = 0
        self.lr = 0
        self.color = color
        self.bony = []
        self.no = 0
        self.alive = 1
        self.score = 0
        self.swichedctrl = 0
        self.square = 0
    
    def shuffle(self, maxpx, maxpy):
        self.a = random.uniform(0, 2*math.pi)
        self.px = random.randint(0, maxpx)
        self.py = random.randint(0, maxpy)
        self.alive = 1
        self.no = 0
        while len(self.bony):
            self.delete_bon(-1)
        
    
    def move(self, dane):
        if self.alive:
            self.check_bon()
            if self.square:
                if dane.tg.keys[self.k_l] and not self.ll:
                    #print "a"
                    self.a -= math.pi/2
                if dane.tg.keys[self.k_r] and not self.lr:
                    self.a += math.pi/2
            else:
                if dane.tg.keys[self.k_l]:
                    self.a -= 0.02
                if dane.tg.keys[self.k_r]:
                    self.a += 0.02 
            self.a = normaliserad(self.a)
            #px, py = self.px, self.py
            t0, t1 = vxy(self.v, self.a)
            self.px += t0
            self.py += t1
            if self.px < 0:
                self.px = dane.a_w
            if self.px > dane.a_w:
                self.px = 0 
            if self.py < 0:
                self.py = dane.a_h
            if self.py > dane.a_h:
                self.py = 0
            for x in xrange(3):
                n = math.sqrt(2)
                if x == 1 or not self.square:
                    n = 1
                t0, t1 = vxy(self.size*n + (1.1 + 1.0/max(0.5, self.v))/2.0, self.a + (x - 1)*math.pi/4)
                t0, t1 = int(self.px + t0), int(self.py + t1)
                if t0 >= 0 and t1 >= 0 and t0 < dane.a_w and t1 < dane.a_h:
                    dane.tg.bufor.set_at((t0, t1), (0,255,0))
                    if dane.background.get_at((t0, t1)) != dane.bgcolor:
                        print "lolz", dane.background.get_at((t0, t1)), t0, t1
                        self.alive = 0
            
            if not self.alive:
                pygame.event.post(pygame.event.Event(self.DEATH, dead = self))
                
            if self.no < 0:
                self.no = random.randint(100, 800)
            if self.no > self.size * 10:
                pkt = []
                t0, t1 = vxy(self.size, normaliserad(self.a + math.pi/2.0))
                pkt.append((int(self.px + t0), int(self.py + t1)))
                t0, t1 = vxy(self.size, normaliserad(self.a - math.pi/2.0))
                pkt.append((int(self.px + t0), int(self.py + t1)))
                t0, t1 = vxy(self.size*math.sqrt(2), normaliserad(self.a - 3*math.pi/4.0))
                pkt.append((int(self.px + t0), int(self.py + t1)))
                t0, t1 = vxy(self.size*math.sqrt(2), normaliserad(self.a + 3*math.pi/4.0))
                pkt.append((int(self.px + t0), int(self.py + t1)))        
                pygame.gfxdraw.filled_polygon(dane.background, pkt, self.color)
                #pygame.gfxdraw.filled_circle(dane.background, int(self.px), int(self.py), int(self.size), self.color)
                #pygame.draw.circle(dane.background, self.color, (int(self.px), int(self.py)), int(self.size))
            self.no -= 1
            self.ll = dane.tg.keys[self.k_l]
            self.lr = dane.tg.keys[self.k_r]
    
    def add_bon(self, b):
        self.bony.append(b)
        b.modify(self)
    
    def delete_bon(self, x):
        #self.bony.pop(self.bony.index(b))
        b = self.bony.pop(x)
        b.unmodify(self)
        
    def check_bon(self):
        x = 0
        while x < len(self.bony):
            if not self.bony[x].active():
                print "elo"
                self.delete_bon(x)
                continue
            x += 1
                
    
    def rysuj(self, bit):
        clr = (200,200,0)
        if self.swichedctrl:
            clr = (0,0,255)
        if self.square:
            pkt = []
            r = self.size * math.sqrt(2)
            p4 = math.pi/4.0
            t0, t1 = vxy(r, normaliserad(self.a - p4))
            pkt.append((int(self.px + t0), int(self.py + t1)))
            t0, t1 = vxy(r, normaliserad(self.a + p4))
            pkt.append((int(self.px + t0), int(self.py + t1)))
            t0, t1 = vxy(r, normaliserad(self.a + 3*p4))
            pkt.append((int(self.px + t0), int(self.py + t1)))
            t0, t1 = vxy(r, normaliserad(self.a - 3*p4))
            pkt.append((int(self.px + t0), int(self.py + t1)))
            pygame.gfxdraw.filled_polygon(bit, pkt, clr)
            pygame.gfxdraw.aapolygon(bit, pkt, clr)
            #pygame.draw.polygon(bit, clr, pkt)
        else:
            pygame.gfxdraw.filled_circle(bit, int(self.px), int(self.py), int(self.size), clr)
            pygame.gfxdraw.aacircle(bit, int(self.px), int(self.py), int(self.size), clr)
            
        
        
        