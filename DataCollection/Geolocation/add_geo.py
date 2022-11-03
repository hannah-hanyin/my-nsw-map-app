import pandas as pd
import csv


def geo_add(result_f, suburb_f):
    rl = []
    sl = []
    with open(result_f) as rf:
        r_data = csv.reader(rf)
        for i in r_data:
            rl.append(i)
    with open(suburb_f) as sf:
        s_data = csv.reader(sf)
        for j in s_data:
            sl.append(j)
    sub_f = pd.read_csv(suburb_f)
    res_f = pd.read_csv(result_f)
    for s in sl:
        for r in rl:
            print(r[1])
            if s[0] == r[1]:
                sub_f.loc[sub_f['suburb'] == s[0], 'lng'] = r[7]
                sub_f.loc[sub_f['suburb'] == s[0], 'lat'] = r[8]
                break
    sub_f.to_csv("suburb_list2.csv", index=False)

if __name__ == '__main__':
    file1 = "suburb_list.csv"
    file2 = "results_merge.csv"
    geo_add(file2, file1)