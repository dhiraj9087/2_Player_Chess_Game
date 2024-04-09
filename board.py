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
        self.square[row_other][1] = Square(row_other,1,Knight(color))
        self.square[row_other][6] = Square(row_other,6,Knight(color))

        # bishops
        self.square[row_other][2] = Square(row_other,2,Bishop(color))
        self.square[row_other][5] = Square(row_other,5,Bishop(color))

        # rooks
        self.square[row_other][0] = Square(row_other,0,Rook(color))
        self.square[row_other][7] = Square(row_other,7,Rook(color))

        #queen
        self.square[row_other][3] = Square(row_other,3,Queen(color))
        self.square[row_other][4] = Square(row_other,4,King(color))

b=Board()
b._create()