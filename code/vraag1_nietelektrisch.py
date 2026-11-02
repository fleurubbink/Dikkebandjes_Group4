from tkinter import Tk, filedialog
import pandas as pd
import plotly.express as px


seh_file = filedialog.askopenfilename(title="Selecteer Aantal_SEHbezoeken.csv", filetypes=[("CSV-bestanden", "*.csv")])

df = pd.read_csv(seh_file, encoding="cp1252", sep=';')
print(df.head())


graph1 = px.line(df, x="jaar", y="niet_elektrische_fiets", color="leeftijd", markers=True, 
                 title="SEH-bezoeken na ongevallen met niet-elektrische fietsen", color_discrete_map={'0_11': 'green', '12_17': 'yellow'})
graph1.update_layout(template="plotly_dark",xaxis_title="Jaar", yaxis_title="Aantal SEH-bezoeken", legend_title="Leeftijdsgroep", 
                     xaxis=dict(tickmode="linear", tick0=0, dtick=1), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
legend_names = ["Kinderen van 0-11 jaar", "Jongeren van 12-17 jaar"]
for idx, name in enumerate(legend_names):
    graph1.data[idx].name = name
    graph1.data[idx].hovertemplate = name
graph1.show()



