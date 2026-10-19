import pandas as pd
import plotly.express as px

moped_sales = pd.read_csv('data/Aantal_nieuwverkochte_voertuigen_met_bromfietskenteken.csv')
#moped_possession = pd.read_csv('data/Aantal_voertuigen_met_bromfietskenteken.csv')
moped_age_possession = pd.read_csv('data/Brom- en snorfietsen, naar leeftijd eigenaar, 1 januari (x 1 000).csv', sep=';')
moped_possession = pd.read_csv('data/Voertuigen met een bromfietskenteken, 1 januari (x 1 000).csv', sep=';')


