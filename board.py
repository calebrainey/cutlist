AVAILABLE_BOARD_LENGTHS = [72.0, 96.0, 120.0, 144.0]

class Board:
    def __init__(self, length: float):
        self.length = length
        self.cuts = []
        self.remaining = length
        self.kerf = 0.125

    def can_fit(self, cut: float):
        return self.remaining >= cut

    def add_cut(self, cut: float):
        if self.can_fit(cut):
            self.cuts.append(cut)
            self.remaining -= cut
            if len(self.cuts) > 1:
                self.remaining -= self.kerf
            return True
        return False
    
    def get_cutlist(self, cuts):
        pass
    
    @property
    def waste(self):
        return self.remaining