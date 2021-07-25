import sys
import numpy as np
from instances_meta import AType


class ItemA:
    def __init__(self,
                 att_index,
                 lbl_index,
                 lbl_count: np.array,
                 rank,
                 a_type=AType.nominal,
                 itm_index=-1,
                 lower=-sys.maxsize,
                 upper=sys.maxsize):
        self.att_index = att_index
        self.lbl_index = lbl_index
        self.lbl_count = lbl_count
        self.rank = rank
        self.a_type = a_type
        self.itm_index = itm_index
        self.lower = lower
        self.upper = upper

    def max(self, that):
        if self.rank >= that.rank:
            return self
        else:
            return that

    def __repr__(self):
        if self.a_type == AType.nominal:
            rs = f'itm_index={self.itm_index}'
        else:
            rs = f'lower={self.lower}, upper={self.upper}'
        return f"""Item: type={self.a_type}, 
   att_index={self.att_index}
   lbl_count={self.lbl_count}
   lbl_index={self.lbl_index}
   rank={self.rank}
   {rs}"""

    def sum(self):
        return np.sum(self.lbl_count)

    def correct(self):
        return self.lbl_count[self.lbl_index]

    def errors(self):
        return self.sum() - self.correct()

    def confidence(self):
        return self.correct() / self.sum()

    def match(self, v):
        return self.itm_index == int(v) \
            if self.a_type == AType.nominal \
            else self.lower <= v < self.upper


# TODO make sure it is not changed later, make it immutable
identity_item = ItemA(-1, -1, [], -sys.maxsize, AType.nominal)

