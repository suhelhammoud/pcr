import json
import os.path


class AType:
    """
    #TODO use Enum names
    """
    nominal = 0
    numeric = 1
    o_nominal = 2

    def name(i):
        return ['nominal', 'numeric'][i]


def get_type(v):
    v = v.lower()
    if v == 'nominal':
        return AType.nominal
    return AType.numeric


class AttributeMeta:
    def __init__(self, d):
        self.name = d['name']
        self.a_type = get_type(d['type'])
        if 'items' in d:
            self.items = d['items']

    def num_items(self):
        return len(self.items) if self.a_type == AType.nominal else -1

    def to_dict(self):
        d = {'name': self.name}
        if hasattr(self, 'att_type'):
            d['att_type'] = self.a_type.__repr__()
        if hasattr(self, 'items'):
            d['items'] = self.items
        return d

    def to_json(self):
        out = {'name': self.name}
        if hasattr(self, 'att_type'):
            out['att_type'] = self.a_type
        if hasattr(self, 'items'):
            out['items'] = self.items
        return json.dumps(out)


class InstancesMeta:
    def __init__(self, file_name):
        if not os.path.isfile(file_name):
            raise Exception(f"Meta file ${file_name} does not exist")

        d = json.load(open(file_name, 'r'))
        if 'relation' in d:
            self.relation = d['relation']

        if 'size' in d:
            self.size = int(d['size'])

        if 'attributes' not in d:
            raise Exception(f"No attributes found in meta file")

        self.attributes = [AttributeMeta(i) for i in d['attributes']]
        self.relation = d['relation'] if 'relation' in d else 'na'

    def to_json(self):
        out = {'relation': self.relation}
        if hasattr(self, 'size'):
            out['size'] = self.size

        out['attributes'] = [i.to_dict() for i in self.attributes]
        return json.dumps(out, indent=2, )

    def label_index(self):
        return len(self.attributes) - 1

    def num_labels(self):
        return len(self.attributes[-1].items)

    def label(self):
        return self.attributes[-1]

    def num_items(self, idx=None):
        if idx is not None:
            return len(self.attributes[idx].num_items())
        else:
            return [att.num_items() for att in self.attributes]

    def a_type(self, att_index=None):
        if att_index is None:
            return [a.a_type for a in self.attributes]
        else:
            return self.attributes[att_index].a_type

    def num_attributes(self):
        return len(self.attributes) - 1

    def num_items(self, att_index=None):
        if att_index is None:
            return [att.num_items() for att in self.attributes]
        else:
            return self.att(att_index).num_items()

    def att_indexes(self):
        return list(range(len(self.attributes) - 1))

    def att(self, att_index):
        return self.attributes[att_index]

    def headers(self, htype):
        return [i.name for i in self.attributes if i.a_type == htype]

    def nominal_indexes(self):
        return self.indexes_with_type(AType.nominal)

    def indexes_with_type(self, tp):
        return [i for i, att in enumerate(self.attributes)
                if att.a_type == tp]

