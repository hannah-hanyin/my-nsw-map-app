import json
import os
import csv

# suburb file and search result folder path
suburb_file_dir = "suburb_list.csv"
search_results_path = "search results"


# query industry
industry_list = ["bus stop", "coffee shop", "dental", "hair care", "motor repair", "restaurant"]
k_industry = industry_list[5]
type_list = ["transit_station", "cafe", "dentist", "hair_care", "car_repair", "restaurant"]
k_type_name = type_list[5]
res = {}

k1 = "results"
k2 = "plus_code"
k3 = "compound_code"
k_type = "types"
k_name = "name"
k_rating = "rating"
k_ratingNum = "user_ratings_total"
k_location = "location"
k_lng, k_lat = "lng", "lat"
k_address = "formatted_address"
count = 0

# csv writing
headers = ["suburb", "postcode", "name", "types", "rating", "user_ratings_total", "lng", "lat", "formatted_address"]
header_count = ["suburb", "post", "industry", "count"]
rows = []
count_rows = []
locations = []
with open(suburb_file_dir) as suburb_list_file:
    csv_reader = csv.reader(suburb_list_file)
    for i in csv_reader:
        locations.append(i[1])

for sub in locations:
    count = 0
    k_suburb = sub
    k_post = 0
    # read postcode file
    with open("NSW suburb postcodes.csv") as post_f:
        csv_reader1 = csv.reader(post_f)
        for a in csv_reader1:
            if a[4] == k_suburb.upper():
                k_post = a[3]
    filedir = search_results_path + '/' + k_industry + '/' + k_industry + ' in ' + k_suburb
    filenames = os.listdir(filedir)
    for filename in filenames:
        output_dic = {}
        filepath = filedir + '/' + filename
        with open(filepath, 'r') as load_f:
            load_dict = json.load(load_f)
        if k1 in load_dict:
            for item in load_dict[k1]:
                if k2 in item:
                    if k3 in item[k2]:
                        compound_code = item[k2][k3]
                        suburb_str = compound_code[8:].split(", ")
                        if suburb_str[0] == k_suburb and suburb_str[1] == "New South Wales":

                            # data_num = k_suburb + str(count)
                            if k_type_name in item[k_type]:
                                count += 1
                                rows.append({"suburb": suburb_str[0],
                                             "postcode": k_post,
                                             k_name: item[k_name],
                                             k_type: k_type_name,
                                             k_rating: item[k_rating],
                                             k_ratingNum: item[k_ratingNum],
                                             k_lng: item["geometry"][k_location][k_lng],
                                             k_lat: item["geometry"][k_location][k_lat],
                                             k_address: item[k_address]})

    print(k_suburb, k_post, count)
    count_rows.append({"suburb": k_suburb,
                       "post": k_post,
                       "industry": k_industry,
                       "count": count})
    # create store count file

with open('filter_result/' + k_industry + '-count.csv', 'w', newline='') as f_count:
    f_count_csv = csv.DictWriter(f_count, header_count)
    f_count_csv.writeheader()
    f_count_csv.writerows(count_rows)


# write csv file
with open('filter_result/' + k_industry + '_results.csv', 'w', newline='') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)
