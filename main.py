import csv
import json
import xml.etree.ElementTree as ET

def data_from_csv(name):
    with open (name, 'r') as csvfile:
        csv_src = list(csv.reader(csvfile))
        dict_list = []
        for i in range(len(csv_src) - 1):
            s = {}
            j = 0
            for col in csv_src[0]:
                s[col] = csv_src[i + 1][j]
                j += 1
            dict_list.append(s)
        return dict_list

def data_from_json(name):
    with open (name, 'r') as jsonfile:
        json_src = json.load(jsonfile)['fields']
        return list(json_src)

def data_from_xml(name):
    xml_src = ET.parse(name)
    root = xml_src.getroot()
    xml_dict = {}
    for child in root.iter('object'):
        xml_dict[child.attrib['name']] = child.find('value').text
    xml_list = []
    xml_list.append(xml_dict)
    return xml_list

def find_least(inp_list):
    min_val = min(list(map(len, inp_list)))
    return min_val

def count_first_class(inp_dict):
    count = 0
    for key in inp_dict.keys():
        if key[0] == 'D':
            count += 1
    return count

def cut(inp_dict, n):
    l = len(inp_dict)
    d = count_first_class(inp_dict)
    for i in range(l - n):
        key = 'M' + str(n - d + i + 1)
        inp_dict.pop(key)

def order(inp_list):
    sub_list = []
    row = 0
    for d in inp_list:
        sub_list.append([d['D1'], row])
        row += 1
    sub_list.sort()

    ord_inp_list = []
    for i in range(len(inp_list)):
        ord_inp_list.append(inp_list[sub_list[i][1]])
    return ord_inp_list

def row_sum(inp_list):
    sub_list = []
    r = 0
    n = count_first_class(inp_list[0])

    for d in inp_list:
        dd = {}
        for i in range(n):
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

    l = len(eqs)
    for i in range(l):
        splt = eqs.pop()
        for j in range(len(splt) - 1):
            row = inp_list.pop(splt[j + 1])
            for k in range(len(inp_list[0]) - n):
                colM = 'M' + str(k + 1)
                inp_list[splt[0]][colM] = int(inp_list[splt[0]][colM])
                inp_list[splt[0]][colM] += int(row[colM])

    for row in inp_list:
        for i in range(len(inp_list[0]) - n):
            old_col = 'M' + str(i + 1)
            new_col = 'MS' + str(i + 1)
            row[new_col] = row.pop(old_col)

    return order(inp_list)

def to_tsv(name, inp_list):
    with open(name, 'w') as tsvfile:
        writer = csv.writer(tsvfile, delimiter = '\t')
        keys = inp_list[0].keys()
        writer.writerow(keys)
        for row in inp_list:
            s = ''
            for key in keys:
                s += str(row[key])
            writer.writerow(s)



csv_src_1 = data_from_csv('csv_data_1.csv')
csv_src_2 = data_from_csv('csv_data_2.csv')
json_src = data_from_json('json_data.json')
xml_src = data_from_xml('xml_data.xml')

n = find_least([csv_src_1[0], csv_src_2[0], json_src[0], xml_src[0]])


[cut(d,n) for d in csv_src_1]
[cut(d,n) for d in csv_src_2]
[cut(d,n) for d in json_src]
[cut(d,n) for d in xml_src]

total = []
[total.append(d) for d in csv_src_1]
[total.append(d) for d in csv_src_2]
[total.append(d) for d in json_src]
[total.append(d) for d in xml_src]

ord_total = order(total)
to_tsv('res1.tsv', ord_total)
summed_total = row_sum(total)
to_tsv('res2.tsv', summed_total)
