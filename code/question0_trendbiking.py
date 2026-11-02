import pandas as pd
import plotly.express as px
from pathlib import Path

# seh_file = filedialog.askopenfilename(title="Selecteer (Elektrisch)_fietsen_onder_jongeren", filetypes=[("CSV-bestanden", "*.csv")])

# reads the CSV file with the data on biking trends among youth
df = pd.read_csv('data/(Elektrisch)_fietsen_onder_jongeren.csv', sep=';')
print(df.head())

# creates a line graph with the data on biking trends among youth
graph = px.line(df, x="jaar", y="percentage", color="soort_fiets", markers=True, 
                 title="Trend in (elektric) biking among youth", 
                 color_discrete_map={'elektrisch': 'orange', 'uitsluitend_elektrisch': 'yellow', 'uitsluitend_niet_elektrisch': 'red'})

# adjusts the layout of the graph
graph.update_layout(template="plotly_dark", xaxis_title="Year", yaxis_title="Percentage bikers", legend_title="Mode of biking", 
                     xaxis=dict(tickmode="linear", tick0=0, dtick=1), yaxis=dict(tickmode="linear", tick0=0, dtick=10), 
                     legend=dict(yanchor="top", y=0.79, xanchor="left", x=0.05))

# adjusts the width of the ticks on the x-axis
graph.update_xaxes(tickwidth=1)

# adjusts the legend and hovertext of the graph
legend_names = ["Elektric", "Solely electric", "Soleley non-electric"]
for idx, name in enumerate(legend_names):
    graph.data[idx].name = name
    graph.data[idx].hovertemplate = name
graph.show()

# saves the graph as a PNG file in the "graphs" folder
Graph_folder = Path("graphs")
Graph_folder.mkdir(exist_ok=True)   # creates the folder if it doesn't exist yet
graph.write_image(Graph_folder /"vraag0_trendbiking.png", scale=2)
