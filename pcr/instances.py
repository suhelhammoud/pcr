import os.path
import numpy as np
import csv
from instances_meta import *
from constants import missing_nominal, missing_numeric


def _get_all_columns(data, num_columns):
    result = [[] for i in range(num_columns)]
    for line in data:
        for idx, val in enumerate(line):
            result[idx].append(val)
    return result


def _get_column(data, col_index):
    return [data[i][col_index] for i in range(len(data))]


def _map_nominal_att(attribute, items_names):
    return np.array([items_names.index(i)
                     if i != '?' else missing_nominal
                     for i in attribute],
                    dtype=np.uint16)


def _map_numeric_att(attribute):
    return np.array([float(i)
                     if i != '?' else missing_numeric
                     for i in attribute],
                    dtype=np.float32)


def _map_att(attribute, att_meta: AttributeMeta):
    """

    :param attribute:
    :param att_meta:
    :return: np.array represents and attribute with mapped values as numbers and with missing data replaced
    """
    if att_meta.a_type == AType.nominal:
        return _map_nominal_att(attribute, att_meta.items)
    if att_meta.a_type == AType.numeric:
        return _map_numeric_att(attribute)


def _load_csv(file_name):
    if not os.path.isfile(file_name):
        raise Exception(f"csv data file ${file_name} does not exist")

    data_reader = csv.reader(open(file_name, 'r'),
                             skipinitialspace=True,
                             delimiter=',',
                             quoting=csv.QUOTE_NONE)
    return [row for row in data_reader]


class Instances:
    def __init__(self, meta: AttributeMeta,
                 data_file=None):
        self.meta = meta
        if data_file is not None:
            _load_csv(data_file)

    def load(self, data_file):
        """
        TODO if not with cross-validation then try to initialize in constructor,
        :param data_file: "data.csv"
        :return: list(list([str]))
        """
        if not os.path.isfile(data_file):
            raise Exception(f"Data file ${data_file} does not exist")

        csv_data = _load_csv(data_file)
        columns = _get_all_columns(csv_data, len(self.meta.attributes))
        self.data = [_map_att(column, self.meta.attributes[idx])
                     for idx, column in enumerate(columns)]
        self.labels = self.data[-1]  #
        self.data = self.data[:-1]  # keep only attributes

    def num_instances(self):
        return self.labels.size


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


if __name__ == '__main__':
    instances = get_instances()
    print(instances.data[0])
