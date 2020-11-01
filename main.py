# -*- coding: utf-8 -*-
import sys
import csv

def loadData(fnameDB, deLimiter, quotechar, encoding):
    head = None
    data = []
    with open(fnameDB, newline="", encoding=encoding) as csvfile:
        reader = csv.reader(csvfile, delimiter=deLimiter, quotechar=quotechar)
        for row in reader:
            if head is None:
                if len(row[0]) == 0:
                    continue
                head = row
            else:
                data.append(row)
    return head, data


def joinHead(head, data):
    data2 = []
    for rec in data:
        rec2 = {}
        for i in range(len(rec)):
            rec2[head[i]] = rec[i]
        data2.append(rec2)
    return data2


if __name__ == "__main__":

    fnameDB = "data/Book1.csv"
    deLimiter = ","
    quotechar = '"'
    encoding = "cp1250"

    head, data = loadData(fnameDB, deLimiter, quotechar, encoding)
    data = joinHead(head, data)

    for rec in data:
        print(data)

    vs = {}
    for rec in data:
        for key in rec:
            if not key in vs:
                vs[key] = []
            v = rec[key]
            if not v in vs[key]:
                vs[key].append(v)
    print(vs)