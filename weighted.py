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
        return self.fen+'\n'+self.move.uci()+'\n'+str(self.weight)
        