# -*- coding: utf-8 -*-
import sys
import csv
from datetime import date

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


def stat(rec, thisYear, q=0.01):
    years = {}
    weight = 1.0
    sum0 = 1e-30
    sum1 = 0.0
    for i in range(10):
        year = "%d" % (thisYear - i)
        if year in rec:
            val = int(rec[year])
            years[int(year)] = val
            sum0 = sum0 + weight
            sum1 = sum1 + weight * val
        weight = q * weight
    s = sum1 / sum0
    return years, s



if __name__ == "__main__":

    fnameDB = "data/Book1.csv"
    deLimiter = ","
    quotechar = '"'
    encoding = "cp1250"

    thisYear = int(date.today().year)

    head, data = loadData(fnameDB, deLimiter, quotechar, encoding)
    data = joinHead(head, data)

    str2int = lambda x: int(x.replace(",", ""))

    shopLabel = "SHOP RESPONSIBLE FOR STOCK"

    results = {}
    for rec in data:
        shop = "%s = %s" % (shopLabel, rec[shopLabel])
        if not shop in results:
            results[shop] = []
        key = ["%s = %s" % (label, rec[label]) for label in ["YK10", "DOCK", "SATELLITE CODE"]]
        key = ", ".join(key)
        years, s = stat(rec, thisYear)
        s_tab = str2int(rec["pocet kanbanu"]) * str2int(rec["kanban mnozstvi"])
        loss = s_tab - s
        results[shop].append((loss, key, s_tab, s, years))

    for shop in results:
        results[shop].sort()
        results[shop].reverse()
        print("")
        print(shop)
        for item in results[shop]:
            print("")
            loss, key, s_tab, s, years = item
            print("\t%s" % key)
            print("\tyears = " + str(years))
            print("\tstat = %f" % s)
            print("\ttab  = %f" % s_tab)
            print("\tloss  = %f" % loss)

