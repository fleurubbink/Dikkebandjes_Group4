# Dikkebandjes_Group4

Date: 6 November 2026

Course: TIL6022 – TIL Python Programming

Repository Link: https://github.com/fleurubbink/Dikkebandjes_Group4

TU Delft

1. Overview


2. Repository Content
data: Contains all datasets we created and filtered from sources.
sources: Contains all unfiltered data and sources we found and used.
code: Contains all the python code we wrote for the visualization of our data.
graphs: Contains all the visualizations created with our code.
main report: Contains the main report notebook file and html file.
README: File with instructions.

3. Data Sources
All datasets are publicly available or manually retreived from reliable sources. They are stored in the /data/ directory to ensure reproducibility.

Source Information:
  Aandeel-fietsers-2021-2025.csv
Percentages in bike use and e-bike use (indirectly used)
  Aantal_nieuwverkochte_voertuigen_met_bromfietskenteken.csv

  Aantal_voertuigen_met_bromfietskenteken_2023.csv

  Brom- en snorfietsen, naar leeftijd eigenaar, 1 januari (x 1 000).csv

  Verkeersdoden_vanaf_1950.csv

  Voertuigen met een bromfietskenteken, 1 januari (x 1 000).csv

  sources_for_Aantal_SEHbezoeken
All sources that were used to create the dataset 'Aantal_SEHbezoeken'. All datasets show numbers on severe traffic-related accidents. We used the bike-related ER-visits among the youth. (indirectly used)
  Ongevallen_regio.ods


Directory structure /data/: This contains the following datasets:
  (Elektrisch)_fietsen_onder_jongeren.csv
The filtered dataset from the source 'Aandeel-fietsers-2021-2025.csv'
  Aantal_SEHbezoeken.csv
The created dataset to show numbers on the bike-related ER-visits among the youth in 2020 - 2024
  ongevallen_regio_BRON.csv
The filtered dataset from the source 'Ongevallen_regio.ods'

4. Reproduction Guide
4.1 Requirements
To reproduce the analysis, the following are required:

Installed Python packages:
pandas
plotly.express
plotly.io
pathlib
numpy
tkinter
matplotlib.pyplot
mathplotlib.ticker

4.2 General Setup
To regenerate the all the graphs:
- Install all the required packages
- Download all of the required datasets and put them into accessible folders
- Download the python files
- Run the python files

Key parameters:

??

4.3 Execution Order of Code

The code files can be run in any order. However, the logical order, following the structure of the report, is:


Following this procedure ensures full reproducibility: all graphs and analyses can be regenerated using the provided code and data files.
