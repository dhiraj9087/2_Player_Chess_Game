from const import *
from square import Square
from piece import *

class Board:
    
    def __init__(self) -> None:
        self.square = [[0,0,0,0,0,0,0,0] for _ in range(COLS)]

        self._create()

    def _create(self):        # undersocere to show thes methods are private methods  
        

        for row in range(ROWS):
            for col in range(COLS):
                self.square[row][col] = Square(row,col)

        # print(self.square)


    def _add_piece(self,color):
        if color=='white':
            row_pawn, row_other = (6,7)
        else:
            row_pawn,row_other = (1,0)

        #pawns
        for col in range(COLS):
            self.square[row_pawn][col] = Square(row_pawn,col,Pawn(color))

        ##knights
        

b=Board()
b._create()