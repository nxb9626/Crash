class WeightedMove( object ):
    """
    class representing a board and move so that it can be sorted
    """
    def __init__(self,fen,move,parent=None,weight=0):
        self.fen = fen
        self.move = move
        self.weight = weight
        self.parent=parent

    def __repr__(self) -> str:
        if self.move != None:
            return self.fen+' '+self.move.uci()+' '+str(self.weight)
        else:
            return str(self.weight)
        