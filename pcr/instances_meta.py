import json
import os.path


class AType:
    """
    #TODO use Enum names
    """
    nominal = 0
    numeric = 1
    o_nominal = 2

    def name(i:int):
        return ['nominal', 'numeric'][i]

    def get_type(v:str):
        v = v.lower()
        return AType.nominal \
            if v == 'nominal' \
            else AType.numeric


class AttributeMeta:

    def __init__(self, d):
        self.name = d['name']
        self.a_type = AType.get_type(d['type'])
        if 'items' in d:
            self.items = d['items']

    def num_items(self):
        return len(self.items) \
            if self.a_type == AType.nominal \
            else 0

    def to_dict(self):
        d = {'name': self.name}
        if hasattr(self, 'a_type'):
            d['a_type'] = self.a_type.__repr__()
        if hasattr(self, 'items'):
            d['items'] = self.items
        return d

    def to_json(self):
        out = {'name': self.name}
        if hasattr(self, 'a_type'):
            out['a_type'] = self.a_type
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

    def num_lbl(self):
        return self.attributes[-1].num_items()

    def lbl(self):
        return self.attributes[-1]

    def num_items(self, idx=None):
        if idx is None:
            return [att.num_items() for att in self.attributes]
        else:
            return self.attributes[idx].num_items()

    def a_type(self, att_index=None):
        if att_index is None:
            return [a.a_type for a in self.attributes]
        else:
            return self.attributes[att_index].a_type

    def num_attributes(self):
        return len(self.attributes) - 1

    def headers(self, a_type=None):
        if a_type is None:
            return [i.name for i in self.attributes]
        else:
            return [i.name for i in self.attributes
                    if i.a_type == a_type]

    def indexes_of_type(self, a_type):
        return [i for i, att in enumerate(self.attributes)
                if att.a_type == a_type]
