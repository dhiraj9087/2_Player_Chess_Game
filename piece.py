import math
import os

class Piece:

    def __init__(self, name, color, value, texture=None, texture_rect = None):
        self.name = name
        self.color = color

        value_sign = 1 if color == "white" else -1   ## white have 1 value sign and black -1 as white is moving in up which is moving toward zero from negative in y axis and black is moving down which moving away from zero in downward dir
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self,size = 80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')
        


    def add_move(self,move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []
        


class Pawn(Piece):

    def __init__(self,color):
        self.dir = -1 if color=='white' else 1
        self.en_passant = False 
        super().__init__('pawn',color,1.0)        # 1.0 is steps for piece

class Knight(Piece):
    def __init__(self,color):
       super().__init__('knight',color,3.0) 


class Bishop(Piece):

    def __init__(self,color):
       super().__init__('bishop',color,3.001)


class Rook(Piece):

    def __init__(self,color):
       super().__init__('rook',color,5.0)


class Queen(Piece):

    def __init__(self,color):
       super().__init__('queen',color,9.0)


class King(Piece):

    def __init__(self,color):
       self.left_rook = None
       self.right_rook= None 
       super().__init__('king',color,math.inf)
    
    def add_move(self, move):
        # print(f"Adding move for King: {move.initial.row},{move.initial.col} to {move.final.row},{move.final.col}")
        super().add_move(move)


 
