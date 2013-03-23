# coding: utf-8

import pygame, time, math, random, os 


def link_to_resource(p):
    return os.path.join('data', p)

def tuc(s):
    try:
        return unicode(s, "UTF-8")
    except:
        try:
            return str(s)
        except:
            return s

class Config(object):
    def __init__(self, path = None):
        self.data = {}
        self.path = path
        if path:
            self.load(path)
        
    def load(self, path):
        self.data = {}
        for l in open(path, "r"):
            try:
                t = l.split(":", 1)
                if t[0]:
                    self.data[t[0]] = tuc(t[1][:-1]) # t[1][:-1].decode('UTF-8')
            except Exception:
                pass
    
    def save(self, path = None):
        keylist = self.data.keys()
        keylist.sort()
        if path:
            self.path = path
        f = open(self.path, "w+")
        f.write("Achtung config\n".encode('UTF-8'))
        for k in keylist:
            f.write(tuc(k).encode('UTF-8'))
            f.write(":".encode('UTF-8'))
            f.write(tuc(self.data[k]).encode('UTF-8'))
            f.write("\n".encode('UTF-8'))
        f.write("\n".encode('UTF-8'))
    
    def add(self, k, d):
        self.data[k] = d
        
    def has(self, k):
        return self.data.has_key(k)
    
    def get(self, k, defv = None, typ = None):
        try:
            if not self.data.has_key(k):
                raise 
            r = self.data[k]
            if typ:
                r = typ(r)
            return r
        except:
            if defv == None:
                raise
            return defv



class Bonus(object):
    r = 20
    img_red = pygame.image.load(link_to_resource('red.png'))
    img_green = pygame.image.load(link_to_resource('green.png'))
    img = None
    chance = 0.0
    duration = 0.0
    
    def __init__(self, maxpx, maxpy, game):
        self.game = game
        self.px = random.randint(self.r, maxpx - self.r)
        self.py = random.randint(self.r, maxpy - self.r)
        self.typ = random.choice([0, 1]) # 0 - ja; 1 - inni
        self.to = 0
        
    def active(self):
        if self.to == 0:
            self.to = time.clock() + self.duration
        #print self.to, time.clock()
        if self.to > time.clock():
            return 1
        return 0
        
    def colide(self, p):
        if p.alive and self.r + p.size > math.hypot(self.px - p.px, self.py - p.py):
            return 1
        return 0
    
    def draw(self, bit):
        #pygame.gfxdraw.filled_circle(bit, self.px, self.py, self.r, (255,255,255))
        if self.typ:
            bit.blit(self.img_red, (self.px - self.r, self.py - self.r))
        else:
            bit.blit(self.img_green, (self.px - self.r, self.py - self.r))
        bit.blit(self.img, (self.px - self.r, self.py - self.r))
        
    def modify(self, p): # override
        pass
        
    def unmodify(self, p): # override
        pass
    
    #def modify_game(self, game): # override
    #    pass
    #
    #def unmodify_game(self, game): # override
    #    pass


def Define(chance, duration, src):
    def f(o):
        o.chance = chance
        o.duration = duration 
        o.img = pygame.image.load(link_to_resource(src))
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
            r += " " + tuc(k) + ":" + tuc(v) + ";"
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