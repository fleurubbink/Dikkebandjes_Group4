import pandas as pd
import plotly.express as px
from pathlib import Path 

# reads the CSV file with the data on e-bike-related ER visits among youth
df = pd.read_csv('data/Aantal_SEHbezoeken.csv', sep=';')
print(df.head())

# creates a line graph with the data on e-bike-related ER visits among youth
graph1 = px.line(df, x="jaar", y="niet_elektrische_fiets", color="leeftijd", markers=True, 
                 title="ER-visits following accidents with non-electric bikes", color_discrete_map={'0_11': 'green', '12_17': 'red'})

# adjusts the layout of the graph
graph1.update_layout(xaxis_title="Year", yaxis_title="Number of ER Visits", legend_title="Age Group", 
                     xaxis=dict(tickmode="linear", tick0=0, dtick=1), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

# adjusts the legend and hovertext of the graph
legend_names = ["Children aged 0-11", "Youth aged 12-17"]
for idx, name in enumerate(legend_names):
    graph1.data[idx].name = name
    graph1.data[idx].hovertemplate = name
graph1.show()

# saves the graph as a PNG file in the "graphs" folder
Graph_folder = Path("graphs")
Graph_folder.mkdir(exist_ok=True)   # creates the folder if it doesn't exist yet
graph1.write_image(Graph_folder /"question1_nonelectric.png", scale=2)


