# -*- coding: utf-8 -*-

import os
import sys
import csv
from datetime import date

if sys.version_info[0] == 3:
    # for Python3
    import tkinter as tk
    import tkinter.filedialog
else:
    # for Python2
    import Tkinter as tk
    import Tkinter.filedialog

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


def stat(rec, thisYear):
    for i in range(100):
        year = "%d" % (thisYear - i)
        if year in rec:
            val = int(rec[year])
            return year, val
    return None, None


def computeStats(fnameDB, deLimiter=",", quotechar='"', encoding="cp1250"):

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
        year, s = stat(rec, thisYear)
        s_tab = str2int(rec["pocet kanbanu"]) * str2int(rec["kanban mnozstvi"])
        loss = s_tab - s
        results[shop].append((loss, key, s_tab, s, year))

    for shop in results:
        results[shop].sort()
        results[shop].reverse()

    return results

def data2text(results):
    text = []
    for shop in results:
        text.append(shop)
        for item in results[shop]:
            loss, key, s_tab, s, year = item
            text.append("%s: year = %s, stat = %f, tab = %f, loss = %f" % (key, year, s, s_tab, loss))
        text.append("")
    text = "\n".join(text)
    return text

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.data = None
        self.monitor = None
        self.create_widgets()

    def newMonitor(self):
        if not self.monitor is None:
            self.xscrollbar.destroy()
            self.yscrollbar.destroy()
            self.monitor.destroy()
        xscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        yscrollbar = tk.Scrollbar(self)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.xscrollbar = xscrollbar
        self.yscrollbar = yscrollbar
        self.monitor = tk.Text(self, wrap="none", xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set, height = 200, width = 400)
        xscrollbar.config(command=self.monitor.xview)
        yscrollbar.config(command=self.monitor.yview)
        #self.monitor.pack(side="bottom")
        self.monitor.pack(expand=tk.YES, fill=tk.BOTH)

    def create_widgets(self):
        menubar = tk.Menu(self)
        self.menu = menubar
        menubar.add_command(label="Load dataset", command=self.load)
        menubar.add_command(label="Save results", command=self.save)
        menubar.add_command(label="Quit", command=self.master.destroy)
        self.master.config(menu=menubar)
        self.newMonitor()


    def load(self):
        initialdir = (os.path.dirname(os.path.abspath(__file__)))
        filename = tk.filedialog.askopenfilename(initialdir=initialdir, title="Select a File", filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
        if len(filename) == 0:
            return
        self.data = computeStats(filename)
        self.newMonitor()
        text = data2text(self.data)
        self.monitor.insert(tk.INSERT, text)
        #print(self.data)

    def save(self):
        print("saving")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("ToyStats")
    app = App(master=root)
    app.mainloop()
