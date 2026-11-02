"""
Compares fatalities from two sources BRON (ongevallen_regio_BRON.csv)
and the fatalities file from (Verkeersdoden_vanaf_1950) in fatal_bicycle_moped_accidents.py.
"""

import pandas as pd
import matplotlib.pyplot as plt

from fatal_bicycle_moped_accidents import df_total_fatalities, starting_year

# preparing dataframe bron
df_road_incidents = pd.read_csv('data/ongevallen_regio_BRON.csv')
df_road_incidents = df_road_incidents[df_road_incidents['Year'] >= starting_year]

# dataframe from bron
df_BRON = df_road_incidents.groupby('Year', as_index = False)['Fatal'].sum()

comparison = df_BRON.merge(df_total_fatalities, on = 'Year', suffixes = ('_BRON', '_SWOV'))
comparison['Difference'] = comparison['Fatal'] - comparison['Fatalities']
print(comparison.rename(columns = {'Fatal': 'BRON', 'Fatalities': 'SWOV'}).to_string(index = False))

if __name__ == '__main__':
    plt.plot(df_BRON['Year'], df_BRON['Fatal'], label = 'BRON')
    plt.plot(df_total_fatalities['Year'], df_total_fatalities['Fatalities'], label = 'SWOV')

    plt.xlabel('Year')
    plt.ylabel('Fatalities')
    plt.title('Fatalities per year: BRON vs SWOV')
    plt.legend()
    plt.ylim(bottom=0)
    plt.gca().yaxis.grid(True)

    plt.show()
