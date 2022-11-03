import pandas as pd
import glob
import csv
filename = "tap_on_off_data.csv"
header = ["type", "station name", "date", "tap on", "tap off"]


t_list = []
outrow = []
with open(filename) as tf:
    tr = csv.reader(tf)
    for i in tr:
        t_list.append(i)
for row in t_list:
    t_on = 0
    if row[2] == "off":
        for a in range(251, 492):
            if t_list[a][3] == row[3]:
                t_on = t_list[a][4]
        outrow.append({"type": "Train station",
                       "station name": row[3],
                       "date": row[1],
                       "tap on": t_on,
                       "tap off": row[4]})

with open("filter.csv", 'w', newline='') as wf:
    f_csv = csv.DictWriter(wf, header)
    f_csv.writeheader()
    f_csv.writerows(outrow)
