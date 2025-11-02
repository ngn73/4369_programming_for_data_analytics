'''
Assignment_5.py
Author  Niall Naughton
Date    27/10/2025
----------------------------------------------------------------------------------
Description:     
Testing code for notebook called assignment05_population.ipynb
----------------------------------------------------------------------------------
'''


import pandas as pd
import csv as csv

url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/FY006A/CSV/1.0/en"
df = pd.read_csv(url)
df.tail(3)

# Review Columns
headers = df.columns.tolist()
headers

# Remove unwanted columns
drop_col_list = ['STATISTIC', 'Statistic Label','TLIST(A1)','CensusYear','C02199V02655','C02076V03371','C03789V04537','UNIT']
df.drop(columns=drop_col_list, inplace=True)


# Filter "Administrative Counties" for Ireland only
#df = df[df["Administrative Counties"] == "Ireland"]
#Filter "Single Year of Age" by removing "all Ages
df = df[df["Single Year of Age"] != "All ages"]
#Filter "Sex" by removing "Both Sexes"
#df = df[df["Sex"] != "Both sexes"]

#Tidy up Column Names
df.rename(columns={'Administrative Counties': 'Region', 'Single Year of Age': 'Age'}, inplace=True)


#Format Age Column (replace 'Under 1 year' with 0, and convert to int)
df['Age'] = df['Age'].str.replace('Under 1 year', '0')
df['Age'] = df['Age'].str.replace(r'\D', '', regex=True)

# Convert columns to int64
df['Age']=df['Age'].astype('int64')
df['VALUE']=df['VALUE'].astype('int64')

pivot_df = df.pivot(index=['Age', 'Region'], columns='Sex', values='VALUE')
#With the Pivot, Age and Region are not regular columns anymore — they have been moved into the index (row labels)
#We need Age and Region back as normal columns
pivot_df = pivot_df.reset_index()

#Output to CSV for testing
pivot_df.to_csv('testdata.csv', index=True)

'''
#Weighted mean is sum(age*population at age) / sum (populations at age)
weighted_mean_male = (pivot_df['Age'] * pivot_df['Male']).sum() / pivot_df['Male'].sum()
weighted_mean_female = (pivot_df['Age'] * pivot_df['Female']).sum() / pivot_df['Female'].sum()

print(weighted_mean_male)
print(weighted_mean_female)

age_group = 35
age_group_limit1 = age_group - 5;
age_group_limit2 = age_group + 5;

df_grouped = pivot_df[(pivot_df['Age'] >= age_group_limit1) & (pivot_df['Age'] <= age_group_limit2)]

print(df_grouped)

print(df_grouped['Male'].sum())
print(df_grouped['Female'].sum())

'''
