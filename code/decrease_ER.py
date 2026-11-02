import pandas as pd
import plotly.express as px

# importing csv and converting to a dataframe
df_ER = pd.read_csv('data/Aantal_SEHbezoeken.csv', sep=';')
df_ER_filtered = df_ER.groupby('jaar', as_index=False)['elektrische_fiets'].sum()

#prediction of ER visits in 2028 based on moped trend, 2024 = 3200, 2025 is ongeveer 3500 -> 8% increase
bicycle_2028 = 3500 * (1 - 0.364)
a = (bicycle_2028 - 3500) / 3
b = 3500
bicycle_2026 = a * 1 + b
bicycle_2027 = a * 2 + b

bicycle_extension = [3200, 3500, bicycle_2026, bicycle_2027, bicycle_2028]
years_extension = [2024, 2025, 2026, 2027, 2028]

upper_bound = [3200, 3600, 3800, 4000, 4200]
lower_bound = [3200, 3400, 2800, 2200, 1600]


#plot the data
fig = px.line(df_ER_filtered, x='jaar', y='elektrische_fiets', title='ER visits for electric bikes in the Netherlands')
fig.update_traces(name='ER visits (2020-2024)', showlegend=True)

fig.add_scatter(x=years_extension, y=upper_bound, mode='lines', line=dict(width=0), showlegend=False)
fig.add_scatter(x=years_extension, y=lower_bound, mode='lines', line=dict(width=0), name='Possible futures', fill='tonexty', fillcolor='rgba(255, 0, 0, 0.2)')
fig.add_scatter(x=years_extension, y=bicycle_extension, mode='lines', name='Predicted fatalities (2025-2028)', line=dict(dash='dash', color='red'))

fig.show()