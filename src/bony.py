# coding: utf-8

import random, math, pygame
from protoobjects import Bonus, Define
from player import vxy


@Define(0.1, 3, "speed.png")
class Speed(Bonus):
    def modify(self, p):
        p.v *= 2  
    def unmodify(self, p):
        p.v /= 2

@Define(0.1, 3, "slow.png")        
class Slow(Bonus):
    def modify(self, p):
        p.v /= 2.0  
    def unmodify(self, p):
        p.v *= 2.0

@Define(0.1, 3, "invert.png")
class InvertControls(Bonus):
    def modify(self, p):
        p.swichedctrl = not p.swichedctrl
        p.k_l, p.k_r = p.k_r, p.k_l
        p.ll, p.lr = p.lr, p.ll
    def unmodify(self, p):
        p.swichedctrl = not p.swichedctrl
        p.k_l, p.k_r = p.k_r, p.k_l
        p.ll, p.lr = p.lr, p.ll
        
        
@Define(0.1, 3, "unknown.png")
class Unknown(Bonus):
    def __init__(self, maxpx, maxpy, typ):
        Bonus.__init__(self, maxpx, maxpy, typ)
        bl = BonusList[:]
        bl.pop(bl.index(Unknown))
        self.bonus = random.choice(bl)(maxpx, maxpy, typ)
    def modify(self, p):
        return self.bonus.modify(p)
    def unmodify(self, p):
        return self.bonus.unmodify(p)
 
@Define(0.1, 3, "thinner.png")
class Thinner(Bonus):
    def modify(self, p):
        p.size /= 2.0  
    def unmodify(self, p):
        p.size *= 2.0

@Define(0.1, 3, "thicker.png")
class Thicker(Bonus):
    def modify(self, p):
        p.size *= 2.0  
    def unmodify(self, p):
        p.size /= 2.0
 
@Define(0.1, 3, "square.png")
class Square(Bonus):
    def modify(self, p):
        p.square += 1
    def unmodify(self, p):
        p.square -= 1

@Define(0.9, 3, "walkingthroughwalls.png")
class WalkingThroughWalls(Bonus):
    def modify(self, p):
        if self.typ:
            self.game.wtwalls += 1
        else:
            p.wtwalls += 1
    def unmodify(self, p):
        if self.typ:
            self.game.wtwalls -= 1
        else:
            p.wtwalls -= 1
 
@Define(0.1, 10, "invulnerability.png")
class Invulnerability(Bonus):
    def __init__(self, maxpx, maxpy, game):
        Bonus.__init__(self, maxpx, maxpy, game)
        self.typ = 0
    def modify(self, p):
        p.invulnerability += 1
    def unmodify(self, p):
        p.invulnerability -= 1 
 
@Define(0.1, 0, "clear.png")
class Clear(Bonus):
    def __init__(self, maxpx, maxpy, game):
        Bonus.__init__(self, maxpx, maxpy, game)
        self.typ = 0
    def modify(self, p):
        self.game.background.fill(self.game.bgcolor) 
        
        
@Define(0.9, 0, "laser.png")
class Laser(Bonus):
    def __init__(self, maxpx, maxpy, game):
        Bonus.__init__(self, maxpx, maxpy, game)
        self.typ = 0
    def modify(self, p):
        pkt = []
        r0, r1 = vxy(1500, p.a)
        t0, t1 = vxy(200, p.a + math.pi/2.0)
        pkt.append((int(p.px + t0 / 10.0), int(p.py + t1 / 10.0)))
        pkt.append((int(p.px + t0 + r0), int(p.py + t1 + r1)))
        t0, t1 = vxy(200, p.a - math.pi/2.0)
        pkt.append((int(p.px + t0 + r0), int(p.py + t1 + r1)))
        pkt.append((int(p.px + t0 / 10.0), int(p.py + t1 / 10.0)))
        pygame.gfxdraw.filled_polygon(self.game.background, pkt, self.game.bgcolor)
 
 
        
BonusList = [
         Speed,
         Slow,
         InvertControls,
         Unknown,
         Thinner,
         Thicker,
         Square,
         WalkingThroughWalls,
         Invulnerability,
         Clear,
         Laser,
         
         ]

def AddBony(maxpx, maxpy, game):
    r = []
    for b in BonusList:
        if b.chance > random.random():
            r.append(b(maxpx, maxpy, game))
    return r
