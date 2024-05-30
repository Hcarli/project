import pandas as pd

alpha = 1/3


# Steady-state capital per worker
def ss_capital_per_worker(s, delta, n, g, alpha):
    return (s / (delta + n + g)) ** (1 / (1 - alpha))

# Steady-state output per worker
def ss_output_per_worker(k, alpha):
    return k ** alpha


def get_sollowdf(sollow):

    # Select relevant columns
    relevant_columns = ['country', 'year', 'rgdpe', 'csh_i', 'popul', 'rtfpna', 'cn']
    sollow = sollow[relevant_columns]

    # Calculate GDP growth rate
    sollow['gdp_growth_rate'] = sollow.groupby('country')['rgdpe'].pct_change() * 100

    # Rename 'csh_i' to 'savings_rate'
    sollow.rename(columns={'csh_i': 'savings_rate'}, inplace=True)

    # Calculate population growth rate
    sollow['pop_growth_rate'] = sollow.groupby('country')['popul'].pct_change() * 100

    # Rename 'rtfpna' to 'technological_progress'
    sollow.rename(columns={'rtfpna': 'technological_progress'}, inplace=True)

    # Rename 'cn' to 'capital_stock'
    sollow.rename(columns={'cn': 'capital_stock'}, inplace=True)

    # Drop rows with missing values (if necessary)
    sollow = sollow.dropna()

    return(sollow)
