# coding: utf-8

import pygame, sys, os
from pygame.locals import *
import re

class button :
    def __init__(self, (pxt, pyt, wt, ht), cl1t, cl2t, tclt, textt, size=10, rk=0):
        self.on=1
        self.px=pxt
        self.py=pyt
        self.w=wt
        self.h=ht
        self.cl1=cl1t
        self.cl2=cl2t
        self.tcl=tclt
        self.text=str(textt)
        self.onm=self.cl=0
        self.m_k=rk
        self.size=size
        self.c1=self.c2=pygame.Surface((self.w, self.h))
        self.render()
        
    
    def render(self):
        font = pygame.font.Font(pygame.font.match_font('doesNotExist,Arial'), self.size)
        text = font.render(self.text, True, self.tcl, self.cl1)
        text2 = font.render(self.text, True, self.tcl, self.cl2)
        textRect = text.get_rect()
        textRect.x = self.w/2-textRect.width/2
        textRect.y = self.h/2-textRect.height/2
        tmp=pygame.Surface((self.w, self.h))
        tmp2=pygame.Surface((self.w, self.h))
        tmp.fill(self.cl1)
        tmp2.fill(self.cl2)
        tmp.blit(text, textRect)
        tmp2.blit(text2, textRect)
        pygame.draw.rect(tmp, (0,0,0), (0, 0, self.w-1, self.h-1), 2)
        pygame.draw.rect(tmp2, (0,0,0), (0, 0, self.w-1, self.h-1), 2)
        self.c1=tmp
        self.c2=tmp2

    def rysuj(self, surf, mk, bk):
        p=pygame.mouse.get_pos()
        self.cl=0
        r=0
        if self.onm or (p[0]>=self.px and p[0]<=self.px+self.w and p[1]>=self.py and p[1]<=self.py+self.h):
            if not self.onm: r=1
            surf.blit(self.c2,(self.px, self.py, self.w, self.h))
        else: surf.blit(self.c1,(self.px, self.py, self.w, self.h))
        if (self.onm and bk[K_RETURN]) or  (p[0]>=self.px and p[0]<=self.px+self.w and p[1]>=self.py and p[1]<=self.py+self.h and mk[0] and not self.lmk[0]):
            self.onm=0
            self.cl=1
        self.lmk=mk
        return r
      
    def ust(self, rk):
        self.m_k=int(rk)
        self.text=pygame.key.name(int(rk))
        self.render()


class menu:
    def __init__(self, (pxt, pyt, wt, ht), ot, cl1t, cl2t, tclt, size, strzalki=0):
        self.on=1
        self.px=pxt
        self.py=pyt
        self.w=wt
        self.h=ht
        self.cl1=cl1t
        self.cl2=cl2t
        self.tcl=tclt
        self.o=ot
        self.pos=-2
        self.kt=pygame.key.get_pressed()
        self.str=strzalki
        self.but=[]
        self.size=size
      
    def __getitem__(self, key):
        return self.but[key].cl  
    
    def push_back(self, txt, mk=0):
        t=button((self.px, self.py+len(self.but)*(self.h+self.o), self.w, self.h), self.cl1, self.cl2, self.tcl, txt, self.size, mk)
        self.but.append(t)
        #self.but[-1]=button((self.px, self.py+len(self.but)*(self.h+self.o), self.w, self.h), self.cl1, self.cl2, self.tcl, txt, self.size, mk)
        self.but[-1].render()
        
    def rysuj(self, surf, mk, bk):
        x=0
        xlen=len(self.but)
        while x<xlen:
            self.but[x].cl=0
            self.but[x].onm=0
            if self.str:
                if x==self.pos: self.but[x].onm=1
                if x==self.pos and bk[K_RETURN]: self.but[x].cl=1
            if self.but[x].rysuj(surf, mk, bk): self.pos=-2
            x+=1
        if bk[K_DOWN] and not self.kt[K_DOWN]:
            if self.pos==-2: self.pos=-1
            self.pos+=1
          
        if bk[K_UP] and not self.kt[K_UP]: self.pos-=1
        if self.pos<-2: self.pos=len(self.but)-1
        if self.pos==-1: self.pos=len(self.but)-1
        if self.pos==len(self.but): self.pos=0
        self.kt=bk
        
        
class textbox:

    def __init__(self, pos, size=(150,20), color=(0,0,0), bgcolor=(240,240,240), border=(0,0,0), bgonactive=(255,255,255), maxchars=None, text_size=15, text="", allow_number=True, allow_letter=True, allow_special=True):
        self.on=1
        self.text=text
        self.pos=pos
        self.size=size
        self.maxchars = maxchars
        self.border=border
        self.color=color
        self.bgcolor=bgcolor
        self.onactive=bgonactive
        self.text_size=text_size
        self.anumber=allow_number
        self.aletter=allow_letter
        self.aspecial=allow_special
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pos)
        self.font = pygame.font.Font(pygame.font.match_font("Courier New"), self.text_size)
        self.e = None
        self.vistext = ""
        self.charw = 9
        self.selected = False


    def getEntered(self):
        if self.e.type == KEYDOWN:
            if self.e.key == K_RETURN:
                return True


    def rysuj(self, surface, mk, bk):
        cr=Rect(0, 0, 1, 1)
        cr.topleft=pygame.mouse.get_pos()
        if self.maxchars is not None:
            self.text = self.text[-self.maxchars:]
            self.vistext = self.text[-self.maxchars:]
        else:
            self.vistext = self.text
        self.vistext = self.vistext[-1*self.text_size+self.selected-1:]
        x = self.pos[0]
        if cr.colliderect(self.rect):
            if mk[0]:
                self.selected = True
        if not cr.colliderect(self.rect):
            if mk[0]:
                self.selected = False
        if not self.selected:
            pygame.draw.rect(surface, self.bgcolor, (self.pos[0],self.pos[1],self.size[0],self.size[1]))
        else:
            pygame.draw.rect(surface, self.onactive, (self.pos[0],self.pos[1],self.size[0],self.size[1]))
        if self.border:
            pygame.draw.rect(surface, self.border, (self.pos[0],self.pos[1],self.size[0],self.size[1]), 1)
        for char in self.vistext:
            ren = self.font.render(char, 1, self.color)
            cw = ren.get_width()
            surface.blit(ren, (x - cw/2 + 5, self.pos[1]))
            x += self.charw
        if self.selected and pygame.time.get_ticks()%1500<800:
            ren = self.font.render("|", 1, self.color)
            surface.blit(ren, (x-self.charw+8, self.pos[1]))


    def update(self, event):
        e = event
        self.e = e
        if e.type == KEYDOWN:
            if e.key not in (K_ESCAPE, K_BACKSPACE, K_RETURN):
                if self.maxchars is not None:
                    if len(self.text) < self.maxchars:
                        if self.selected:
                            if (self.anumber or not len(re.findall("\d", e.unicode))) and (self.aletter or not len(re.findall("[a-zA-Z]", e.unicode))) and (self.aspecial or len(re.findall("[0-9a-zA-Z]", e.unicode))):
                                self.text += e.unicode
                else:
                    if self.selected:
                        if (self.anumber or not len(re.findall("\d", e.unicode))) and (self.aletter or not len(re.findall("[a-zA-Z]", e.unicode))) and (self.aspecial or len(re.findall("[0-9a-zA-Z]", e.unicode))):
                            self.text += e.unicode
            if e.key == K_BACKSPACE:
                if len(self.text) > 0:
                    if self.selected:
                        self.text = self.text[:-1]
                        
                        
class multitextbox():
    def __init__(self, pos, odstep, submit_button_text=None, pion=True, tab=True, size=(150,20), color=(0,0,0), bgcolor=(240,240,240), border=(0,0,0), bgonactive=(255,255,255), maxchars=None, text_size=15, allow_number=True, allow_letter=True, allow_special=True):
        self.on=1
        self.poz=-2
        self.pos=pos
        self.size=size
        if submit_button_text:
            self.sbb=button((pos[0], pos[1], size[0], int(size[1]*1.5)), (200,200,200), (230,230,230), color, submit_button_text, text_size)
        else:
            self.sbb=None
        self.ods=odstep
        self.maxchars = maxchars
        self.border=border
        self.color=color
        self.bgcolor=bgcolor
        self.onactive=bgonactive
        self.text_size=text_size
        self.anumber=allow_number
        self.aletter=allow_letter
        self.aspecial=allow_special
        self.font = pygame.font.Font(pygame.font.match_font("Courier New"), self.text_size)
        self.pion=pion
        self.tab=tab
        self.txt=[]
        self.submit=0
      
    def __getitem__(self, key):
        if key=="sub": 
            if not self.sbb: return 0
            if self.submit:
                self.submit=0
                return 1
            return self.sbb.cl
        return self.txt[key].text  
    
    def push_back(self, txt, mk=0):
        if not self.pion:
            pos=(self.pos[0]+(self.size[0]+self.ods)*len(self.txt), self.pos[1])
            if self.sbb:
                self.sbb.px=self.pos[0]+(self.size[0]+self.ods)*(len(self.txt)+1)
        else:
            pos=(self.pos[0],self.pos[1]+(self.size[1]+self.ods)*len(self.txt))
            if self.sbb:
                self.sbb.py=self.pos[1]+(self.size[1]+self.ods)*(len(self.txt)+1)
        t=textbox(pos, self.size, self.color, self.bgcolor, self.border, self.onactive, self.maxchars, self.text_size, txt, self.anumber, self.aletter, self.aspecial)
        self.txt.append(t)      
        
    def rysuj(self, surf, mk, bk):
        x=0
        xlen=len(self.txt)
        while x<xlen:
            self.txt[x].rysuj(surf, mk, bk)
            x+=1
        if self.sbb:
            self.sbb.rysuj(surf, mk, bk)
        
    def update(self, event):
        sel=-1
        x=0
        xlen=len(self.txt)
        while x<xlen:
            self.txt[x].update(event)
            if self.txt[x].selected:
                sel=x
                self.poz=sel
            x+=1
        #if self.poz>=0:
        #    self.txt[self.poz].selected=1
            
        if sel>=0:
            if event.type == KEYDOWN:
                if event.key == K_TAB:
                    if self.poz==-2: self.poz=-1
                    self.txt[self.poz].selected=0
                    self.poz+=1
                if self.poz<-2: self.poz=len(self.txt)-1
                if self.poz==len(self.txt): self.poz=0 
                self.txt[self.poz].selected=1
            if event.type == KEYUP:
                if event.key==K_RETURN and self.poz==len(self.txt)-1:
                    self.submit=1
        else:
            self.poz=-2


class simgui():
    def __init__(self):
         self.elements={}
    
    def rysuj(self, surf, mk, mb, *args):
        for el in args:
            self.elements[el].rysuj(surf, mk, mb)
    
    def rysuj_on(self, surf, mk, bk):
        for idd in self.elements:
            if self.elements[idd].on:
                self.elements[idd].rysuj(surf, mk, bk)
    
    def update(self, events, *args):
        for event in events:
            for el in args:
                self.elements[el].update(event)

    def update_on(self, event):
        for idd in self.elements:
            if self.elements[idd].__class__ in (textbox, multitextbox) and self.elements[idd].on:
                self.elements[idd].update(event)

    def add(self, ID, element):
        self.elements[ID]=element
    
    def __getitem__(self, key):
        return self.elements[key]
        
    def on(self, *args):
        for idd in self.elements:
            self.elements[idd].on=0 
        for el in args:
            self.elements[el].on=1
    
    def off(self, *args):
        for idd in self.elements:
            self.elements[idd].on=1 
        for el in args:
            self.elements[el].on=0       

