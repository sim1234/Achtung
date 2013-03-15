import pygame, time, math, random, os 

class Bonus(object):
    r = 20
    img_red = pygame.image.load(os.path.join('..', 'data', 'red.png'))
    img_green = pygame.image.load(os.path.join('..', 'data', 'green.png'))
    img = None
    chance = 0.0
    duration = 0.0
    
    def __init__(self, maxpx, maxpy, typ):
        self.px = random.randint(self.r, maxpx - self.r)
        self.py = random.randint(self.r, maxpy - self.r)
        self.typ = typ # 0 - ja; 1 - inni
        self.to = 0
        
    def active(self):
        if self.to == 0:
            self.to = time.clock() + self.duration
        #print self.to, time.clock()
        if self.to > time.clock():
            return 1
        return 0
        
    def colide(self, p):
        if self.r + p.size > math.hypot(self.px - p.px, self.py - p.py):
            return 1
        return 0
    
    def draw(self, bit):
        #pygame.gfxdraw.filled_circle(bit, self.px, self.py, self.r, (255,255,255))
        if self.typ:
            bit.blit(self.img_red, (self.px - self.r, self.py - self.r))
        else:
            bit.blit(self.img_green, (self.px - self.r, self.py - self.r))
        bit.blit(self.img, (self.px - self.r, self.py - self.r))
        
    def modify(self, p): #  override
        pass
        
    def unmodify(self, p): # override
        pass


def Define(chance, duration, src):
    def f(o):
        o.chance = chance
        o.duration = duration 
        o.img = pygame.image.load(os.path.join('..', 'data', src))
        return o
    return f


class Return(object):
    def __init__(self):
        self.data = {}
        
    def add(self, k, d):
        self.data[k] = d
        
    def has(self, k):
        return self.data.has_key(k)
    
    def get(self):
        return self.data
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        r = "<Return object with parameters:"
        for k, v in self.data.iteritems():
            r += " " + str(k) + ":" + str(v) + ";"
        r += ">"
        return r
            

class GamePart(object):
    def __init__(self, topgame):
        self.tg = topgame
        self.paused = 0
        
    def start(self, data):
        pass
    
    def stop(self):
        return Return()
    
    def pause(self):
        self.paused = 1
    
    def unpause(self):
        self.paused = 0
    
    def frame(self):
        pass
    
    def event(self, e):
        pass
    
    
class CObj(object):
    def __init__(self):
        pass
    
    def blit(self, bit):
        pass
    
    def event(self, event):
        pass