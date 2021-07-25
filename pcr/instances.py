import os.path
import numpy as np
import csv

from instances_meta import AttributeMeta, AType, InstancesMeta


def get_column(data, col_index):
    return [data[i][col_index] for i in range(len(data))]


def get_all_columns(data, num_columns):
    result = [[] for i in range(num_columns)]
    for line in data:
        for idx, val in enumerate(line):
            result[idx].append(val)
    return result


def map_nominal_att(attribute, items_names):
    return np.array([items_names.index(i) if i != '?' else -1 for i in attribute],
                    dtype=np.int16)  # TODO check to use np.int rather than short numbers


def map_att(attribute, att_meta: AttributeMeta):
    """

    :param attribute:
    :param att_meta:
    :return: np.array represents and attribute with mapped values as numbers and with missing data replaced
    """
    if att_meta.a_type == AType.nominal:
        return map_nominal_att(attribute, att_meta.items)
    if att_meta.a_type == AType.numeric:
        return map_numeric_att(attribute)


def map_numeric_att(attribute):
    return np.array([float(i) if i != '?' else np.nan for i in attribute], dtype=float)


def load_csv(file_name):
    result = []
    if not os.path.isfile(file_name):
        raise Exception(f"csv data file ${file_name} does not exist")

    with open(file_name) as csvfile:
        data_reader = csv.reader(csvfile,
                                 skipinitialspace=True,
                                 delimiter=',',
                                 quoting=csv.QUOTE_NONE)
        for row in data_reader:
            result.append(row)
    return result


class Instances:
    def __init__(self, meta: AttributeMeta):
        self.meta = meta

    def labels(self):
        return self.atts[-1]

    def num_instances(self):
        return self.labels.size

    def load(self, data_file):
        if not os.path.isfile(data_file):
            raise Exception(f"data file ${data_file} does not exist")

        csv_data = load_csv(data_file)
        columns = get_all_columns(csv_data, len(self.meta.attributes))
        self.data = [map_att(column, self.meta.attributes[idx])
                     for idx, column in enumerate(columns)]
        self.labels = self.data[-1]  # TODO if not with cross-validation then try to initialize in constructor,

    def a_type(self, att_index=None):
        """
        type of attribute
        :param att_index:
        :return: nominal, numeric
        """
        if att_index is None:
            return [a.a_type for a in self.meta.attributes]
        else:
            return self.meta.att(att_index).a_type


def get_instances():
    """
    Used only for testing
    :return:
    """
    base = '/home/suhel/PycharmProjects/pcr_py/data/uci/'
    meta_file = base + 'iris.json'
    data_file = base + 'iris/iris.data'

    meta = InstancesMeta(meta_file)
    instances = Instances(meta)

    instances.load(data_file)
    return instances
