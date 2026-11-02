# Importing packages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def helmet_usage_plot():
    
    data = {
        'Category': [
            'Light Moped (Roadside Count, Post-Mandate)',
            'Light Moped (Always wear, Post-Mandate)',
            'Light Moped (Always wear, Pre-Mandate)',
            'E-bike (No mandate)',
            'Fatbike (No mandate)',
            'E-bike (Voluntary use, 12-24 yrs)'
        ],
        'Helmet Usage Percentage': [99.0, 67.0, 9.0, 6.0, 3.0, 0.4],
        'Source': [
            'Schmidt et al., 2026',
            'Schmidt et al., 2026',
            'Schmidt et al., 2026',
            'VeiligheidNL, 2024',
            'VeiligheidNL, 2024',
            'TeamAlert, 2020'
        ]
    }
    
    df = pd.DataFrame(data)
    
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_context("paper", font_scale=1.2)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # barplot with horizontal bars and muted colors
    bars = sns.barplot(
        x='Helmet Usage Percentage', 
        y='Category',
        hue='Category',
        legend=False, 
        data=df, 
        palette='crest', 
        ax=ax,
        edgecolor='black',
        linewidth=0.8
    )
    
    # Format axes and labels
    ax.set_xlabel('Helmet Usage (%)', fontweight='bold', labelpad=10)
    ax.set_ylabel('', fontweight='bold')
    ax.set_title('Helmet Usage Patterns in the Netherlands Across Different Bicycle Types', 
                 fontweight='bold', pad=15, fontsize=14)
    
    # Set x-axis limit to slightly above 100 so that the text labels fit nicely
    ax.set_xlim(0, 105)
    
    # Assigning the data to the bar and label
    for i, p in enumerate(bars.patches):
        width = p.get_width()
        source_text = df['Source'].iloc[i]
        
        # Display the percentage and the citation source next to the bar
        ax.text(
            width + 1.5,                 # X-coordinate (slightly right of the bar)
            p.get_y() + p.get_height()/2,# Y-coordinate (centered on the bar)
            f'{width:.1f}% ({source_text})', # Text label
            ha='left', 
            va='center', 
            fontsize=10,
            color='black'
        )
    # Clean up grid lines (keep x-grid, remove y-grid for clean look)
    ax.xaxis.grid(True, linestyle='--', alpha=0.7)
    ax.yaxis.grid(False)
     
    # Despine top and right borders
    sns.despine(left=True, bottom=False)
    
    # Adjust layout and display
    plt.tight_layout()
    plt.savefig("Helmet_Usage.png", bbox_inches="tight")
    plt.show()

helmet_usage_plot()

def attitudes_usage_plot():
    
    data = {
        'Category': [
            'Perception: Others wear helmets (Post-Mandate)',
            'Attitude: Helmet use is a habit (Post-Mandate)',
            'Fear remarks about wearing a helmet (12-24 yrs)',
            "Others' opinions matter on helmet use (12-24 yrs)",
            'Stopped riding after light moped mandate',
            'Attitude: Helmet use is a habit (Pre-Mandate)',
            'Perception: Others wear helmets (Pre-Mandate)'
        ],
        'Percentage': [63.6, 50.9, 48.3, 46.9, 20.0, 19.7, 18.2],
        'Source': [
            'Schmidt et al., 2026',
            'Schmidt et al., 2026',
            'TeamAlert, 2020',
            'TeamAlert, 2020',
            'Schmidt et al., 2026',
            'Schmidt et al., 2026',
            'Schmidt et al., 2026'
        ]
    }
    
    df = pd.DataFrame(data)
    
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_context("paper", font_scale=1.2)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # barplot with horizontal bars and muted colors
    bars = sns.barplot(
        x='Percentage', 
        y='Category',
        hue='Category',
        legend=False, 
        data=df, 
        palette='crest', 
        ax=ax,
        edgecolor='black',
        linewidth=0.8
    )
    
    # Format axes and labels
    ax.set_xlabel('Percentage (%)', fontweight='bold', labelpad=10)
    ax.set_ylabel('', fontweight='bold')
    ax.set_title('Attitudes and Behaviors of Underage Riders', 
                 fontweight='bold', pad=15, fontsize=14)
    
    # Set x-axis limit to slightly above 100 so that the text labels fit nicely
    ax.set_xlim(0, 105)
    
    # Assigning the data to the bar and label
    for i, p in enumerate(bars.patches):
        width = p.get_width()
        source_text = df['Source'].iloc[i]
        
        # Display the percentage and the citation source next to the bar
        ax.text(
            width + 1.5,                 # X-coordinate (slightly right of the bar)
            p.get_y() + p.get_height()/2,# Y-coordinate (centered on the bar)
            f'{width:.1f}% ({source_text})', # Text label
            ha='left', 
            va='center', 
            fontsize=10,
            color='black'
        )
    # Clean up grid lines (keep x-grid, remove y-grid for clean look)
    ax.xaxis.grid(True, linestyle='--', alpha=0.7)
    ax.yaxis.grid(False)
     
    # Despine top and right borders
    sns.despine(left=True, bottom=False)
    
    # Adjust layout and display
    plt.tight_layout()
    plt.savefig("Attitudes_Usage", bbox_inches="tight")
    plt.show()

attitudes_usage_plot()

def trip_replacement_plot():
    
    data = {
        'Category': [
            'Cars (over 50%)',
            'E-bikes',
            'Regular bicycles',
            'Walking',
            'Fatbikes and speed pedelecs (fewer than 5%)'
        ],
        'Percentage': [50.0, 33.0, 20.0, 20.0, 5.0],
        'Source': [
            'Schmidt et al., 2026',
            'Schmidt et al., 2026',
            'Schmidt et al., 2026',
            'Schmidt et al., 2026',
            'Schmidt et al., 2026'
        ]
    }
    
    df = pd.DataFrame(data)
    
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_context("paper", font_scale=1.2)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # barplot with horizontal bars and muted colors
    bars = sns.barplot(
        x='Percentage', 
        y='Category',
        hue='Category',
        legend=False, 
        data=df, 
        palette='crest', 
        ax=ax,
        edgecolor='black',
        linewidth=0.8
    )
    
    # Format axes and labels
    ax.set_xlabel('Percentage (%)', fontweight='bold', labelpad=10)
    ax.set_ylabel('', fontweight='bold')
    ax.set_title('Where Replaced Light Moped Trips Go', 
                 fontweight='bold', pad=15, fontsize=14)
    
    # Set x-axis limit to slightly above 100 so that the text labels fit nicely
    ax.set_xlim(0, 65)
    
    # Assigning the data to the bar and label
    for i, p in enumerate(bars.patches):
        width = p.get_width()
        source_text = df['Source'].iloc[i]
        
        # Display the percentage and the citation source next to the bar
        ax.text(
            width + 1.0,                 # X-coordinate (slightly right of the bar)
            p.get_y() + p.get_height()/2,# Y-coordinate (centered on the bar)
            f'{width:.1f}% ({source_text})', # Text label
            ha='left', 
            va='center', 
            fontsize=10,
            color='black'
        )
    # Clean up grid lines (keep x-grid, remove y-grid for clean look)
    ax.xaxis.grid(True, linestyle='--', alpha=0.7)
    ax.yaxis.grid(False)
     
    # Despine top and right borders
    sns.despine(left=True, bottom=False)
    
    # Adjust layout and display
    plt.tight_layout()
    plt.savefig("Trip_Replacement.png", bbox_inches="tight")
    plt.show()

trip_replacement_plot()

def effects_plot():
    
    data = {
        'Category': [
            'Fatal head trauma reduction',
            'Serious head injury reduction',
            'Pre-mandate severe head injury share',
            'Post-mandate severe head injury share',
            'E-bike brain injury casualties',
            'Fatbike brain injury casualties',
            'Reduction in severe injuries',
            'Reduction in rider deaths',
            'Reduction in light moped crashes'
        ],
        'Percentage': [70.0, 60.0, 55.0, 30.0, 22.0, 17.0, 50.0, 38.0, 38.0],
        'Effect Type': [
            'Direct Effect', 'Direct Effect', 'Direct Effect', 'Direct Effect', 
            'Direct Effect', 'Direct Effect', 'Exposure Effect', 'Exposure Effect', 'Exposure Effect'
        ],
        'Source': [
            'TeamAlert, 2020',
            'TeamAlert, 2020',
            'Schmidt et al., 2026',
            'Schmidt et al., 2026',
            'VeiligheidNL, 2024',
            'VeiligheidNL, 2024',
            'Schmidt et al., 2026',
            'Schmidt et al., 2026',
            'Schmidt et al., 2026'
        ]
    }
    
    df = pd.DataFrame(data)
    
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_context("paper", font_scale=1.2)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # barplot with horizontal bars
    bars = sns.barplot(
        x='Percentage', 
        y='Category',
        hue='Effect Type',
        dodge=False,
        data=df, 
        palette='crest', 
        ax=ax,
        edgecolor='black',
        linewidth=0.8
    )
    
    # Format axes and labels
    ax.set_xlabel('Percentage (%)', fontweight='bold', labelpad=10)
    ax.set_ylabel('', fontweight='bold')
    ax.set_title('Direct and Exposure Effects on Fatal and Serious Incidents', 
                 fontweight='bold', pad=15, fontsize=14)
    
    # Set x-axis limit for better visibility of text labels
    ax.set_xlim(0, 90)
    
    # Move the legend outside the plot
    plt.legend(title='Effect Type', loc='lower right')
    
    # Assigning the data to the bar and label
    for i, p in enumerate(ax.patches):
        # Seaborn creates patches for all hue categories
        if p.get_width() == 0:
            continue
            
        width = p.get_width()
        
        # round the width to one decimal place
        matched_row = df[df['Percentage'].round(1) == round(width, 1)].iloc[0]
        source_text = matched_row['Source']
        
        # Display the percentage and the citation source next to the bar
        ax.text(
            width + 1.0,                 # X-coordinate (slightly right of the bar)
            p.get_y() + p.get_height()/2,# Y-coordinate (centered on the bar)
            f'{width:.0f}% ({source_text})', # Text label
            ha='left', 
            va='center', 
            fontsize=10,
            color='black'
        )
        
    # Clean up grid lines
    ax.xaxis.grid(True, linestyle='--', alpha=0.7)
    ax.yaxis.grid(False)
     
    # Despine top and right borders
    sns.despine(left=True, bottom=False)
    
    # Adjust layout and display
    plt.tight_layout()
    plt.savefig("Effects.png", bbox_inches="tight")
    plt.show()

effects_plot()

def helmet_adoption_prediction():
    # Set seaborn theme
    sns.set_theme(style="whitegrid")

    # Timeline up to 12 months
    months = np.arange(0, 13)

    # Parameters from qualitative resarch
    start_usage = 0.4  # Current voluntary helmet use 
    best_case_max = 67.0 # Structural helmet use post-light moped mandate
    resistance_factor = 0.48 # Based on youth fearing remarks (48.3%)

    # Calculate final percentage ceilings per scenario
    expected_case_max = best_case_max * (1 - resistance_factor)
    worst_case_max = 15.0 # Assumption based avoidance behavior

    # Adoption rate constant (speed of adaptation to the mandate)
    k = 0.4 

    # Modelling adoption curves (asymptotic growth: y = max - (max - start) * e^(-k*x))
    best_case = best_case_max - (best_case_max - start_usage) * np.exp(-k * months)
    expected_case = expected_case_max - (expected_case_max - start_usage) * np.exp(-k * months)
    worst_case = worst_case_max - (worst_case_max - start_usage) * np.exp(-k * months)

    # Data into Pandas DataFrame
    df_prediction = pd.DataFrame({
        'Month': months,
        'Best Case (%)': np.round(best_case, 1),
        'Expected Case (%)': np.round(expected_case, 1),
        'Worst Case (%)': np.round(worst_case, 1)
    })

    # Visualisation 
    plt.figure(figsize=(10, 6))

    sns.lineplot(
        x='Month',
        y='Best Case (%)',
        data=df_prediction,
        color='green',
        label='Best Case (Light moped benchmark)',
        linewidth=2
    )
    sns.lineplot(x='Month', y='Expected Case (%)', data=df_prediction, color='blue', label='Expected Case (Social resistance penalty)', linewidth=2.5)
    sns.lineplot(x='Month', y='Worst Case (%)', data=df_prediction, color='red', label='Worst Case (Avoidance behavior)', linewidth=2)

    plt.fill_between(months, worst_case, best_case, color='blue', alpha=0.1, label='Prediction Margin')

    plt.title('Projected Helmet Adoption Curve for 12-17 Year Olds (E-bike/Fatbike)', fontsize=14, fontweight='bold')
    plt.xlabel('Months after mandate implementation', fontsize=12)
    plt.ylabel('Structural helmet compliance (%)', fontsize=12)
    plt.xlim(0, 12)
    plt.ylim(0, 100)
    plt.xticks(months)
    plt.legend(loc='upper left')

    plt.tight_layout()
    plt.savefig("Helmet_Adaption_Prediction.png", bbox_inches="tight")
    plt.show()
helmet_adoption_prediction()