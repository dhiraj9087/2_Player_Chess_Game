import pygame
from board import Board
from const import *
from square import Square
from piece import *
from dragger import *
from config import Config

class Game:
    
    def __init__(self) -> None:
        self.next_player = 'white'
        self.hovered_square = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    ## these are methods to display

    def show_bg(self,surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2==0 else theme.bg.dark
                # if (row + col) % 2==0:
                #     color = (234,235,200)    # light green color
                # else:
                #     color = (119,154,88)     # dark green
                    
                rect = (col*SQSIZE,row*SQSIZE,SQSIZE,SQSIZE)

                pygame.draw.rect(surface,color,rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)
                
    def show_pieces(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    ## all except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)                            ## taking image from assests

                        img_center = col * SQSIZE + SQSIZE// 2, row * SQSIZE + SQSIZE// 2   ## image center

                        piece.texture_rect  = img.get_rect(center = img_center)      ## 
                        surface.blit(img,piece.texture_rect)                                ## to draw one img on other 

    def show_moves(self,surface):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                #color
                color = theme.moves.light if (move.final.row + move.final.col)%2==0 else theme.moves.dark

                ## rect  
                rect = (move.final.col*SQSIZE , move.final.row*SQSIZE,SQSIZE,SQSIZE)

                ## blits
                pygame.draw.rect(surface,color,rect)

    def show_last_move(self,surface):
        theme = self.config.theme

        if self.board.last_move:
            initial= self.board.last_move.initial
            final= self.board.last_move.final

            for pos in [initial,final]:
                #color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark

                ## rect  
                rect = (pos.col*SQSIZE, pos.row*SQSIZE, SQSIZE, SQSIZE)

                ## blits
                pygame.draw.rect(surface,color,rect)


    def show_hover(self,surface):
        if self.hovered_square :
            #color
            color = (180,180,180) 

            ## rect  
            rect = (self.hovered_square.col*SQSIZE, self.hovered_square.row*SQSIZE, SQSIZE, SQSIZE)

            ## blits
            pygame.draw.rect(surface,color,rect,width=3)


    # other methods 
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self,row,col):
        if Square.in_range(row,col):
            self.hovered_square = self.board.squares[row][col]


    def change_theme(self):
        self.config.change_theme()

    def play_sound(self,captured = False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def check_end_condition(self):
        white_king = any(piece.name == 'king' and piece.color == 'white' for row in self.board.squares for piece in row if piece and isinstance(piece, Piece))
        black_king = any(piece.name == 'king' and piece.color == 'black' for row in self.board.squares for piece in row if piece and isinstance(piece, Piece))
        
        if not white_king:
            self.result = "Black wins!"
        elif not black_king:
            self.result = "White wins!"
        elif not any(piece.moves for row in self.board.squares for piece in row if piece and isinstance(piece, Piece)):
            self.result = "Draw!"

    def show_result(self, surface):
        if self.result:
            font = pygame.font.SysFont('Arial', 50)
            text_surface = font.render(self.result, True, (255, 0, 0))
            rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            surface.blit(text_surface, rect)


    def reset(self):
        self.__init__()

    