from item import ItemA


class Rule:
    def __init__(self, lbl_index):
        self.lbl_index = lbl_index
        self.items = []

    def size(self):
        return len(self.items)

    def last(self):
        assert len(self.items) > 0
        return self.items[-1]

    def errors(self):
        return self.last().errors()

    def correct(self):
        return self.last().correct()

    def cover(self):
        return self.last().cover()

    def confidence(self):
        return self.correct() / self.cover()

    def contains_att(self, att_index):
        return any(a.att_index == att_index for a in self.items)

    def add_test(self, itm: ItemA):
        assert not self.contains_att(itm.att_index)
        self.items.append(itm)

    def can_enhance_rule(self, itm: ItemA):
        return itm.lbl_index == self.lbl_index and \
               itm.confidence() >= self.confidence()

    def __repr__(self):
        pass  # TODO
