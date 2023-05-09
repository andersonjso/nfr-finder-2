import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV file into pandas dataframe


def analysis_1():
    df = pd.read_csv('res.csv')

    # Group data by NFR type
    grouped = df.groupby(['nfr'])

    # Calculate mean, median, standard deviation, and range for each NFR type
    stats = grouped['changes_before', 'changes_after'].agg(['mean', 'median', 'std', 'max', 'min'])

    # Rename columns to make them more readable
    stats.columns = [' '.join(col).strip() for col in stats.columns.values]

    # Print the resulting statistical analysis
    print(stats.to_csv())

    # Plot the data using a boxplot
    sns.boxplot(x='nfr', y='changes_before', data=df)
    plt.show()

def analysis_2():
    import csv
    from collections import defaultdict
    import statistics

    # read csv file
    with open('changes.csv', 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # create defaultdict to store data by NFR
    nfr_data = defaultdict(list)

    # loop through data and group by NFR
    for row in data:
        nfr = row['nfr']
        changes_before = int(row['changes_before'])
        changes_after = int(row['changes_after'])
        nfr_data[nfr].append((changes_before, changes_after))

    # loop through nfr_data and calculate statistics
    for nfr, data in nfr_data.items():
        print(nfr)
        changes_before = [x[0] for x in data]
        changes_after = [x[1] for x in data]
        print(
            f'Changes Before - Mean: {statistics.mean(changes_before)}, Median: {statistics.median(changes_before)}, Stdev: {statistics.stdev(changes_before)}')
        print(
            f'Changes After - Mean: {statistics.mean(changes_after)}, Median: {statistics.median(changes_after)}, Stdev: {statistics.stdev(changes_after)}')
        print()

def analysis_3():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Read the csv file into a pandas dataframe
    df = pd.read_csv('changesv2.csv')

    # Group the data by NFR and calculate the mean and standard deviation of changes before and after
    nfr_grouped = df.groupby('nfr').agg({'changes_after': ['mean', 'std'], 'changes_after': ['mean', 'std']})

    # Print the statistics for each NFR
    print(nfr_grouped)

    # Create a bar plot showing the mean number of changes before and after for each NFR
    sns.set_style('whitegrid')
    nfr_grouped.plot(kind='bar', y=['changes_before', 'changes_after'], alpha=0.7, yerr='std', capsize=4)
    plt.title('Changes before and after by NFR')
    plt.xlabel('NFR')
    plt.ylabel('Number of changes')
    plt.show()


analysis_1()