import numpy as np
import pandas as pd
import plotly.express as px

# starting parameters nad sources
# scope of estimation
start_year = 2019
last_data_year = 2025      
start_law = 2027  
end_year = 2029                 

# sources and ages
fatalities_file = 'sources/Verkeersdoden_vanaf_1950.csv'
age_groups = ['0 t/m 4', '5 t/m 9', '10 t/m 14', '15 t/m 19']   

# fraction of deaths caused by head injury (source from CBS)
head_injury_share = 0.63

# fraction of decrease in fatal head injury (from SWOV)
helmet_effect = 0.71 

blue_year_shift = 0.0           # 0 = paste the snorfiets percentages as they are, 0.5 = mid-year like the group

# toggle for saving graph
save_graph = False


# loading in fatalities dataframe and taking necessary info
df_fatalities = pd.read_csv(fatalities_file)
df_bicycle = df_fatalities[df_fatalities['TransportMode'] == 'Bicycle']
df_underage = df_bicycle[df_bicycle['Age group'].isin(age_groups)]

fatal_per_year = df_underage.groupby('Year')['Fatalities'].sum().to_dict()

# there is no 2026 data of cyclist fatalities yet, so the 2025 value is used for 2026 and beyond
baseline_fatalities = fatal_per_year[last_data_year]

# blue line: snorfiets effect decrease in fatalities
effect_years = [0, 1, 2, 3]

# values from question 2
effect_values = [0.0, 0.137, 0.238, 0.320]

# function for ploting the snorfiets effect on e bikes
def snorfiets_effect(year):

    # years since the law, interpolates the values to coming years using last year 
    years_since_law = year + blue_year_shift - start_law

    return np.interp(years_since_law, effect_years, effect_values)


# green line is decline of the ebike population -> thus reduction in deaths
# ebike population certain % of cycling 12 - 17 year-olds (from question 2)
group_no_law = {2025: 29.0, 2026: 33.6, 2027: 38.2, 2028: 42.7, 2029: 47.3}
group_with_law = {2027: 35.6, 2028: 34.7, 2029: 34.1}

# function for ploting the population decline on e bikes
def population_decline(year):

    # return fraction of much e bike use decreases compared to no law
    return 1 - group_with_law[year] / group_no_law[year]


# calculation of ebike population per year
# csv with the ebike share of cyclists of 12 and older (from question 2)
survey_shares = {2021: 29.1, 2023: 36.5, 2025: 43.0} 

survey_years = sorted(survey_shares.keys())

# list for the values of each year 
survey_values = []

for year in survey_years:
    survey_values.append(survey_shares[year])

# straight line through the survey points for the years outside of the survey
slope, intercept = np.polyfit(survey_years, survey_values, 1)

def ebike_share(year):

    # between the survey years: interpolate, outside of them: extend the line
    if survey_years[0] <= year <= survey_years[-1]:
        share = np.interp(year, survey_years, survey_values)
    else:
        share = slope * year + intercept
    share = min(max(share, 0), 100)
    return share / 100

# fraction of the remaining ebike deaths that the helmet prevents (assuming everyone wears one)
helmet_cut = head_injury_share * helmet_effect

# preparing data for plotting from 2019 to 2026
past_years = []
past_total = []
past_ebike = []

for year in range(start_year, start_law):
    if year <= last_data_year:
        total = fatal_per_year[year]
    else:
        total = baseline_fatalities
    past_years.append(year)
    past_total.append(total)
    past_ebike.append(total * ebike_share(year))

# data for the lines after the implementation of the law

# lines start from the last passing year
line_years = [past_years[-1]]
no_law_line = [past_ebike[-1]]
green_line = [past_ebike[-1]]
blue_line = [past_ebike[-1]]

for year in range(start_law, end_year + 1):

    # if no law is passed
    no_law = baseline_fatalities * ebike_share(year)

    # if e bike fatalities declines (from going to different modes of transport)
    green = no_law * (1 - population_decline(year))

    # if e bike fatalities declines (assuming same decrease as for snorfietsen)
    blue = no_law * (1 - snorfiets_effect(year)) * (1 - helmet_cut)

    line_years.append(year)
    no_law_line.append(no_law)
    green_line.append(green)
    blue_line.append(blue)

if __name__ == '__main__':

    # plotting the graph
    df_past = pd.DataFrame({'Year': past_years, 'Fatalities': past_total})
    fig = px.line(df_past, x = 'Year', y = 'Fatalities', labels = {'Fatalities': 'Fatalities per year'}, title = 'Fatal underage cyclists and ebike fatalities with a helmet law prediction')
    fig.update_traces(name = 'Fatal underage cyclists', showlegend = True, line = dict(color = 'black'))

    # adding the lines
    fig.add_scatter(x = past_years, y = past_ebike, mode = 'lines', name = 'Estimation of e-bike population in all cyclists', line = dict(color = 'red'))
    fig.add_scatter(x = line_years, y = no_law_line, mode = 'lines', name = 'No law impemented', line = dict(dash = 'dot', color = 'grey'))

    fig.add_scatter(x = line_years, y = blue_line, mode = 'lines', name = 'Law: snorfiets percentages + helmet safety effect', line = dict(color = 'blue'))
    fig.add_scatter(x = line_years, y = green_line, mode = 'lines', name = 'Difference (mostly the effect of helmet protection)', line = dict(width = 0), fill = 'tonexty', fillcolor = 'lightgrey')
    fig.add_scatter(x = line_years, y = green_line, mode = 'lines', name = 'Law: decline ebike population', line = dict(color = 'green'))

    fig.add_vline(x = start_law, line_dash = 'dash', line_color = 'grey', annotation_text = 'Planned helmet law')
    fig.update_xaxes(dtick = 1)

    fig.show()

    # saving figure to graphs folder
    if save_graph == True:

        fig.write_image('graphs/vraag4_fatal_ebike_graph.png', scale = 2)