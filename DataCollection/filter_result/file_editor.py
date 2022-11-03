import pandas as pd
import glob
import csv


# file merge function
def merge(outfile):
    csv_list = glob.glob('results/*.csv')
    print(u'found %s files' % len(csv_list))
    print(u'processing............')
    for i in range(len(csv_list)):
        print(csv_list[i])
        fr = open(csv_list[i], 'r')
        data = pd.read_csv(fr)
        data["suburb_id"] = ""
        # data.loc[data['types'] == type_list2[i], 'types'] = type_list[i]
        data.to_csv(outfile, mode='a', index=False)
    print(u'merge complete')


# drop duplicates
def distinct(file):
    df = pd.read_csv(file, header=None)
    datalist = df.drop_duplicates()
    datalist.to_csv(file, index=False, header=False)
    print('distinct complete')


# merge new version counts_merge file
def newmerge(file1, file2, file3):
    type_list = ["bus stop", "coffee shop", "dental", "hair care", "motor repair", "restaurant", "orchard",
                 "clothing store", "train station"]
    header = ["suburb_id",
              "suburb",
              "bus stop",
              "coffee shop",
              "dental",
              "hair care",
              "motor repair",
              "restaurant",
              "orchard",
              "clothing store",
              "train station"]
    s_list = []
    c_list = []
    rows = []
    with open(file1) as f_csv:
        sfr = csv.reader(f_csv)
        for i in sfr:
            s_list.append(i)
    with open(file2) as f2_csv:
        cf = csv.reader(f2_csv)
        for j in cf:
            c_list.append(j)
    for sub in s_list:
        bus_stop = coffee_shop = dentist = hair_care = car_repair = restaurant = orchard = clothing_store = train_station = 0
        for row in c_list:
            if row[0] == sub[0] and row[3] == type_list[0]:
                bus_stop = int(row[4])
            if row[0] == sub[0] and row[3] == type_list[1]:
                coffee_shop = int(row[4])
            if row[0] == sub[0] and row[3] == type_list[2]:
                dentist = int(row[4])
            if row[0] == sub[0] and row[3] == type_list[3]:
                hair_care = int(row[4])
            if row[0] == sub[0] and row[3] == type_list[4]:
                car_repair = int(row[4])
            if row[0] == sub[0] and row[3] == type_list[5]:
                restaurant = int(row[4])
            if row[0] == sub[0] and row[3] == type_list[6]:
                orchard = int(row[4])
            if row[0] == sub[0] and row[3] == type_list[7]:
                clothing_store = int(row[4])
            if row[0] == sub[0] and row[3] == type_list[8]:
                train_station = int(row[4])
        if bus_stop + coffee_shop + dentist + hair_care + car_repair + restaurant + orchard + clothing_store + train_station != 0:
            print(
                bus_stop + coffee_shop + dentist + hair_care + car_repair + restaurant + orchard + clothing_store + train_station)
            rows.append({
                "suburb": sub[1],
                "bus stop": bus_stop,
                "coffee shop": coffee_shop,
                "dental": dentist,
                "hair care": hair_care,
                "motor repair": car_repair,
                "restaurant": restaurant,
                "orchard": orchard,
                "clothing store": clothing_store,
                "train station": train_station
            })
            print(rows[-1])
    with open(file3, 'w', newline='') as m_file:
        m_file_csv = csv.DictWriter(m_file, header)
        m_file_csv.writeheader()
        m_file_csv.writerows(rows)


# edit types column value in result_merge file
def edit_type(file):
    r_list = []
    type_list = ["Bus stop", "Coffee shop", "Dentist", "Hair care", "Motor repair", "Restaurant", "Orchard",
                 "Clothing store", "Train station"]
    type_list2 = ["bus stop", "coffee shop", "dental", "hair care", "motor repair", "restaurant", "orchard",
                  "clothing store", "train_station"]
    rf = pd.read_csv(file)
    # for a in range(len(type_list)):
    #     rf.loc[rf['types'] == type_list2[a], 'types'] = type_list[a]
    rf.loc[rf['types'] == 'cafe', 'types'] = 'Coffee shop'
    rf.to_csv(file, index=False)


# merge train result into result_merge file
def mer_train(file1, file2):
    f1 = pd.read_csv(file1)
    f2 = pd.read_csv(file2)
    f2['train station'] = f1['count']
    f2.to_csv(file2, index=False)


# edit id of suburb list
def edit_id(file1, file2):
    s_list = []
    with open(file1) as subf:
        sf = csv.reader(subf)
        for a in sf:
            s_list.append(a)
    rf = pd.read_csv(file2)
    for i in s_list:
        rf.loc[rf['suburb'] == i[0], 'suburb_id'] = i[1]
    rf.to_csv(file2, index=False)


# find how many suburbs have no coffee results, get the suburb list to request information again
def find_zero(file, file2):
    c_list = []
    s_list = []
    sub_list = []
    header = ["suburb"]
    with open(file) as cfile:
        cf = csv.reader(cfile)
        for a in cf:
            c_list.append(a)
    with open(file2) as sfile:
        sf = csv.reader(sfile)
        for s in sf:
            sub_list.append(s[0])
    for i in c_list:
        if i[4] == "0" and i[1] in sub_list:
            print(i[1])
            s_list.append({"suburb": i[1]})
    with open("0cafe_list.csv", 'w', newline='') as s_file:
        m_file = csv.DictWriter(s_file, header)
        m_file.writeheader()
        m_file.writerows(s_list)


# modify coffee shop count after repair the results
def add_count(count1, count2):
    c_list = []
    with open(count1) as c_file1:
        c1 = csv.reader(c_file1)
        for i in c1:
            c_list.append(i)
    c2 = pd.read_csv(count2)
    for a in c_list:
        c2.loc[c2["suburb"] == a[1], 'Coffee shop'] = a[4]
    c2.to_csv(count2, index=False)

if __name__ == '__main__':
    sub_file = "suburb_list.csv"
    result_file = "results_merge.csv"
    count_file = "counts_merge.csv"
    train = "train station-count.csv"
    mer = "count_merge.csv"
    add_count("coffee shop-count.csv", mer)
    # merge(result_file)
    # distinct(result_file)
    # edit_type(result_file)
    # newmerge(sub_file, count_file, mer)
    # delete_extruct(mer)
    # edit_id(sub_file, result_file)
    # remove_orchard(result_file)
    # find_zero("coffee shop-count.csv", sub_file)
    # fr = open("coffee shop_results.csv", 'r')
    # data = pd.read_csv(fr, header=None)
    # data.to_csv(result_file, mode='a', index=False, header=False)
