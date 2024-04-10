from const import *
from square import *
from piece import *
from move import *

class Board:
    
    def __init__(self) -> None:
        self.squares = [[0,0,0,0,0,0,0,0] for _ in range(COLS)]

        self._create()
        self._add_piece('white')
        self._add_piece('black')

    def calc_moves(self,piece,row,col):                 ## calculate all the possible and valide moves of a specific piece art specific position
        
        def knight_moves():
            ## 8 possible moves if there are all square empty
            possible_moves = [
                (row-2,col+1),
                (row-1,col+2),
                (row+1,col+2),
                (row+2,col+1),
                (row+2,col-1),
                (row+1,col-2),
                (row-1,col-2),
                (row-2,col-1),
            ]

            for move in possible_moves:
                move_row,move_col = move
                if Square.in_range(move_row,move_col):
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                        ## create squares of move
                        initial = Square(row,col)
                        final = Square(move_row,move_col)
                        
                        ## create new move
                        move = Move(initial,final)

                        ##append valid move
                        piece.add_move(move)

        if isinstance(piece,Pawn):                      ## same as piece.name == 'Pawn
            pass

        elif isinstance(piece,Knight):
            knight_moves()

        elif isinstance(piece,Bishop):
            pass
        elif isinstance(piece,Rook):
            pass
        elif isinstance(piece,Queen):
            pass
        elif isinstance(piece,King):
            pass
        



    def _create(self):        # undersocere to show thes methods are private methods  
        

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row,col)

        # print(self.square)


    def _add_piece(self,color):
        if color=='white':
            row_pawn, row_other = (6,7)
        else:
            row_pawn,row_other = (1,0)

        #pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn,col,Pawn(color))

        ##knights
        self.squares[row_other][1] = Square(row_other,1,Knight(color))
        self.squares[row_other][6] = Square(row_other,6,Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other,2,Bishop(color))
        self.squares[row_other][5] = Square(row_other,5,Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other,0,Rook(color))
        self.squares[row_other][7] = Square(row_other,7,Rook(color))

        #queen and king 
        self.squares[row_other][3] = Square(row_other,3,Queen(color))
        self.squares[row_other][4] = Square(row_other,4,King(color))

b=Board()
b._create()