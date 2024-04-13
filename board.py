from const import *
from square import *
from piece import *
from move import *

class Board:
    
    def __init__(self) -> None:
        self.squares = [[0,0,0,0,0,0,0,0] for _ in range(COLS)]
        self.last_move = None
        self._create()
        self._add_piece('white')
        self._add_piece('black')
    
    def move(self,piece,move):
        initial = move.initial
        final = move.final

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # pawn promotion 
        if isinstance(piece,Pawn):
            self.check_promotion(piece,final)

        # king castling
        if isinstance(piece,King):
            if self.castling(initial,final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff<0) else piece.right_rook
                self.move(rook,rook.moves[-1])

        # move  
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self,piece,move):
        return move in piece.moves

    def check_promotion(self,piece,final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self,initial,final):
        return abs(initial.col - final.col)==2

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
                    if self.squares[move_row][move_col].isempty_or_enemy(piece.color):
                        ## create squares of move
                        initial = Square(row,col)
                        final = Square(move_row,move_col)
                        
                        ## create new move
                        move = Move(initial,final)

                        ##append valid move
                        piece.add_move(move)

        def starightline_moves(incrs):
            for incr in incrs:
                # print(incr)
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

        def king_moves():
            adjs = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]

            for possible_move in adjs:
                # print(possible_move)
                possible_move_row,possible_move_col=possible_move
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        ## create squares of move
                        initial = Square(row,col)
                        final = Square(possible_move_row,possible_move_col)
                        
                        ## create new move
                        move = Move(initial,final)

                        ## append valid move
                        piece.add_move(move)

            # castling moves 
            if not piece.moved:

                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook,Rook):
                    if not left_rook.moved:
                        print("inside not left_rook.moved ")
                        for c in range(1,4):
                            if self.squares[row][c].has_piece():        ## castling not possible as there is a piece between rook and king
                                print("break becue insde has piece ",c)
                                break
                            # else:
                            if c==3:
                                # add left rook to king
                                # print(c,"inside the c==3")
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row,0)
                                final = Square(row,3)
                                move=Move(initial,final)
                                left_rook.add_move(move)
                                # print(c,"inside the c==3")

                                # king move
                                initial = Square(row,col)
                                final = Square(row,2)
                                move=Move(initial,final)
                                # left_rook.add_move(move)
                                piece.add_move(move)
                                # print(c,"inside the c==3")

                                
                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook,Rook):
                    if not right_rook.moved:
                        for c in range(5,7):
                            if self.squares[row][c].has_piece():        ## castling not possible as there is a piece between rook and king
                                break
                            if c==6:
                                # add right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row,7)
                                final = Square(row,5)
                                move=Move(initial,final)
                                right_rook.add_move(move)

                                # king move
                                initial = Square(row,col)
                                final = Square(row,6)
                                move=Move(initial,final)
                                piece.add_move(move)

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
            king_moves()
        



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