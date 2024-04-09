import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

csv_url = "fcc-forum-pageviews.csv"

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv(csv_url, index_col='date', parse_dates=True)

# Clean data
df = df.loc[
         (df['value'] >= df['value'].quantile(0.025)) &
         (df['value'] <= df['value'].quantile(0.975)) 
     ]

def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(12, 5))
    plt.plot(df.index, df['value'], c='firebrick')
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel(str(df.index.name).capitalize())
    plt.ylabel("Page Views")
    plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar = df_bar.resample(rule = 'M').mean()

    # Draw bar plot
    years = pd.to_datetime(df.index).year.unique().sort_values()
    monthly_average_page_views = {
        'January': [],
        'February': [],
        'March': [],
        'April': [],
        'May': [],
        'June': [],
        'July': [],
        'August': [],
        'September': [],
        'October': [],
        'November': [],
        'December': []
    }
    for year in years:
        for index, month in enumerate(monthly_average_page_views):
            if(df_bar.loc[(df_bar.index.year == year) 
                    & (df_bar.index.month == index + 1)].empty):
                monthly_average_page_views[month].append(0)
            else:
                monthly_average_page_views[month].append(
                    df_bar.loc[(df_bar.index.year == year) & (df_bar.index.month == index + 1)]
                    .iloc[-1]
                    .value
                )

    x = list(range(years.size))
    width = 0.03
    multiplier = 0

    fig, ax = plt.subplots(figsize=(8,6))

    for month, value in monthly_average_page_views.items():
        offset = width * multiplier
        ax.bar([i + offset for i in x], value, width, label=month)
        multiplier += 1

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_xticks([i + 0.15 for i in x], years)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.legend(loc='upper left', title='Months')

    plt.show()

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
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.boxplot(
        x=df_box['year'], 
        y=df_box['value'], 
        ax=axes[0],
        hue=df_box['year'], 
        legend=False,
        fliersize=3, 
        flierprops={'marker': 'd', 'markerfacecolor':'k'},
        palette=sns.color_palette(n_colors=4)
    ).set(xlabel='Year', ylabel='Page Views')

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    s = df_box['month'].astype('category')
    s = s.cat.set_categories(months, ordered=True).sort_values()
    sns.boxplot(
        x=s, 
        y=df_box['value'],
        ax=axes[1],
        hue=s, 
        legend=False, 
        fliersize=3, 
        flierprops={'marker': 'd', 'markerfacecolor':'k'}
    ).set(xlabel='Month', ylabel='Page Views')
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    for i in range(2):
        axes[i].set_ylim([0, 200000])
        axes[i].set_yticks(list(range(0,220000,20000)))
    
    plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
