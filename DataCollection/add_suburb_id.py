import pandas as pd
import numpy as np

# Read csv file and convert to DataFrame format
api_file = "Database/results_merge.csv"
api_data = pd.read_csv(api_file, low_memory = False) # Prevent pop-up warnings
api_df = pd.DataFrame(api_data)

count_file = "Database/counts_merge2.csv"
count_data = pd.read_csv(count_file, low_memory = False)
count_df = pd.DataFrame(count_data)

abs_file = "Database/aggregated_data_census_rental.csv"
abs_data = pd.read_csv(abs_file, low_memory = False)
abs_df = pd.DataFrame(abs_data)

api_suburb_list = api_df['suburb'].values.tolist()
count_suburb_list = count_df['suburb'].values.tolist()
abs_suburb_list = abs_df['Label'].values.tolist()

# Merge two lists
suburb_list = api_suburb_list + abs_suburb_list

# De-duplicate the elements of the new list
suburb_list = list(set(suburb_list))

# Sort the elements of the new list
suburb_list.sort()

# Add an index list
suburb_id = list(range(1,len(suburb_list)+1))
print(len(suburb_list))
print(len(suburb_id))

# Convert suburb_list and suburb_id into DataFrame
suburb_df = pd.DataFrame(suburb_list, columns=['suburb'])
suburb_df = pd.concat([suburb_df, pd.DataFrame(suburb_id,columns=['id'])],axis=1)
print(suburb_df.head())

# Save DataFrame into a new csv file
suburb_df.to_csv('Database/suburb_list.csv',index=False,header="suburb_list")

# Use the zip function to convert the two lists into a dictionary
suburb_dict = dict(zip(suburb_list,suburb_id))

api_suburb_id = []
count_suburb_id = []
abs_suburb_id = []

# Traverse the dictionary, find the id corresponding to the suburb, and add it to a new list
for s in api_suburb_list:
    api_suburb_id.append(int(suburb_dict[s]))
print(api_suburb_id)

for s in abs_suburb_list:
    abs_suburb_id.append(int(suburb_dict[s]))
print(abs_suburb_id)

for s in count_suburb_list:
    count_suburb_id.append(int(suburb_dict[s]))
print(count_suburb_id)

# Add suburb_id list into DataFrame
api_df.loc[:, 'suburb_id'] = api_suburb_id
count_df.loc[:, 'suburb_id'] = count_suburb_id
abs_df.loc[:, 'suburb_id'] = abs_suburb_id

# Save DataFrame into csv file

api_df.to_csv('Database/results_merge.csv',index=False,header="results_merge")
count_df.to_csv('Database/count_merge.csv',index=False,header="count_merge")
abs_df.to_csv('Database/aggregated_data_census.csv',index=False,header="aggregated_data_census")
