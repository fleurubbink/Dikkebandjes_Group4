import pandas as pd
import plotly.express as px

# importing csv and converting to a dataframe
df_fatal_accidents = pd.read_csv('data/Verkeersdoden_vanaf_1950.csv')
df_fatal_accidents_2013_plus = df_fatal_accidents[(df_fatal_accidents['Year'] >= 2013) & 
                                                  (df_fatal_accidents['TransportMode'].isin(['Bicycle', 'Moped'])) & 
                                                  (df_fatal_accidents['Age group'].isin(['0 t/m 4', '5 t/m 9', '10 t/m 14', '15 t/m 19']))]


p1 = px.bar(df_fatal_accidents_2013_plus, x='Year', y='Fatalities')
p1.show()
#print(df_fatal_accidents_2013_plus.head())