import csv
import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

class Handler(ABC):
    def __init__(self, src):
        self.src = src
        self.data = []

    @abstractmethod
    def load_data(self):
        pass
    
    def get_data(self):
        return self.data

class CSVHandler(Handler):
    def __init__(self, src):
        super(CSVHandler, self).__init__(src)
    
    def load_data(self):
        with open(self.src, 'r') as csvfile:
            csv_src = list(csv.reader(csvfile))
            dict_list = []
            for i in range(len(csv_src) - 1):
                s = {}
                j = 0
                for col in csv_src[0]:
                    s[col] = csv_src[i + 1][j]
                    j += 1
                dict_list.append(s)
            self.data = dict_list
class JSONHandler(Handler):
    def __init__(self, src):
        super(JSONHandler, self).__init__(src)

    def load_data(self):
        with open(self.src, 'r') as jsonfile:
            json_src = json.load(jsonfile)['fields']
            self.data = list(json_src)
class XMLHandler(Handler):
    def __init__(self, src):
        super(XMLHandler, self).__init__(src)

    def load_data(self):
        xml_src = ET.parse(self.src)
        root = xml_src.getroot()
        xml_dict = {}
        for child in root.iter('object'):
            xml_dict[child.attrib['name']] = child.find('value').text
        xml_list = []
        xml_list.append(xml_dict)
        self.data = xml_list

class Table():
    def __init__(self):
        self.src_list = []
        self.data_list = []
        self.min_lenght = 0
        self.d_lenght = 0
        self.ready = 0

    def load(self, src):
        if src[-4:] == '.csv':
            self.src_list.append(CSVHandler(src))
        if src[-4:] == 'json':
            self.src_list.append(JSONHandler(src))
        if src[-4:] == '.xml':
            self.src_list.append(XMLHandler(src))

        self.src_list[-1].load_data()
        data = self.src_list[-1].get_data()
        [self.data_list.append(d) for d in data]

    def cut(self):
        if self.data_list is not None:
            self.min_lenght = min(list(map(len, self.data_list)))

            count = 0
            for key in self.data_list[0].keys():
                if key[0] == 'D':
                    count += 1
            self.d_lenght = count

            for data in self.data_list:
                l = len(data)
                for i in range(l - self.min_lenght):
                    key = 'M' + str(self.min_lenght - self.d_lenght + i + 1)
                    data.pop(key)
            self.ready = 1

    def order(self):
        if self.ready == 1:
            sub_list = []
            row = 0
            for d in self.data_list:
                sub_list.append([d['D1'], row])
                row += 1
            sub_list.sort()

            ord_list = []
            for i in range(len(self.data_list)):
                ord_list.append(self.data_list[sub_list[i][1]])
            self.data_list = ord_list

    def row_sum(self):
        if self.ready == 1:
            sub_list = []
            r = 0

            for d in self.data_list:
                dd = {}
                for i in range(self.d_lenght):
                    colD = 'D' + str(i + 1)
                    dd[colD] = d[colD]
                sub_list.append([dd, r])
                r += 1

            eqs = set()
            for i in range(len(sub_list)):
                splt = [sub_list[i][1]]
                for j in range(len(sub_list)):
                    if sub_list[i][0] == sub_list[j][0] and i != j:
                        splt.append(sub_list[j][1])
                if len(splt) > 1:
                    eqs.add(tuple(sorted(splt)))
            eqs = list(eqs)

            l = len(eqs)
            for i in range(l):
                splt = eqs.pop()
                for j in range(len(splt) - 1):
                    row = self.data_list.pop(splt[j + 1])
                    for k in range(len(self.data_list[0]) - self.d_lenght):
                        colM = 'M' + str(k + 1)
                        self.data_list[splt[0]][colM] = int(self.data_list[splt[0]][colM])
                        self.data_list[splt[0]][colM] += int(row[colM])

            for row in self.data_list:
                for i in range(len(self.data_list[0]) - self.d_lenght):
                    old_col = 'M' + str(i + 1)
                    new_col = 'MS' + str(i + 1)
                    row[new_col] = row.pop(old_col)

            sub_list = []
            row = 0
            for d in self.data_list:
                sub_list.append([d['D1'], row])
                row += 1
            sub_list.sort()

            ord_list = []
            for i in range(len(self.data_list)):
                ord_list.append(self.data_list[sub_list[i][1]])
            self.data_list = ord_list


    def print(self, name):
        with open(name, 'w') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t')
            keys = self.data_list[0].keys()
            writer.writerow(keys)
            for row in self.data_list:
                s = ''
                for key in keys:
                    s += str(row[key])
                writer.writerow(s)


table = Table()
table.load('csv_data_1.csv')
table.load('csv_data_2.csv')
table.load('json_data.json')
table.load('xml_data.xml')
table.cut()
table.order()
table.print('res_basic.tsv')
table.row_sum()
table.print('res_adv.tsv')

