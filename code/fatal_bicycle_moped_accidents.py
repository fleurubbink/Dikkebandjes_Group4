"""
Write something here about what the code does and stuff
"""

# importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# importing csv and converting to a dataframe
df_fatal_accidents = pd.read_csv('data/Verkeersdoden_vanaf_1950.csv')


#==== Preparing the dataset ====

# removing Vervoerswijze and keeping transportmode
df_fatal_accidents.drop('Vervoerswijze',inplace = True, axis = 1)

# keeping the time period from 2013-2025
time_period_mask = df_fatal_accidents['Year'] >= 2013 
df_time_period = df_fatal_accidents[(time_period_mask)]

# removing all transport modes except Bicycle and Moped 
bicycle_mask = df_time_period['TransportMode'] == 'Bicycle'
moped_mask = df_time_period['TransportMode'] == 'Moped'

# 3 seperate dataframes (1: Moped, 2: Bicycle, 3: Both)
df_moped = df_time_period[moped_mask]
df_bicycle = df_time_period[bicycle_mask]

df_moped_bicycle = df_time_period[(bicycle_mask | moped_mask)]

# removing data with 'Onbekend' age group label
df_moped_clean = df_moped[df_moped['Age group'] != 'Onbekend']
df_bicycle_clean = df_bicycle[df_bicycle['Age group'] != 'Onbekend']
df_moped_bicycle_clean = df_moped_bicycle[df_moped_bicycle['Age group'] != 'Onbekend']

# resetting indeces for the 3 data frames
df_moped_clean = df_moped_clean.reset_index(drop = True)
df_bicycle_clean = df_bicycle_clean.reset_index(drop = True)
df_moped_bicycle_clean = df_moped_bicycle_clean.reset_index(drop = True)

# list of ages for boolean mask
minor_age_groups = ['0 t/m 4', '5 t/m 9', '10 t/m 14', '15 t/m 19']

# dataframes for underage fatalities
df_fatal_minor_bicycle = df_bicycle_clean[df_bicycle_clean['Age group'].isin(minor_age_groups)]
df_fatal_minor_moped = df_moped_clean[df_moped_clean['Age group'].isin(minor_age_groups)]

#==== Visualising Data ====

"""
Plotting the total moped and bicycle fatalities per year regardless of age
"""
# grouping the fatalities per year
moped_fatal_per_year = df_moped_clean.groupby('Year', as_index = False)['Fatalities'].sum()
bicycle_fatal_per_year = df_bicycle_clean.groupby('Year', as_index = False)['Fatalities'].sum()

plt.plot(moped_fatal_per_year['Year'], moped_fatal_per_year['Fatalities'], label = 'Moped Fatalities')
plt.plot(bicycle_fatal_per_year['Year'], bicycle_fatal_per_year['Fatalities'], '-.', label = 'Bicycle Fatalities')

"""
Plotting the total moped and bicycle fatalities per year of minors
Moped ages: 15 to 19
Bicycle ages: 0 to 19
"""
# Keep in mind that the dataset groups 15 to 19 year old together, so numbers could be inflated

minor_moped_fatal_per_year = df_fatal_minor_moped.groupby('Year', as_index = False)['Fatalities'].sum()
minor_bicycle_fatal_per_year = df_fatal_minor_bicycle.groupby('Year', as_index = False)['Fatalities'].sum()

plt.plot(minor_moped_fatal_per_year['Year'], minor_moped_fatal_per_year['Fatalities'], label = 'Underage Moped Fatalities')
plt.plot(minor_bicycle_fatal_per_year['Year'], minor_bicycle_fatal_per_year['Fatalities'], '--', label = 'Underage Bicycle Fatalities')

plt.xlabel('Year')
plt.ylabel('Fatalities')
plt.title('Fatalities per Year')
plt.legend()

plt.ylim(bottom = 0)

plt.show()
