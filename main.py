import pygame
import sys
from const import *
from game import Game
from square import *
from move import *
from board import *

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()
    
    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger


        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                if event.type==pygame.MOUSEBUTTONDOWN:       ## click
                    dragger.update_mouse(event.pos)
                    # print(event.pos)                        ## it is the position we click on board

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():     ## if clicked square has a piece 
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color)?
                        if piece.color == game.next_player:
                                
                            board.calc_moves(piece,clicked_row,clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            #show methods
                            game.show_bg(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                elif event.type==pygame.MOUSEMOTION:         ## mouse motion
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)


            
                elif event.type==pygame.MOUSEBUTTONUP:       ## click release

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE
                        
                        # create poss move
                        initial = Square(dragger.intial_row,dragger.intial_col)
                        final = Square(released_row,released_col)
                        move = Move(initial,final)

                        # valid move?
                        if board.valid_move(dragger.piece,move):
                            board.move(dragger.piece,move)

                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            # next player turn 
                            game.next_turn()

                    dragger.undrag_piece()

                elif event.type==pygame.QUIT:                ## quit application
                    pygame.quit()
                    sys.exit()



            
            pygame.display.update()

main = Main()
main.mainloop()