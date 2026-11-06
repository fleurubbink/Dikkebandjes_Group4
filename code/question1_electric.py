import pandas as pd
import plotly.express as px
from pathlib import Path

# reads the CSV file with the data on bike-related ER visits among the youth
df = pd.read_csv('data/Aantal_SEHbezoeken.csv', sep=';')
print(df.head())

# creates a line graph with the data on bike-related ER visits among the youth
graph2 = px.line(df, x="jaar", y="elektrische_fiets", color="leeftijd", markers=True, 
                 title="ER-visits following accidents with electric bikes", color_discrete_map={'0_11': 'green', '12_17': 'red'})

# adjusts the layout of the graph
graph2.update_layout(xaxis_title="Year", yaxis_title="Number of ER Visits", legend_title="Age Group", 
                     xaxis=dict(tickmode="linear", tick0=0, dtick=1), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

# adjusts the width of the ticks on the x-axis
graph2.update_xaxes(tickwidth=1)

# adjusts the legend and hovertext of the graph
legend_names = ["Children aged 0-11", "Youth aged 12-17"]
for idx, name in enumerate(legend_names):
    graph2.data[idx].name = name
    graph2.data[idx].hovertemplate = name
graph2.show()

# saves the graph as a PNG file in the "graphs" folder
Graph_folder = Path("graphs")
Graph_folder.mkdir(exist_ok=True)   # creates the folder if it doesn't exist yet
graph2.write_image(Graph_folder /"vraag1_elecrtic.png", scale=2)
