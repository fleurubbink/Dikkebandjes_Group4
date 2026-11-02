#import the necessary libraries, pandas for data manipulation and plotly for visualization
import pandas as pd
import plotly.express as px

# importing csv and converting to a dataframe
df_fatal_accidents = pd.read_csv('sources/Verkeersdoden_vanaf_1950.csv')

#cleaning up the data to only include bicycle fatalities from 2013 and later, and only for the age groups 0-19
df_fatal_accidents_2013_plus = df_fatal_accidents[(df_fatal_accidents['Year'] >= 2013) & 
                                                  (df_fatal_accidents['TransportMode'].isin(['Bicycle'])) & 
                                                  (df_fatal_accidents['Age group'].isin(['0 t/m 4', '5 t/m 9', '10 t/m 14', '15 t/m 19']))]

bicycle_deaths = df_fatal_accidents_2013_plus.groupby('Year', as_index=False)['Fatalities'].sum()

#Here new data points are made for the for the years 2026 to 2028.
#This is based on the rate of decrease in moped fatalitties after the helmet was made mandatory in 2023.
#The rate of decrease is then put into a linear function to predict the number of bicycle fatalities for the years 2026 to 2028, in the form y = ax + b

moped_2023 = 11
moped_2025 = 7
rate_moped = (moped_2023 - moped_2025) / moped_2023


bicycle_2028 = 19 * (1 - rate_moped)
a = (bicycle_2028 - 19) / 3
b = 21
bicycle_2026 = a * 1 + b
bicycle_2027 = a * 2 + b

bicycle_extension = [19, bicycle_2026, bicycle_2027, bicycle_2028]
years_extension = [2025, 2026, 2027, 2028]

upper_bound = [19, 21, 23, 25]
lower_bound = [19, 16, 13, 10]

#plot the data, with the prediction data points for the years 2026 to 2028
fig = px.line(bicycle_deaths, x='Year', y='Fatalities', title='Bicycle fatalities in the Netherlands (2013-2028)')
fig.update_traces(name='Bicycle fatalities (2013-2025)', showlegend=True)

fig.add_scatter(x=years_extension, y=upper_bound, mode='lines', line=dict(width=0), showlegend=False)
fig.add_scatter(x=years_extension, y=lower_bound, mode='lines', line=dict(width=0), name='Possible futures', fill='tonexty', fillcolor='rgba(255, 0, 0, 0.2)')

fig.add_scatter(x=years_extension, y=bicycle_extension, mode='lines', name='Predicted fatalities (2026-2028)', line=dict(dash='dash', color='red'))
fig.show()
