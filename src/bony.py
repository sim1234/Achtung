
import random
from protoobjects import Bonus, Define


@Define(0.9, 3, "speed.png")
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
        #self.bonus.__init__(self, maxpx, maxpy, typ)
        #self.modify = self.bonus.modify
        #self.unmodify = self.bonus.unmodify
    def modify(self, p):
        return self.bonus.modify(p)
    def unmodify(self, p):
        return self.bonus.unmodify(p)
 
@Define(0.9, 10, "thinner.png")
class Thinner(Bonus):
    def modify(self, p):
        p.size /= 2.0  
    def unmodify(self, p):
        p.size *= 2.0

@Define(0.9, 10, "thicker.png")
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
 
 
 
 
 
 
 
        
BonusList = [
         Speed,Speed,Speed,Speed,
         Slow,Slow,Slow,Slow,Slow,
         InvertControls,
         Unknown,
         Thinner,
         Thicker,
         Square,
         
         ]

def AddBony(maxpx, maxpy):
    r = []
    for b in BonusList:
        if b.chance > random.random():
            r.append(b(maxpx, maxpy, random.choice([0, 1])))
    return r
