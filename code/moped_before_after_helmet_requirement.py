import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#Gather all the data
moped_possesion = pd.read_csv('data/Voertuigen met een bromfietskenteken, 1 januari (x 1 000).csv', sep=';', decimal=',')

#filter the data for the correct ages and vehicles
moped_possesion_filtered = moped_possesion[["Jaar", "Snorfiets", "Bromfiets"]]
#moped_possesion_filtered_melted = pd.melt(moped_possesion_filtered, id_vars='Jaar')
#print(moped_possesion_filtered)


#code for the plots
def plot_moped_possesion():
    fig, ax = plt.subplots(figsize=(10, 6))
    x_axis = moped_possesion_filtered.Jaar
    y_axis1 = moped_possesion_filtered.Snorfiets
    y_axis2 = moped_possesion_filtered.Bromfiets

    ax.plot(x_axis, y_axis1, label = "Snorfiets", color = "tab:blue")
    ax.plot(x_axis, y_axis2, label = "Bromfiets", color = "tab:red")

    ax.axvline(x=2023, color='red', linestyle='--', label='Helm verplichting snorfietsers')

    ax.set_ylim(0, 1000)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(100))

    ax.set_xlabel("Jaar")
    ax.set_ylabel("Aantal voertuigen (x 1.000)")
    ax.set_title("Aantal brom- en snorfietsen per jaar")

    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    plt.show()
    return fig, ax

plot_moped_possesion()
