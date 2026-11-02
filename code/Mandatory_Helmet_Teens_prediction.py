#Guestion 2 


# Main question:
# To what extent will underage e-bike users change their attitude towards riding a e-bike? 

# Assignment question:
# To what extent will the introduction of mandatory helmet requirement change the use of e-bikes? 
# > Compare the underage e-bike users with the "snorfiets users decline thanks to the then implemented helmet law (2023)" 

# Sources:
# https://neo4j.com/blog/graph-data-science/build-predictive-model-python/

# what do i need?
# 1. Population growth "snorfiets pupulation"
# 2. Graph "snorfiets population"
# 3. Determine the "decline rate"
#       3.1 if possible show different decline rate predictions?
# 4. Determine the population of minors with an e-bike 
# 5. Graph the population of minors with an e-bike
#       5.1 "predict" population growth of the e-bike 
#       5.2 "predict" population decline when the law is implemented
#
#
# AI statement I only used Claude Sonnet 5.5 during this assignment for discussing the data structures, 
# getting help with understanding linear fit implementation in python and making the graphs show the information better.



import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "notebook"
from pathlib import Path


# ---------------------- Settings (change these to run sensitivity checks) ---------------------- #
Snorfiets_Wetgeving_Ingang  = 2023              # national helmet obligation for snorfiets
Start_Fit, End_Fit          = 2019, 2023        # "pre-law" window used for the trend fits
Covid                       = []                # e.g. [2020, 2021] to leave out the COVID years
End_Year                    = 2029              # end of the prediction horizon
Start_Law                   = 2027 #+ 8 / 12    # planned: 1 September 2027
Survey_Moment               = 0.5               # treat each e-bike survey year as measured mid-year


# ---------------------- Load the data ---------------------- #
moped_possesion = pd.read_csv(
    'data/Voertuigen met een bromfietskenteken, 1 januari (x 1 000).csv',
    sep=';', decimal=',')

# filter the data 
moped_possesion_filtered = moped_possesion[["Jaar", "Snorfiets", "Bromfiets"]]

# RIVM/CBS Leefstijlmonitor, 12-17 year-olds: share of cycling 12-17 year-olds
# that cycles electrically (alone or combined with a normal bike)
ebike_minors = pd.read_csv('data\(Elektrisch)_fietsen_onder_jongeren.csv', sep=';')
ebike_filtered = (ebike_minors[ebike_minors["soort_fiets"] == "elektrisch"]
                  .rename(columns={"jaar": "Jaar", "percentage": "Elektrisch fietsen"})
                  [["Jaar", "Elektrisch fietsen"]]
                  .reset_index(drop=True))
# Used Claude in determining how to read the data


# ---------------------- Helper: linear trend fit ---------------------- #

def linear_fit(years, values, exclude=()):
    """Least-squares line through (years, values); returns slope, intercept."""
    years  = np.asarray(years,  dtype=float)
    values = np.asarray(values, dtype=float)
    keep   = ~np.isin(years, list(exclude))
    slope, intercept = np.polyfit(years[keep], values[keep], 1)
    return slope, intercept



# ----------------------  Graph 1: snorfiets and bromfiets + trend fits ---------------------- #

pre_law     = moped_possesion_filtered[moped_possesion_filtered["Jaar"].between(Start_Fit, End_Fit)]
years_all   = np.arange(Start_Fit, End_Year + 1)
Trend = f"Trend fit ({Start_Fit}-{End_Fit}, extended)"

fits   = {}
frames = []
for vehicle in ["Snorfiets", "Bromfiets"]:
    slope, intercept = linear_fit(pre_law["Jaar"], pre_law[vehicle], Covid)
    fits[vehicle] = (slope, intercept)

    frames.append(pd.DataFrame({
        "Year": moped_possesion_filtered["Jaar"],
        "Vehicles (x1000)": moped_possesion_filtered[vehicle],
        "Vehicle": vehicle,
        "Type": "Actual"}))
    frames.append(pd.DataFrame({
        "Year": years_all,
        "Vehicles (x1000)": slope * years_all + intercept,
        "Vehicle": vehicle,
        "Type": Trend}))

df_moped = pd.concat(frames, ignore_index=True)

fig1 = px.line(
    df_moped, x="Year", y="Vehicles (x1000)",
    color="Vehicle", line_dash="Type", markers=True,
    color_discrete_map={"Snorfiets": "blue", "Bromfiets": "red"},
    line_dash_map={"Actual": "solid", Trend: "dot"},
    title="Snorfiets and bromfiets fleet (1 January) with pre-law trend fit")
fig1.for_each_trace(lambda t: t.update(mode="lines") if "Trend" in t.name else None)
fig1.add_vline(x=Snorfiets_Wetgeving_Ingang, line_dash="dash", line_color="grey",
               annotation_text=f"Snorfiets helmet law ({Snorfiets_Wetgeving_Ingang})")
fig1.update_xaxes(dtick=1)


# ----------------------  Law effect from the snorfiets data  ---------------------- #
#    effect(t) = 1 - actual / trend-without-law, t = years since the law
#    (counts are on 1 January, so 2024 = one year after the 2023 law)

snor = moped_possesion_filtered.set_index("Jaar")["Snorfiets"]
slope_s, intercept_s = fits["Snorfiets"]
gap = 1 - snor / (slope_s * snor.index + intercept_s)
post = gap[gap.index > Snorfiets_Wetgeving_Ingang]

effect_t = np.concatenate([[0], (post.index - Snorfiets_Wetgeving_Ingang).to_numpy()])
effect_v = np.concatenate([[0], post.to_numpy()])
print("Effect curve (years since law -> share below trend):")
for t, e in zip(effect_t, effect_v):
    print(f"  t={t:.0f}: {e:.1%}")


# ---------------------- Graph 2: underage e-bike users, no-law trend vs. with-law trend ---------------------- #

slope_e, intercept_e = linear_fit(ebike_filtered["Jaar"], ebike_filtered["Elektrisch fietsen"])
years_e = np.arange(ebike_filtered["Jaar"].min(), End_Year + 1)
baseline = slope_e * years_e + intercept_e

# years since the (planned) e-bike law at each survey moment; np.interp gives 0
# before the law and holds the last observed effect after year 3
t_since_law = years_e + Survey_Moment - Start_Law
effect = np.interp(t_since_law, effect_t, effect_v)
with_law = baseline * (1 - effect)

OBS = "Actual (RIVM/CBS)"
NO_LAW = "Prediction without law (trend)"
LAW = "Prediction with law (snorfiets effect)"

last_obs = ebike_filtered["Jaar"].max()
from_last = years_e >= last_obs
df_ebike = pd.concat([
    pd.DataFrame({"Year": ebike_filtered["Jaar"],
                  "% of cycling 12-17 year-olds": ebike_filtered["Elektrisch fietsen"],
                  "Series": OBS}),
    pd.DataFrame({"Year": years_e, "% of cycling 12-17 year-olds": baseline, "Series": NO_LAW}),
    pd.DataFrame({"Year": years_e[from_last],
                  "% of cycling 12-17 year-olds": with_law[from_last], "Series": LAW}),
], ignore_index=True)

fig2 = px.line(
    df_ebike, x="Year", y="% of cycling 12-17 year-olds",
    color="Series", line_dash="Series", markers=True,
    color_discrete_map={OBS: "black", NO_LAW: "green", LAW: "orange"},
    line_dash_map={OBS: "solid", NO_LAW: "dot", LAW: "dash"},
    title="Underage (12-17) e-bike use: continued growth vs. helmet law")
fig2.for_each_trace(lambda t: t.update(mode="lines") if t.name != OBS else None)
fig2.add_vline(x=Start_Law, line_dash="dash", line_color="grey")
               #annotation_text="Planned helmet law (Sep 2027)")
fig2.update_xaxes(dtick=1)

print("\nE-bike scenario (% of cycling 12-17 year-olds):")
print(pd.DataFrame({"Year": years_e, "No law": baseline.round(1),
                    "With law": with_law.round(1)}).tail(5).to_string(index=False))


Graph_folder = Path("graphs")
Graph_folder.mkdir(exist_ok=True)   # creates the folder if it doesn't exist yet

fig1.write_image(Graph_folder /"graph1_moped.png", scale=2)
fig2.write_image(Graph_folder /"graph2_ebike.png", scale=2)
