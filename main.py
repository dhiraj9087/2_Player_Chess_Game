import pygame
import sys
from const import *
from game import Game
from square import *
from move import *
from board import *
# from stockfish import StockfishEngine
class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Chess")
        clock = pygame.time.Clock()
        self.game = Game()
        # self.ai_player = StockfishEngine(stockfish_path="/opt/homebrew/bin/stockfish")
    
    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        ai = self.game.ai
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

                    pos = event.pos
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():     ## if clicked square has a piece 
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color)?
                        if piece.color == game.next_player:
                            # print(f"Piece clicked:---> {piece}")
                            # print(f"Square clicked: {(clicked_row,clicked_col)}")
                            # for move in piece.moves:
                            #     print(f"Move to------> ({move.final.row}, {move.final.col})")
                            # print(f"Piece moves:---> {piece.moves}")
                            
                            # if isinstance(piece, King):
                            #     # print("Valid Moves for King:")
                            #     for move in piece.moves:
                            #         print(f"Move to -->>> ({move.final.row}, {move.final.col})")


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

                            if game.gamemode == "ai":
                                game.unselect_piece()
                                game.show_pieces(screen)
                                pygame.display.update()

                                move = ai.eval(board)
                                initial = move.initial
                                final = move.final
                                # piece
                                piece = board.squares[initial.row][initial.col].piece
                                # capture
                                captured = board.squares[final.row][final.col].has_piece()
                                # move
                                board.move(piece, move)
                                game.play_sound(captured)
                                # draw
                                game.show_bg(screen)
                                game.show_pieces(screen)
                                # next -> AI
                                game.next_turn()

                    game.unselect_piece()
                    
                    dragger.undrag_piece()

                elif event.type == pygame.KEYDOWN:           # key pressed
                    
                    if event.key == pygame.K_a:             # change gamemode
                        game.change_gamemode()

                    # chnaging themes
                    if event.key == pygame.K_t:
                        game.change_theme()


                    # depth
                    if event.key == pygame.K_3:
                        ai.depth = 3

                    if event.key == pygame.K_4:
                        ai.depth = 4

                    if event.key == pygame.K_r:
                        game.reset()

                        screen = self.screen
                        game = self.game
                        board = self.game.board
                        ai = self.game.ai
                        dragger = self.game.dragger

                    # if event.key == pygame.K_r:
                    #     game.reset()
                    #     # screen = self.screen
                    #     game = self.game
                    #     board = self.game.board
                    #     dragger = self.game.dragger
                elif event.type==pygame.QUIT:                ## quit application
                    pygame.quit()
                    sys.exit()
        
            pygame.display.update()
# pygame.init()
# pygame.mixer.init()
main = Main()
main.mainloop()
