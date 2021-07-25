import numpy as np

from pcr import item


class Rule:
    def __init__(self, lbl_index):
        self.lbl_index = lbl_index
        self.items = []

    def size(self):
        return len(self.items)

    def last(self):
        assert len(self.items) > 0
        self.items[-1]

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

    def add_test(self, item: item):
        assert not self.contains_att(item.att_index)
        self.items.append(item)

    def can_enhance_rule(self, item: item):
        return item.lbl_index == self.lbl_index and \
               item.confidence() >= self.confidence()

    def __repr__(self):
        pass  # TODO
