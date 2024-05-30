import pandas as pd

alpha = 1/3


# Steady-state capital per worker
def ss_capital_per_worker(s, delta, n, g, alpha):

    capital = ((s / (delta + n + g)) ** (1 / (1 - alpha)))

  #  if isinstance(capital, complex):

   #     capital = 0

    #    return capital

    return capital

# Steady-state output per worker
def ss_output_per_worker(k, alpha):

    output = (k ** alpha)

  #  if isinstance(output, complex):

 #       output = 0

  #      return output

    return output


def get_sollowdf(sollow):

    # Select relevant columns
    relevant_columns = ['country', 'ck', 'rgdpe','year', 'popul', 'csh_i', 'delta', 'rtfpna']
    sollow = sollow[relevant_columns]

    # Calculate population growth rate
    sollow['gdp_growth_rate'] = sollow.groupby('country')['rgdpe'].pct_change() * 100

     # Rename 'csh_i' to 'savings_rate'
    sollow.rename(columns={'csh_i': 'savings_rate'}, inplace=True)

    # Rename 'ck' to 'capital_stock'
    sollow.rename(columns={'ck': 'capital_stock'}, inplace=True)


    # Calculate population growth rate
    sollow['pop_growth_rate'] = sollow.groupby('country')['popul'].pct_change()

    # Rename 'rtfpna' to 'technological_progress'
    sollow.rename(columns={'rtfpna': 'technological_progress'}, inplace=True)

    # Rename 'delta' to 'depreciation_rate'
    sollow.rename(columns={'delta': 'depreciation_rate'}, inplace=True)

    # Drop rows with missing values (if necessary)
    sollow = sollow.dropna()

    return(sollow)
