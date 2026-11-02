# Dikkebandjes_Group4

Date: 6 November 2026

Course: TIL6022 – TIL Python Programming

Repository Link: https://github.com/fleurubbink/Dikkebandjes_Group4

TU Delft



## Overview

This project aims to predict the effects of the implementation of the obligatory helmet requirement on e-bikes for people under the age of 18 the following 5 years. This is based on existing data on e-bike usage, traffic accidents and traffic deaths. As well as existing data on the effects of the obligatory helmet requirement on mopeds afters 2023.



## Repository Content

data: Contains all datasets we created and filtered from sources.

sources: Contains all unfiltered data and sources we found and used.

code: Contains all the python code we wrote for the visualization of our data.

graphs: Contains all the visualizations created with our code.

main report: Contains the main report notebook file and html file.

README: File with instructions.



## Data Sources

All datasets are publicly available or manually retreived from reliable sources. They are stored in the /data/ directory to ensure reproducibility.


Source Information:
> Aandeel-fietsers-2021-2025.csv \

Percentages in bike use and e-bike use (indirectly used)

> Aantal_nieuwverkochte_voertuigen_met_bromfietskenteken.csv \

Number of sold mopeds 2021 - 2023 (directly used)

> Aantal_voertuigen_met_bromfietskenteken_2023.csv \

Number of different mopeds used per age group 2020 - 2023 (directly used)

> Brom- en snorfietsen, naar leeftijd eigenaar, 1 januari (x 1 000).csv \

Number of mopeds per age category 2019 - 2025 (directly used)

> Verkeersdoden_vanaf_1950.csv \

Number of traffic deaths per age group and traffic mode 1950 - 2025 (directly used)

> Voertuigen met een bromfietskenteken, 1 januari (x 1 000).csv \

Number of mopeds used 2019 - 2025 (directly used)

> sources_for_Aantal_SEHbezoeken \

All sources that were used to create the dataset 'Aantal_SEHbezoeken'. All datasets show numbers on severe traffic-related accidents. We used the bike-related ER-visits among the youth. (indirectly used)

> Ongevallen_regio.ods \

By the police registered traffic accidents in the Netherlands per region and severity (indirectly used)


Directory structure /data/: This contains the following datasets:

> (Elektrisch)_fietsen_onder_jongeren.csv \

The filtered dataset from the source 'Aandeel-fietsers-2021-2025.csv'

> Aantal_SEHbezoeken.csv \

The created dataset to show numbers on the bike-related ER-visits among the youth in 2020 - 2024

> ongevallen_regio_BRON.csv \

The filtered dataset from the source 'Ongevallen_regio.ods'


## Reproduction Guide

### Requirements

To reproduce the analysis, the following are required:


Installed Python packages:
- pandas
- plotly.express
- plotly.io
- pathlib
- numpy
- matplotlib.pyplot
- mathplotlib.ticker


### General Setup

To regenerate the all the graphs:
- Install all the required packages
- Clone our GitHub repository in VS Code
- Run the python files


### Execution Order of Code

The code files can be run in any order. However, the logical order, following the structure of the report, is:
- question0_trendbiking.py
- question1_electric.py
- question1_nonelectric.py
- Question2_Mandatory_Helmet_Teens_prediction.py
- Ron_Helmet_Adaption_Prediction.py
- decrease_ER_question3.py
- decrease_in_deaths_question3.py
- vraag4_fatal_bicycle_moped_accidents.py

Following this procedure ensures full reproducibility: all graphs and analyses can be regenerated using the provided code and data files.
