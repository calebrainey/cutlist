class Board:
    def __init__(self, length: float):
        self.length = length
        self.cuts = []
        self.remaining = length

    def can_fit(self, cut: float):
        return self.remaining >= cut

    def add_cut(self, cut: float):
        if self.can_fit(cut):
            self.cuts.append(cut)
            self.remaining -= cut
            return True
        return False
    
    @property
    def waste(self):
        return self.remaining