import pandas as pd
from sqlalchemy import create_engine
import os

# Establish a connection with mysql
engine = create_engine('mysql+pymysql://root:57035703@localhost:3306/capstone5703')

# Save csv file into sql
def save_csv(path,tablename):
    # Read csv file and save as dataframe
    df = pd.read_csv(path, sep=',')
    # Save dataframe to sql
    df.to_sql(tablename, engine, index= False)
    print("Write to MySQL successfully!")

# Read file name in a specific folder and save it
file_path = '/Users/hanyin/Downloads/CS-39-3-master/DataCollection/filter_result'
files = os.listdir(file_path)
for file in files:
    print(file)
    save_csv(file_path+'/'+file,file)

save_csv('/Users/hanyin/Downloads/CS-39-3-master/DataCollection/data-2020-09-12T20_02_28_553124.csv','census_data')
save_csv('/Users/hanyin/Downloads/CS-39-3-master/DataCollection/suburb_list.csv','suburb_list')
    
