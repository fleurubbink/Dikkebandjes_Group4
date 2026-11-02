import numpy as np
import matplotlib.pyplot as plt

from vraag4_fatal_bicycle_moped_accidents import df_bicycle_per_year, df_total_fatalities

# input parameters
ebike_percentage = 0.41         # percentage of ebike users in total cyclists       
head_injury_percentage = 0.63   # percentage of head injuries of total injuries (??)
helmet_fatality_drop = 0.71     # percentage of fatalities dropped since helmet requirement application
ebike_use_drop = 0.20           # drop in usage of ebike users
baseline_years = 3              # taking an average of 3 years

# baseline of fatalities
def baseline(df, n = baseline_years):
    return df.sort_values('Year').tail(n)['Fatalities'].mean()

baseline_cyclist_fatalities = baseline(df_bicycle_per_year)
baseline_total_fatalities = baseline(df_total_fatalities)
baseline_ebike_fatalities = baseline_cyclist_fatalities * ebike_percentage

# function that predicts the number of deaths avoided because of decrease in ebike usage and required helmet
def deaths_avoided(ridership_drop, compliance, ebike_deaths = baseline_ebike_fatalities, head_injury_percentage = head_injury_percentage, helmet_effect = helmet_fatality_drop):

    # fraction for 
    helmet_reduction = 1 - (head_injury_percentage * helmet_effect * compliance)

    # reduction of e-bike deaths
    after = ebike_deaths * (1 - ridership_drop) * (helmet_reduction)
    return ebike_deaths - after


def decompose(ridership_drop, compliance):
    exposure_only = deaths_avoided(ridership_drop, 0)
    helmet_only = deaths_avoided(0, compliance)
    total = deaths_avoided(ridership_drop, compliance)

    return {'exposure': exposure_only, 'helmet': helmet_only, 'overlap': total - exposure_only - helmet_only, 'total': total}


if __name__ == '__main__':
    print(f'Baseline (last {baseline_years} years): {baseline_cyclist_fatalities:.0f} cyclist deaths, '
          f'{baseline_ebike_fatalities:.0f} on e-bikes, {baseline_total_fatalities:.0f} in total')

    # scenario table
    print('\nDeaths avoided per year (% of all road deaths in brackets)')
    print('drop in e-bike use | compliance 0% | 50% | 100%')
    for drop in [0.0, 0.1, 0.2, 0.3, 0.5]:
        row = [deaths_avoided(drop, c) for c in (0, 0.5, 1.0)]
        print(f'{drop:>17.0%} | ' + ' | '.join(f'{x:5.1f} ({x / baseline_total_fatalities:.1%})' for x in row))

    d = decompose(ebike_use_drop, 0.5)
    print(f'\nQuestion 2 scenario (drop {ebike_use_drop:.0%}, compliance 50%): '
          f"exposure {d['exposure']:.1f}, helmet {d['helmet']:.1f}, "
          f"overlap {d['overlap']:.1f}, total {d['total']:.1f} deaths avoided "
          f"= {d['total'] / baseline_total_fatalities:.1%} of all road deaths")

    # plot 1: deaths avoided vs ridership drop, one line per compliance level
    drops = np.linspace(0, 0.5, 51)
    plt.figure()
    for c in (0, 0.25, 0.5, 0.75, 1.0):
        plt.plot(drops * 100, deaths_avoided(drops, c), label=f'compliance {c:.0%}')
    plt.axvline(ebike_use_drop * 100, color='grey', linestyle=':', label='Question 2 assumption')
    plt.xlabel('Drop in e-bike use (%)')
    plt.ylabel('Road deaths avoided per year')
    plt.title('Effect of a helmet requirement on e-bike deaths')
    plt.legend()
    plt.gca().yaxis.grid(True)
    plt.ylim(bottom=0)

    #     # plot 2: heatmap, deaths avoided as % of all road deaths
    # comps = np.linspace(0, 1, 11)
    # grid = np.array([[deaths_avoided(dr, c) / baseline_total_fatalities * 100 for dr in drops[::5]] for c in comps])
    # plt.figure()
    # plt.imshow(grid, origin='lower', aspect='auto', extent=[0, 50, 0, 100])
    # plt.colorbar(label='% of all road deaths avoided')
    # plt.xlabel('Drop in e-bike use (%)')
    # plt.ylabel('Helmet compliance (%)')
    # plt.title('Sensitivity analysis')
    plt.show()

