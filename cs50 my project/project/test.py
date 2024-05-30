import sqlite3
import pandas as pd
import json

from cs50 import SQL
from sollow import ss_capital_per_worker, ss_output_per_worker, get_sollowdf

# Connect to the SQLite database
db = SQL("sqlite:///growth.db")

# Fetch the necessary data from the database
data = db.execute('SELECT *, countrycode, country FROM pennworld JOIN countries ON country_id = id')

df = pd.DataFrame(data)

pwt = get_sollowdf(df)


# Define alpha (output elasticity of capital)
alpha = 1/3

# Initialize the sollow list
sollow = []

# Iterate over the rows in the dataframe

for index, row in pwt.iterrows():
    country = row['country']
    year = row['year']
    s = row['savings_rate']
    delta = row['capital_stock']
    n = row['pop_growth_rate']
    g = row['technological_progress']

    # Calculate k* and y*
    k_star = ss_capital_per_worker(s, delta, n, g, alpha)
    y_star = ss_output_per_worker(k_star, alpha)

    # Append the results to the sollow list
    sollow.append({
        'country': country,
        'year': year,
        'k_star': k_star,
        'y_star': y_star
    })


# Sort the list by y_star in ascending order
sollow = sorted(sollow, key=lambda x: x['y_star'])

# Save the sorted data to a JSON file
with open('sollow_data.json', 'w') as f:
    json.dump(sollow, f, indent=4)

