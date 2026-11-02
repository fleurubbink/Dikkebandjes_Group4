from tkinter import Tk, filedialog
import pandas as pd
import plotly.express as px

df = pd.read_csv('data/(Elektrisch)_fietsen_onder_jongeren.csv', sep=';')
print(df.head())

graph = px.line(df, x="jaar", y="percentage", color="soort_fiets", markers=True, 
                 title="Trend in (elektric) biking among youth", 
                 color_discrete_map={'elektrisch': 'orange', 'uitsluitend_elektrisch': 'yellow', 'uitsluitend_niet_elektrisch': 'red'})
graph.update_layout(template="plotly_dark", xaxis_title="Year", yaxis_title="Percentage bikers", legend_title="Mode of biking", 
                     xaxis=dict(tickmode="linear", tick0=0, dtick=1), yaxis=dict(tickmode="linear", tick0=0, dtick=10), 
                     legend=dict(yanchor="top", y=0.79, xanchor="left", x=0.05))
graph.update_xaxes(tickwidth=1)
legend_names = ["Elektric", "Solely electric", "Soleley non-electric"]
for idx, name in enumerate(legend_names):
    graph.data[idx].name = name
    graph.data[idx].hovertemplate = name
graph.show()
