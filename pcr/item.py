import sys
import numpy as np
from instances_meta import AType
from constants import missing_nominal, min_float, max_float


class ItemA:
    def __init__(self,
                 att_index,
                 lbl_index,
                 lbl_count: np.array,
                 rank,
                 a_type=AType.nominal,
                 index=missing_nominal,
                 lower=min_float,
                 upper=max_float):
        self.att_index = att_index
        self.lbl_index = lbl_index
        self.lbl_count = lbl_count
        self.rank = rank
        self.a_type = a_type
        self.index = index
        self.lower = lower
        self.upper = upper

    def max(self, that):
        return self if self.rank >= that.rank else that

    def __repr__(self):
        if self.a_type == AType.nominal:
            rs = f'itm_index={self.index}'
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
        return self.index == int(v) \
            if self.a_type == AType.nominal \
            else self.lower <= v < self.upper


# TODO make sure it is not changed later, make it immutable
identity_item = ItemA(-1, -1, [], min_float, AType.nominal)
