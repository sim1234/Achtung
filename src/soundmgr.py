
import pygame
from protoobjects import link_to_resource

class SoundMenager(object):
    def __init__(self, lista):
        pygame.mixer.init()
        self.sounds = {}
        for p in lista:
            try:
                s = pygame.mixer.Sound(link_to_resource(p))
                n = p.split(".")[0]
                self.sounds[n] = s
                print "Loaded", p, "as", n
            except Exception:
                print "Failed to load", p
    
    def get(self, n):
        try:
            return self.sounds[n]
        except Exception as e:
            print e
            return pygame.mixer.Sound()
            
    
    def play(self, n):
        self.get(n).play()
        
    def stop(self, n):
        self.get(n).stop()