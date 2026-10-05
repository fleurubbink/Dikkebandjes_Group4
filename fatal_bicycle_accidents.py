"""
Write something here about what the code does and stuff
"""

# importing libraries
import pandas as pd 

# importing csv and converting to a dataframe
df_fatal_accidents = pd.read_csv('Verkeersdoden_vanaf_1950.csv')

## cleaning up csv file
# removing Vervoerswijze and keeping transportmode
df_fatal_accidents.drop('Vervoerswijze',inplace = True, axis = 1)

# keeping the time period from 2013-2025
time_period_mask = df_fatal_accidents['Year'] >= 2013 
df_time_period = df_fatal_accidents[(time_period_mask)]

# removing all transport modes except Bicycle and Moped 
bicycle_mask = df_time_period['TransportMode'] == 'Bicycle'
moped_mask = df_time_period['TransportMode'] == 'Moped'

df_moped_bicycle = df_time_period[(bicycle_mask | moped_mask)]

# resetting index
df_clean = df_moped_bicycle.reset_index(drop=True)

print(df_clean)
