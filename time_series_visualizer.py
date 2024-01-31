import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np
import calendar


# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df = df.set_index('date')
df.index = pd.to_datetime(df.index)

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')

  
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    bar_groupby = df_bar.groupby(['year', 'month'])['value'].mean().rename_axis(['year', 'month'])
    bar_groupby = bar_groupby.reset_index()
    bar_pivot = pd.pivot_table(bar_groupby, values='value', index='year', columns='month')

    # Draw bar plot
    fig = bar_pivot.plot(kind='bar', legend=True, figsize=(15,6)).figure
    plt.legend(title="Months", labels= ['January','February','March','April','May','June','July','August','September','October','November','December'])
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(1,2)
    fig.set_size_inches(15,5)
    sns.boxplot(x=df_box['year'], y=df_box['value'], ax=axs[0], hue=df_box['year'], legend=False, palette='Set1')
    axs[0].set(xlabel='Year', ylabel='Page Views', title='Year-wise Box Plot (Trend)')
    sns.boxplot(x=df_box['month'], y=df_box['value'], ax=axs[1], order=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], hue=df_box['month'], legend=False, palette='Set1')
    axs[1].set(xlabel='Month', ylabel='Page Views', title='Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
