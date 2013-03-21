# coding: utf-8

import pygame, random, re
from protoobjects import GamePart, CObj


class ClickArea(object):
    def __init__(self, (px, py, w, h)):
        self.px, self.py, self.w, self.h = (px, py, w, h)
        self.bd = [0,0,0,0,0,0,0,0,0,0]

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            px, py = event.pos # pygame.mouse.get_pos()
            if self.px < px < self.px + self.w and self.py < py < self.py + self.h:
                self.bd[event.button] = 1
                #print self.bd
        if event.type == pygame.MOUSEBUTTONUP:
            r = 0
            px, py = event.pos # pygame.mouse.get_pos()
            if self.px < px < self.px + self.w and self.py < py < self.py + self.h:
                if self.bd[event.button]:
                    r = event.button
            self.bd[event.button] = 0
            #self.bd = [0,0,0,0,0,0,0,0,0,0]
            return r
        
        return None
    
    def get_rect(self):
        return (self.px, self.py, self.w, self.h)
        

class CLabel(CObj):
    def __init__(self, text, (px, py, w, h), fsize = 15, color = (0,0,0), bgcolor = None):
        CObj.__init__(self)
        self.px, self.py, self.w, self.h = (px, py, w, h)
        self.fsize = fsize
        self.color = color
        self.bgcolor = bgcolor
        self.set_text(text)
    
    def set_text(self, text):
        self.text = text.decode('UTF-8')
        font = pygame.font.Font(pygame.font.match_font('doesNotExist, Arial'), self.fsize)
        fb = font.render(self.text, True, self.color, self.bgcolor)
        textRect = fb.get_rect()
        textRect.x = self.w/2-textRect.width/2
        textRect.y = self.h/2-textRect.height/2
        self.bit = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        if self.bgcolor:
            self.bit.fill(self.bgcolor)
        self.bit.blit(fb, textRect)
        #pygame.draw.rect(self.bit, (255,255,255), (0, 0, self.w-1, self.h-1), 2)
        
    def blit(self, bit):
        CObj.blit(self, bit)
        textRect = self.bit.get_rect()
        textRect.x = self.px
        textRect.y = self.py
        bit.blit(self.bit, textRect)
        
        
class CButton(CLabel):
    def __init__(self, OnClick, text, (px, py, w, h), fsize = 15, color = (0,0,0), bgcolor = None):
        CLabel.__init__(self, text, (px, py, w, h), fsize, color, bgcolor)
        self.oc = OnClick
        self.ca = ClickArea((px, py, w, h))
    
    def event(self, event):
        CLabel.event(self, event)
        if self.ca.event(event) == 1:
            self.oc()


class CColorPick(CObj):
    SEQ = (0,64,128,192,255)
    def __init__(self, (px, py, w, h), color = None, bgcolor = None):
        CObj.__init__(self)
        self.px, self.py, self.w, self.h = (px, py, w, h)
        if not color:
            self.randomize_color()
        else:
            self.r, self.g, self.b = color
            self.rc = self.bc = self.gc = 0
        self.bgcolor = bgcolor
        mw = self.w / 8
        mh = self.h / 6
        self.csum = ClickArea((px + mw, py + mh, 6 * mw, 2 * mh))
        self.cr = ClickArea((px + mw, py + 3 * mh, 2 * mw, 2 * mh))
        self.cg = ClickArea((px + 3 * mw, py + 3 * mh, 2 * mw, 2 * mh))
        self.cb = ClickArea((px + 5 * mw, py + 3 * mh, 2 * mw, 2 * mh))
    
    def updateclr(self):
        self.r = self.SEQ[self.rc]
        self.b = self.SEQ[self.bc]
        self.g = self.SEQ[self.gc]
    
    def randomize_color(self):
        l = len(self.SEQ) - 1
        self.rc = random.randint(0, l)
        self.bc = random.randint(0, l)
        self.gc = random.randint(0, l)
        self.updateclr()
    
    def _norm(self, v):
        l = len(self.SEQ)
        while v >= l:
            v -= l
        while v < 0:
            v += l
        return v
        
    def event(self, event):
        CObj.event(self, event)
        if self.csum.event(event) == 1:
            self.randomize_color()
        r = self.cr.event(event)
        if r == 1:
            self.rc = self._norm(self.rc + 1)
            self.updateclr()
        elif r == 3:
            self.rc = self._norm(self.rc - 1)
            self.updateclr()
        r = self.cg.event(event)
        if r == 1:
            self.gc = self._norm(self.gc + 1)
            self.updateclr()
        elif r == 3:
            self.gc = self._norm(self.gc - 1)
            self.updateclr()
        r = self.cb.event(event)
        if r == 1:
            self.bc = self._norm(self.bc + 1)
            self.updateclr()
        elif r == 3:
            self.bc = self._norm(self.bc - 1)
            self.updateclr()
    
        
    def blit(self, bit):
        CObj.blit(self, bit)
        pygame.draw.rect(bit, self.get_color(), self.csum.get_rect(), 0)
        pygame.draw.rect(bit, (self.r,0,0), self.cr.get_rect(), 0)
        pygame.draw.rect(bit, (0,self.g,0), self.cg.get_rect(), 0)
        pygame.draw.rect(bit, (0,0,self.b), self.cb.get_rect(), 0)

    def get_color(self):
        return (self.r, self.g, self.b)
    

class CTextBox(CObj):

    def __init__(self, (px, py, w, h), color=(0,0,0), bgcolor=(240,240,240), border=(0,0,0), bgonactive=(255,255,255), maxchars=None, text_size=15, text="", allow_number=True, allow_letter=True, allow_special=True):
        CObj.__init__(self)
        self.px, self.py, self.w, self.h = (px, py, w, h)
        self.on = 1
        self.text = text.decode('UTF-8')
        self.maxchars = maxchars
        self.border = border
        self.color = color
        self.bgcolor = bgcolor
        self.onactive = bgonactive
        self.text_size = text_size
        self.anumber = allow_number
        self.aletter = allow_letter
        self.aspecial = allow_special
        self.bit = pygame.Surface((self.w, self.h))
        self.font = pygame.font.Font(pygame.font.match_font('doesNotExist, Arial'), self.text_size)
        self.e = None
        self.charw = 9
        self.selected = False
        self.ca = ClickArea((self.px, self.py, self.w, self.h))
        self.pos_ = (0, 0)
        self.updatebit()


    def event(self, event):
        CObj.event(self, event)
        r = self.ca.event(event)
        if r == 1:
            self.selected = True
            self.updatebit()
        elif r == 0: 
            self.selected = False
            self.updatebit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0:
                    if self.selected:
                        self.text = self.text.decode('UTF-8')[:-1].decode('UTF-8')
                        self.updatebit()
            elif event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.selected = False
                self.updatebit()
            else:
                if self.selected:
                    if (self.anumber or not len(re.findall("\d", event.unicode))) and (self.aletter or not len(re.findall("[a-zA-Z]", event.unicode))) and (self.aspecial or len(re.findall("[0-9a-zA-Z]", event.unicode))):
                        if self.maxchars is None or len(self.text) < self.maxchars:
                            self.text += event.unicode#.decode('UTF-8')
                            self.text.decode('UTF-8')
                            #"".
                            #self.text.join(event.unicode.decode('UTF-8'))
                            self.updatebit()    
    
    def blit(self, bit):
        CObj.blit(self, bit)
        bit.blit(self.bit, (self.px, self.py))
        if self.selected and pygame.time.get_ticks() % 1500 < 800:
            ren = self.font.render("|", 1, self.color)
            bit.blit(ren, self.pos_)
        
            
    def updatebit(self):
        if not self.selected:
            #pygame.draw.rect(self.bit, self.bgcolor, (self.px, self.py, self.w, self.h))
            self.bit.fill(self.bgcolor)
        else:
            #pygame.draw.rect(self.bit, self.onactive, (self.px, self.py, self.w, self.h))
            self.bit.fill(self.onactive)
            if self.border:
                pygame.draw.rect(self.bit, self.border, (self.px, self.py, self.w, self.h), 1)
        lt = 0
        while self.font.size((self.text[lt:] + "|").decode('UTF-8'))[0] > self.w + 1:
            lt += 1
        ren = self.font.render(self.text[lt:].decode('UTF-8'), 1, self.color)
        textRect = ren.get_rect()#topleft = (self.px, self.py))
        #textRect.x = self.w/2-textRect.width/2
        textRect.y = self.h/2-textRect.height/2
        self.pos_ = (self.px + textRect.width, self.py + textRect.y)
        self.bit.blit(ren, textRect)
    
    def get_text(self):
        return self.text.decode('UTF-8')
          
    
class CPlayer(object):
    def __init__(self, idd, name, color, px, py):
        self.tryb = 0
        self.id = idd
        self.name = str(name)
        #self.b = CButton(self.click, "Gracz " + str(iid), (px, py, 100, 40), 20, (255,255,255), (0,0,0))
        self.b = CTextBox((px, py, 100, 40), (255,255,255), (0,0,0), (255,255,255), (100,100,100), None, 20, self.name, 1, 1, 1)
        self.l = CButton(self.click, "", (px + 120, py, 100, 40), 20, (255,255,255), (0,0,0))
        self.r = CButton(self.click, "", (px + 240, py, 100, 40), 20, (255,255,255), (0,0,0))
        self.c = CColorPick((px + 360, py, 80, 40), color = color, bgcolor = (0,0,0))
        self.kl = None
        self.kr = None
        
    
    def click(self):
        #print "elo", self.id
        self.tryb = 1
        self.l.set_text("???")
    

    def event(self, event):
        self.b.event(event)
        self.l.event(event)
        self.r.event(event)
        self.c.event(event)
        if self.tryb:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.tryb = 0
                    self.l.set_text("")
                    self.r.set_text("")
                    self.kl = None
                    self.kr = None
                elif self.tryb == 1:
                    self.tryb = 2
                    self.kl = event.key
                    k = pygame.key.name(event.key)
                    k = k[0].upper() + k[1:].lower()
                    self.l.set_text(k)
                    self.r.set_text("???")
                elif self.tryb == 2:
                    self.tryb = 0
                    self.kr = event.key
                    k = pygame.key.name(event.key)
                    k = k[0].upper() + k[1:].lower()
                    self.r.set_text(k)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.tryb = 0
                self.l.set_text("")
                self.r.set_text("")
                self.kl = None
                self.kr = None
                
    def blit(self, bit):
        self.b.blit(bit)
        self.l.blit(bit)
        self.r.blit(bit)
        self.c.blit(bit)
        
    def get_state(self):
        return (self.id, self.b.get_text(), self.c.get_color(), self.kl, self.kr)
    

def clr(s):
    t = s.split(",")
    return (int(t[0]), int(t[1]), int(t[2]))
        
        
class MainMenu(GamePart):
    def __init__(self, topgame):
        GamePart.__init__(self, topgame)
        self.g = []
        self.g.append(CLabel(self.tg.config.get("m_left", "Left", unicode), (170, 50, 100, 40), 20, (255,255,255), (0,0,0)))
        self.g.append(CLabel(self.tg.config.get("m_right", "Right", unicode), (290, 50, 100, 40), 20, (255,255,255), (0,0,0)))
        self.g.append(CLabel(self.tg.config.get("m_color", "Color", unicode), (410, 50, 80, 40), 20, (255,255,255), (0,0,0)))
        self.g.append(CButton(self.wyjdz, self.tg.config.get("m_exit", "Exit", unicode), (1000, 580, 200, 50), 30, (255,255,255), (0,0,0)))
        self.g.append(CButton(self.graj, self.tg.config.get("m_play", "Play", unicode), (1000, 650, 200, 50), 30, (255,255,255), (0,0,0)))
        #self.g.append(CTextBox((900, 100, 100, 40), maxchars = 55, text_size = 20))
        self.p = []
        for x in xrange(1, 11):
            self.p.append(CPlayer(x, self.tg.config.get("g" + str(x) + "n", "Player" + str(x), unicode), self.tg.config.get("g" + str(x) + "c", None, clr), 50, x*60 + 50))
        
    
    def graj(self):
        self.tg.ch_tryb(1)
        
    def wyjdz(self):
        self.tg.ch_tryb(0)
        
    def start(self, data):
        GamePart.start(self, data)
        pygame.key.set_repeat(500, 100)
        self.tg.sound.get("in_the_hall").play(-1)
        
    def stop(self):
        r = GamePart.stop(self)
        pygame.key.set_repeat()
        self.tg.sound.get("in_the_hall").stop()
        for p in self.p:
            s = p.get_state()
            self.tg.config.add("g" + str(s[0]) + "n", s[1])
            self.tg.config.add("g" + str(s[0]) + "c", str(s[2][0]) + "," + str(s[2][1]) + "," + str(s[2][2]))
            if s[3] and s[4]:
                r.add(s[0], s)
        return r
    
    def pause(self):
        GamePart.pause(self)
    
    def unpause(self):
        GamePart.unpause(self)
        
    def frame(self):
        self.tg.bufor.fill((150,150,150))
        GamePart.frame(self)
        for x in self.g:
            x.blit(self.tg.bufor)
        for p in self.p:
            p.blit(self.tg.bufor)
        
    def event(self, e):
        GamePart.event(self, e)
        if not self.paused:
            for x in self.g:
                x.event(e)
            for p in self.p:
                p.event(e)