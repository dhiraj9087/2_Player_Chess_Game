class Square:

    def __init__(self,row,col,piece=None):      # piece is set ot bydefault none as not all square will have peices
        self.row = row
        self.col = col
        self.piece = piece
        

    def has_piece(self):
        return self.piece != None
