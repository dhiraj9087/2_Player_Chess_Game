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
        
        def pawn_moves():
            if piece.moved:
                steps = 1   
            else:
                steps = 2                               ## means pawn is on staring position

            ## vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1+steps))
            for possible_move_row in range(start,end,piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        ## create initial and final move squares
                        initial = Square(row, col)
                        final =Square(possible_move_row,col)
                        move=Move(initial,final)
                        piece.add_move(move)
                    # blocked
                    else:
                        break
                # not in range
                else:
                    break

            ## diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1,col+1]

            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        ## create initial 
                        initial = Square(row,col)
                        final = Square(possible_move_row,possible_move_col)

                        ## create new move
                        move = Move(initial,final)
                        ## append new move

                        piece.add_move(move)


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

        def starightline_moves(incrs):
            for incr in incrs:
                row_incr,col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr 
                while True:
                    if Square.in_range(possible_move_row,possible_move_col):
                        # create squares of possible new move 
                        initial = Square(row,col)
                        final  = Square(possible_move_row,possible_move_col)
                        move = Move(initial,final)

                        # empty
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # create new move
                            piece.add_move(move)
                            

                        # has enemy pieces  = add move then  break
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # create new move
                            piece.add_move(move)
                            break
                        # has team piece = break
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    else:
                        break       # not in range

                    possible_move_row += row_incr
                    possible_move_col += col_incr

        if isinstance(piece,Pawn):                      ## same as piece.name == 'Pawn
            pawn_moves()

        elif isinstance(piece,Knight):
            knight_moves()

        elif isinstance(piece,Bishop):
            starightline_moves([
                (-1,1), ## up-right
                (-1,-1),  ##up-left
                (1,1), ## down-right
                (1,-1) ## down- left

            ])
        elif isinstance(piece,Rook):
            starightline_moves([
                (-1,0), #up
                (0,1),  #right
                (1,0),  #down
                (0,-1)  #left
            ])
        elif isinstance(piece,Queen):
            starightline_moves([
                (-1,1), ## up-right
                (-1,-1),  ##up-left
                (1,1), ## down-right
                (1,-1), ## down- left
                (-1,0), #up
                (0,1),  #right
                (1,0),   #down
                (0,-1)  #left
            ])
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
        # self.squares[4][5] = Square(4,5,Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other,0,Rook(color))
        self.squares[row_other][7] = Square(row_other,7,Rook(color))

        #queen and king 
        self.squares[row_other][3] = Square(row_other,3,Queen(color))
        # self.squares[4][3] = Square(4,3,Queen(color))
        self.squares[row_other][4] = Square(row_other,4,King(color))

b=Board()
b._create()