#Guestion 2 


# Main question:
# To what extent will underage e-bike users change their attitude towards riding a e-bike? 

# Assignment question:
# To what extent will the introduction of mandatory helmet requirement change the use of e-bikes? 
# > Compare the underage e-bike users with the "snorfiets users decline thanks to the then implemented helmet law (2023)" 

# Sources:
# https://neo4j.com/blog/graph-data-science/build-predictive-model-python/
# Aanvullende module Bewegen en Ongevallen van de Leefstijlmonitor, CBS i.s.m. RIVM 2021. Aandeel fietsers 2021-2025
# https://www.cbs.nl/nl-nl/visualisaties/verkeer-en-vervoer/vervoermiddelen-en-infrastructuur/bromfietsen-snorfietsen

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
from pathlib import Path

pio.renderers.default = "notebook"
DATA_DIR = Path("sources")

# ---------------------- Settings (change these to run sensitivity checks) ---------------------- #
Snorfiets_Wetgeving_Ingang  = 2023              # national helmet obligation for snorfiets
Start_Fit                   = 2019              # 
Covid                       = []                # e.g. [2020, 2021] to leave out the COVID years
End_Year                    = 2029              # end of the prediction horizon
Start_Law                   = 2027 + 8 / 12     # planned start of the law: 1 September 2027
Survey_Moment               = 0.5               # treat each e-bike survey year as measured mid-year
Pre_Flatten                 = 0.5               # 1 = normal least-squares slope, 0 = flat line at the window mean

# ---------------------- Load the data ---------------------- #
moped_possesion = pd.read_csv(DATA_DIR / "Voertuigen met een bromfietskenteken, 1 januari (x 1 000).csv", sep=";", decimal=",")

# filter the data 
moped_possesion_filtered = moped_possesion[["Jaar", "Snorfiets", "Bromfiets"]]

# RIVM/CBS Leefstijlmonitor, 12-17 year-olds, in % of the cycling 12-17 year-olds
ebike_minors = pd.read_csv(Path("data") / "(Elektrisch)_fietsen_onder_jongeren.csv", sep=';')

ebike_filtered = (ebike_minors[ebike_minors["soort_fiets"] == "elektrisch"]
                  .rename(columns={"jaar": "Jaar", "percentage": "Elektrisch fietsen"})
                  [["Jaar", "Elektrisch fietsen"]]
                  .reset_index(drop=True))

bike_filtered = (ebike_minors[ebike_minors["soort_fiets"] == "uitsluitend_niet_elektrisch"]
                  .rename(columns={"jaar": "Jaar", "percentage": "Normale fietsen"})
                  [["Jaar", "Normale fietsen"]]
                  .reset_index(drop=True))
# Used Claude in determining how to read the data


# ---------------------- Linear trend fit function ---------------------- #

def linear_fit(years, values, exclude=(), flatten=1.0):
    """Least-squares line through (years, values); returns slope, intercept."""
    years  = np.asarray(years,  dtype=float)
    values = np.asarray(values, dtype=float)
    keep   = ~np.isin(years, list(exclude))
    slope, intercept = np.polyfit(years[keep], values[keep], 1)
    if flatten !=1.0:
        x0, y0 = years[keep].mean(), values[keep].mean()
        slope *= flatten
        intercept = y0 - slope *x0
    return slope, intercept

# ----------------------  Graph 1: snorfiets and bromfiets + trend fits ---------------------- #

pre_law  = moped_possesion_filtered[moped_possesion_filtered["Jaar"].between(Start_Fit, Snorfiets_Wetgeving_Ingang)]
post_law = moped_possesion_filtered[moped_possesion_filtered["Jaar"] >= Snorfiets_Wetgeving_Ingang]  # 2023 is the shared anchor
last_actual_year = int(post_law["Jaar"].max())
 
years_all   = np.arange(Start_Fit, End_Year + 1)                    # pre-law trend,  extended to the horizon
years_after = np.arange(Snorfiets_Wetgeving_Ingang, End_Year + 1)   # post-law trend, extended to the horizon
 
Trend_pre   = f"Trend fit ({Start_Fit}-{Snorfiets_Wetgeving_Ingang}, extended)"
Trend_after = f"Trend fit ({Snorfiets_Wetgeving_Ingang}-{last_actual_year}, extended)"


pre_fits    = {}
post_fits   = {}
frames      = []

for vehicle in ["Snorfiets", "Bromfiets"]:
    pre_fits [vehicle]  = linear_fit(pre_law["Jaar"], pre_law[vehicle], Covid, flatten=Pre_Flatten)
    post_fits[vehicle] = linear_fit(post_law["Jaar"], post_law[vehicle])
    slope_pre,  icpt_pre  = pre_fits [vehicle]
    slope_post, icpt_post = post_fits[vehicle]

# Make dataframes for the 
    frames.append(pd.DataFrame({
        "Year": moped_possesion_filtered["Jaar"],
        "Vehicles (x1000)": moped_possesion_filtered[vehicle],
        "Vehicle": vehicle,
        "Type": "Actual"}))

    frames.append(pd.DataFrame({
        "Year": years_all,
        "Vehicles (x1000)": slope_pre * years_all + icpt_pre,
        "Vehicle": vehicle,
        "Type": Trend_pre}))

    frames.append(pd.DataFrame({
        "Year": years_after,
        "Vehicles (x1000)": slope_post * years_after + icpt_post,
        "Vehicle": vehicle,
        "Type": Trend_after}))

df_moped = pd.concat(frames, ignore_index=True)

fig1 = px.line(
    df_moped, x="Year", y="Vehicles (x1000)",
    color="Vehicle", line_dash="Type", markers=True,
    color_discrete_map={"Snorfiets": "blue", "Bromfiets": "red"},
    line_dash_map={"Actual": "solid", Trend_pre: "dot", Trend_after: "dash"},
    title="Snorfiets and bromfiets fleet (1 January): pre-law and post-law trend fits")

fig1.for_each_trace(lambda t: t.update(mode="lines") if "Trend" in t.name else None)

fig1.add_vline(x=Snorfiets_Wetgeving_Ingang, line_dash="dash", line_color="grey",
               annotation_text=f"Snorfiets helmet law ({Snorfiets_Wetgeving_Ingang})")

fig1.update_xaxes(dtick=1)

fig1.update_layout(
    legend=dict(
        orientation="h",       
        yanchor="top",
        y=-0.15,               
        xanchor="left",
        x=0,
        title_text=""),        
    margin=dict(t=80, b=150)) 

# ----------------------  Law effect from the snorfiets data  ---------------------- #
#    effect(t) = 1 - actual / trend-without-law, t = years since the law

snor    = moped_possesion_filtered.set_index("Jaar")["Snorfiets"]
slope_s, intercept_s = pre_fits["Snorfiets"]          # was: fits["Snorfiets"]
gap     = 1 - snor / (slope_s * snor.index + intercept_s)
post    = gap[gap.index > Snorfiets_Wetgeving_Ingang]

effect_t = np.concatenate([[0], (post.index - Snorfiets_Wetgeving_Ingang).to_numpy()])
effect_v = np.concatenate([[0], post.to_numpy()])

# Check if effect gets calculated 
# print("Effect curve (years since law -> share below trend):")
# for t, e in zip(effect_t, effect_v):
#     print(f"  t={t:.0f}: {e:.1%}")


# ---------------------- Graph 2: underage e-bike users, no-law trend vs. with-law trend ---------------------- #

slope_ebikes, intercept_ebikes = linear_fit(ebike_filtered["Jaar"], ebike_filtered["Elektrisch fietsen"])

years_bikes = np.arange(ebike_filtered["Jaar"].min(), End_Year + 1)
baseline_ebikes = slope_ebikes * years_bikes + intercept_ebikes

# years since the (planned) e-bike law at each survey moment
t_since_law = years_bikes + Survey_Moment - Start_Law

effect = np.interp(t_since_law, effect_t, effect_v)
with_law = baseline_ebikes * (1 - effect)

# These baselines are for maintainting a 100% "usage" scenario, 
# with the assumption that those who stop using e-bikes are goint to use normal bikes again
baseline_non_ebikes = 100 - baseline_ebikes
with_law_non_ebikes = 100 - with_law

GROUP_E = "Electric (incl. mixed use)"
GROUP_N = "Non-electric only"
ACTUAL  = "Actual (RIVM/CBS)"
NO_LAW  = "Prediction without law (trend)"
LAW     = "Prediction with law (snorfiets effect)"

last_obs  = ebike_filtered["Jaar"].max()
from_last = years_bikes >= last_obs
# Making dataframes for eacht section of the timeline, current and speculation with and without the law 
# --- e-bike users ---
df_actual_e = pd.DataFrame({
    "Year": ebike_filtered["Jaar"],
    "% of cycling 12-17 year-olds": ebike_filtered["Elektrisch fietsen"],
    "Group": GROUP_E,
    "Type": ACTUAL})

df_no_law_e = pd.DataFrame({
    "Year": years_bikes,
    "% of cycling 12-17 year-olds": baseline_ebikes,
    "Group": GROUP_E,
    "Type": NO_LAW})

df_law_e = pd.DataFrame({
    "Year": years_bikes[from_last],
    "% of cycling 12-17 year-olds": with_law[from_last],
    "Group": GROUP_E,
    "Type": LAW})

# --- non-electric users ---
df_actual_n = pd.DataFrame({
    "Year": bike_filtered["Jaar"],
    "% of cycling 12-17 year-olds": bike_filtered["Normale fietsen"],
    "Group": GROUP_N,
    "Type": ACTUAL})

df_no_law_n = pd.DataFrame({
    "Year": years_bikes,
    "% of cycling 12-17 year-olds": baseline_non_ebikes,
    "Group": GROUP_N,
    "Type": NO_LAW})

df_law_n = pd.DataFrame({
    "Year": years_bikes[from_last],
    "% of cycling 12-17 year-olds": with_law_non_ebikes[from_last],
    "Group": GROUP_N,
    "Type": LAW})

df_ebike = pd.concat([df_actual_e, df_no_law_e, df_law_e,
                      df_actual_n, df_no_law_n, df_law_n], ignore_index=True)

fig2 = px.line(
    df_ebike, x="Year", y="% of cycling 12-17 year-olds",
    color="Group", line_dash="Type", markers=True,
    color_discrete_map={GROUP_E: "green", GROUP_N: "purple"},
    line_dash_map={ACTUAL: "solid", NO_LAW: "dot", LAW: "dash"},
    title="Underage (12-17) e-bike use: continued growth vs. helmet law")

fig2.for_each_trace(lambda t: t.update(mode="lines") if ACTUAL not in t.name else None)

fig2.add_vline(x=Start_Law, line_dash="dash", line_color="grey",
               annotation_text="Planned helmet law")

fig2.update_xaxes(dtick=1)
fig2.update_layout(
    legend=dict(
        orientation="h",      
        yanchor="top",
        y=-0.15,               
        xanchor="left",
        x=0,
        title_text=""),       
    margin=dict(t=80, b=150))       

# Check if effect gets calculated 
# print("\nE-bike scenario (% of cycling 12-17 year-olds):")
# print(pd.DataFrame({"Year": years_bikes, "No law": baseline_ebikes.round(1),
#                     "With law": with_law.round(1)}).tail(5).to_string(index=False))


Graph_folder = Path("graphs")
Graph_folder.mkdir(exist_ok=True)   # creates the folder if it doesn't exist yet

fig1.write_image(Graph_folder /"graph1_moped.png", scale=2)
fig2.write_image(Graph_folder /"graph2_ebike.png", scale=2)
