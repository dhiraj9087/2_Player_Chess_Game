import pygame
from const import *



class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging =False
        self.mouseX = 0
        self.mouseY = 0
        self.intial_row = 0
        self.intial_col = 0

    def update_blit(self,surface):                  ## here we did same what we did in show piece method in game.py
        self.piece.set_texture(size=128)            ##texture
        texture = self.piece.texture

        img = pygame.image.load(texture)            ##img
        img_center = (self.mouseX,self.mouseY)
        self.piece.texture_rect = img.get_rect(center = img_center)


        surface.blit(img,self.piece.texture_rect)     ## blits




    def update_mouse(self,pos):
        self.mouseX,self.mouseY = pos           ## pos = (xcordinate,ycordinate)

    def save_initial(self,pos):
        self.intial_row = pos[1]//SQSIZE
        self.intial_col = pos[0]//SQSIZE

    def drag_piece(self,piece):
        self.piece = piece
        self.dragging=True

    def undrag_piece(self):
        self.piece = None
        self.dragging=False