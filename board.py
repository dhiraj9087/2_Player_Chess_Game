from const import *
from square import Square


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
        pass

b=Board()
b._create()