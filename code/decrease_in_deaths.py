import pandas as pd
import plotly.express as px

# importing csv and converting to a dataframe
df_fatal_accidents = pd.read_csv('data/Verkeersdoden_vanaf_1950.csv')
#cleaning up the data to only include bicycle fatalities from 2013 and later, and only for the age groups 0-19
df_fatal_accidents_2013_plus = df_fatal_accidents[(df_fatal_accidents['Year'] >= 2013) & 
                                                  (df_fatal_accidents['TransportMode'].isin(['Bicycle'])) & 
                                                  (df_fatal_accidents['Age group'].isin(['0 t/m 4', '5 t/m 9', '10 t/m 14', '15 t/m 19']))]

bicycle_deaths = df_fatal_accidents_2013_plus.groupby('Year', as_index=False)['Fatalities'].sum()
print(bicycle_deaths)

#prediction of bicycle fatalities in 2028 based on moped trend, 19 is bicycle deaths in 2025, 
# 36,4% is the rate of decrease for moped possession after the helmet requirement
bicycle_2028 = 19 * (1 - 0.364)
a = (bicycle_2028 - 19) / 3
b = 21
bicycle_2026 = a * 1 + b
bicycle_2027 = a * 2 + b

bicycle_extension = [19, bicycle_2026, bicycle_2027, bicycle_2028]
years_extension = [2025, 2026, 2027, 2028]

upper_bound = [19, 21, 23, 25]
lower_bound = [19, 16, 13, 10]

#plot the data
fig = px.line(bicycle_deaths, x='Year', y='Fatalities', title='Bicycle fatalities in the Netherlands (2013-2028)')
fig.update_traces(name='Bicycle fatalities (2013-2025)', showlegend=True)

fig.add_scatter(x=years_extension, y=upper_bound, mode='lines', line=dict(width=0), showlegend=False)
fig.add_scatter(x=years_extension, y=lower_bound, mode='lines', line=dict(width=0), name='Possible futures', fill='tonexty', fillcolor='rgba(255, 0, 0, 0.2)')

fig.add_scatter(x=years_extension, y=bicycle_extension, mode='lines', name='Predicted fatalities (2026-2028)', line=dict(dash='dash', color='red'))
fig.show()

moped_2023 = 11
moped_2025 = 7
rate_moped = (moped_2023 - moped_2025) / moped_2023 * 100
#36,4%