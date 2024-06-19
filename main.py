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
        clock = pygame.time.Clock()
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
            game.show_hover(screen)

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
                            print(f"Piece clicked:---> {piece}")
                            # print(f"Square clicked: {(clicked_row,clicked_col)}")
                            for move in piece.moves:
                                print(f"Move to------> ({move.final.row}, {move.final.col})")
                            # print(f"Piece moves:---> {piece.moves}")
                            
                            if isinstance(piece, King):
                                print("Valid Moves for King:")
                                for move in piece.moves:
                                    print(f"Move to -->>> ({move.final.row}, {move.final.col})")


                            board.calc_moves(piece,clicked_row,clicked_col,bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                elif event.type==pygame.MOUSEMOTION:         ## mouse motion
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE


                    game.set_hover(motion_row,motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
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
                            captured =  board.squares[released_row][released_col].has_piece()
                            # sound
                            game.play_sound(captured)

                            board.move(dragger.piece,move)

                            board.set_true_en_passant(dragger.piece)

                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            # next player turn 
                            game.next_turn()

                    dragger.undrag_piece()

                elif event.type == pygame.KEYDOWN:           # key pressed
                    
                    # chnaging themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                    if event.key == pygame.K_r:
                        game.reset()
                        # screen = self.screen
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                elif event.type==pygame.QUIT:                ## quit application
                    pygame.quit()
                    sys.exit()

            # game.check_end_condition()  # Check the end condition
        
            # # Drawing
            # game.show_bg(screen)
            # game.show_last_move(screen)
            # game.show_moves(screen)
            # game.show_pieces(screen)
            # game.show_hover(screen)
            # game.show_result(screen)  # Show the result if the game is over

            # pygame.display.flip()
            # clock.tick(60)

            
            pygame.display.update()

main = Main()
main.mainloop()

# main.py
# import pygame
# import sys
# from const import *
# from game import Game
# from square import *
# from move import *
# from board import *
# from ai_player import AIPlayer

# class Main:
#     def __init__(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
#         pygame.display.set_caption("Chess")
#         self.game = Game()
#         self.ai_player = AIPlayer()  # Initialize the AI player

#     def mainloop(self):
#         screen = self.screen
#         game = self.game
#         board = self.game.board
#         dragger = self.game.dragger

#         while True:
#             game.show_bg(screen)
#             game.show_last_move(screen)
#             game.show_moves(screen)
#             game.show_pieces(screen)
#             game.show_hover(screen)

#             if dragger.dragging:
#                 dragger.update_blit(screen)

#             for event in pygame.event.get():
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     dragger.update_mouse(event.pos)

#                     clicked_row = dragger.mouseY // SQSIZE
#                     clicked_col = dragger.mouseX // SQSIZE

#                     if board.squares[clicked_row][clicked_col].has_piece():
#                         piece = board.squares[clicked_row][clicked_col].piece
#                         if piece.color == game.next_player:
#                             board.calc_moves(piece, clicked_row, clicked_col, bool=True)
#                             dragger.save_initial(event.pos)
#                             dragger.drag_piece(piece)
#                             game.show_bg(screen)
#                             game.show_last_move(screen)
#                             game.show_moves(screen)
#                             game.show_pieces(screen)

#                 elif event.type == pygame.MOUSEMOTION:
#                     motion_row = event.pos[1] // SQSIZE
#                     motion_col = event.pos[0] // SQSIZE

#                     game.set_hover(motion_row, motion_col)

#                     if dragger.dragging:
#                         dragger.update_mouse(event.pos)
#                         game.show_bg(screen)
#                         game.show_last_move(screen)
#                         game.show_moves(screen)
#                         game.show_pieces(screen)
#                         game.show_hover(screen)
#                         dragger.update_blit(screen)

#                 elif event.type == pygame.MOUSEBUTTONUP:
#                     if dragger.dragging:
#                         dragger.update_mouse(event.pos)

#                         released_row = dragger.mouseY // SQSIZE
#                         released_col = dragger.mouseX // SQSIZE

#                         initial = Square(dragger.intial_row, dragger.intial_col)
#                         final = Square(released_row, released_col)
#                         move = Move(initial, final)

#                         if board.valid_move(dragger.piece, move):
#                             captured = board.squares[released_row][released_col].has_piece()
#                             game.play_sound(captured)
#                             board.move(dragger.piece, move)
#                             game.show_bg(screen)
#                             game.show_last_move(screen)
#                             game.show_pieces(screen)
#                             game.next_turn()

#                     dragger.undrag_piece()

#                 elif event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_t:
#                         game.change_theme()

#                     if event.key == pygame.K_r:
#                         game.reset()
#                         game = self.game
#                         board = self.game.board
#                         dragger = self.game.dragger

#                 elif event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()

#             # AI Player's turn
#             if game.next_player == 'black':
#                 ai_move = self.ai_player.get_best_move(board)
#                 if ai_move is not None:
#                     board.move(ai_move.piece, ai_move.move)
#                     game.play_sound()
#                     game.next_turn()

#             pygame.display.update()

# main = Main()
# main.mainloop()
