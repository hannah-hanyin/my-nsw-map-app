# education - exclude year 2016
# income - exclude year 2016
# population - Percentage of males (%), Percentage of females (%), Persons - Total (no.) (exclude year 2018)
# rental cost - Weekly median advertised rent (updated August 2020)
from itertools import chain

import pandas as pd

from pandas import read_csv, Series, DataFrame
import numpy as np

income = read_csv('income.csv')
education = read_csv('education.csv')
population = read_csv('population.csv')
rental_cost = read_csv('rental_cost.csv')
# print(rental_cost.info)
rental_cost['Weekly median advertised rent'] = rental_cost['Weekly median advertised rent'].str.replace('$','').fillna(0)
rental_cost['Label'] = rental_cost['Label'].str.title()
rental_cost.drop_duplicates('Label',keep='last',inplace=True)

def chainer(s):
    return list(chain.from_iterable(s.str.split('-')))


def split_rows(df: DataFrame):
    lens = df['Label'].str.split('-').map(len)
    shape = {}
    for column in df.columns:
        if column == "Label":
            shape['Label'] = chainer(df[column])
            continue
        shape[column] = np.repeat(df[column], lens)

    new_df = pd.DataFrame(shape)
    new_df['Label'] = new_df['Label'].str.strip()
    new_df = new_df[~new_df['Label'].isin(['East', 'South', 'West', 'North'])]
    new_df['Label'] = new_df['Label'].apply(lambda x: x.replace('(East)', ''))
    new_df['Label'] = new_df['Label'].apply(lambda x: x.replace('(West)', ''))
    new_df['Label'] = new_df['Label'].apply(lambda x: x.replace('(South)', ''))
    new_df['Label'] = new_df['Label'].apply(lambda x: x.replace('(North)', ''))
    new_df['Label'] = new_df['Label'].apply(lambda x: x.replace('(NSW)', ''))
    new_df['Label'] = new_df['Label'].str.strip()
    #new_df.drop_duplicates('Label')
    return new_df

# pd.set_option("max_columns",5)

population = split_rows(population)
income = split_rows(income)
education = split_rows(education)


final = pd.merge(population.set_index("Label"), income.set_index("Label"), left_on="Label", right_on="Label", right_index=True, left_index=True).reset_index()
final = pd.merge(final.set_index("Label"), education.set_index("Label"), left_on="Label", right_on="Label", right_index=True, left_index=True).reset_index()
final = pd.merge(final.set_index("Label"), rental_cost.set_index("Label"), left_on="Label", right_on="Label", right_index=True, left_index=True).reset_index()


final = final.set_index('Label')
int_column = {'Persons - Total (no.)','Median Household Weekly Income','Employed (no.)','Unemployed (no.)','Labour Force (no.)','Total population aged 15 years and over (no.)','Weekly median advertised rent'}
# remove double quotation for merging
for i, col in enumerate(final.columns):
    final.iloc[:, i] =final.iloc[:, i].str.replace(',','').replace(' ','').replace('-','0').fillna(0).astype(float)


final = final.groupby('Label').mean()
final['Percentage of males (%)']=final['Percentage of males (%)']*100
final['Percentage of females (%)']=final['Percentage of females (%)']*100
for i in final.columns:
    if i in int_column:
        final[i]=final[i].astype(int)
    else:
        final[i]=final[i].round(decimals=1)

# print(final)


final.to_csv("aggregated_data_census_rental.csv",index=True)