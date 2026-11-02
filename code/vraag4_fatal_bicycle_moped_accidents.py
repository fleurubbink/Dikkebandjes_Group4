"""
Loads the fatalities file (Verkeersdoden_vanaf_1950.csv), keeps 2013 onwards and builds yearly fatality series per transport mode and age group.
"""

import pandas as pd
import matplotlib.pyplot as plt

data_path = 'sources/Verkeersdoden_vanaf_1950.csv'
starting_year = 2013

# the dataset groups 15-19 together so 18-19 year olds are also included in the data
minor_age_groups = ['0 t/m 4', '5 t/m 9', '10 t/m 14', '15 t/m 19']

def load_fatalities(path = data_path, starting_year = starting_year):
    df = pd.read_csv(path)
    df = df.drop(columns = 'Vervoerswijze') 

    # reset index for the dataframe
    return df[df['Year'] >= starting_year].reset_index(drop = True)

def fatalities_per_year(dataframe, transport_mode = None, ages = None):

    # apply specified transport modes
    if transport_mode is not None:
        dataframe = dataframe[dataframe['TransportMode'].isin(transport_mode)]

    # applied specified ages
    if ages is not None:
        dataframe = dataframe[dataframe['Age group'].isin(ages)]
    return dataframe.groupby('Year', as_index = False)['Fatalities'].sum()


# preparing dataframes for plotting 
df_time_period = load_fatalities()

df_total_fatalities = fatalities_per_year(df_time_period)
df_bicycle_per_year = fatalities_per_year(df_time_period, transport_mode = ['Bicycle'])
df_moped_per_year = fatalities_per_year(df_time_period, transport_mode = ['Moped'])
df_minor_bicycle_per_year = fatalities_per_year(df_time_period, transport_mode = ['Bicycle'], ages = minor_age_groups)
df_minor_moped_per_year = fatalities_per_year(df_time_period, transport_mode = ['Moped'], ages = minor_age_groups)

# function for plotting
def plot_overview():
    plt.figure()

    # plotting dataframes
    plt.plot(df_total_fatalities['Year'], df_total_fatalities['Fatalities'], label = 'Total (all transport modes)')
    plt.plot(df_bicycle_per_year['Year'], df_bicycle_per_year['Fatalities'], label = 'Bicycle')
    plt.plot(df_moped_per_year['Year'], df_moped_per_year['Fatalities'], label = 'Moped')
    plt.plot(df_minor_bicycle_per_year['Year'], df_minor_bicycle_per_year['Fatalities'], '--', label = 'Bicycle, minors')
    plt.plot(df_minor_moped_per_year['Year'], df_minor_moped_per_year['Fatalities'], '--', label = 'Moped, minors')

    # plot formatting
    plt.xlabel('Year')
    plt.ylabel('Fatalities')
    plt.title('Fatalities per year')
    plt.legend(loc = 'upper left')
    plt.ylim(top = 1000) 
    plt.ylim(bottom = 0) 
    plt.gca().yaxis.grid(True)

    plt.show()
    # graph_path = 'graphs/fatalities_per_year'
    # plt.savefig()

if __name__ == '__main__':
    plot_overview()
