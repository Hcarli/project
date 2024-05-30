import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.offline import plot
from cs50 import SQL


db = SQL("sqlite:///growth.db")

pwt_data = db.execute('SELECT *, countrycode, country FROM pennworld JOIN countries ON country_id = id')

pwt_data = pd.DataFrame(pwt_data)

# Select relevant columns
relevant_columns = ['country', 'year', 'rgdpe', 'csh_i', 'popul', 'rtfpna', 'cn']
pwt_selected = pwt_data[relevant_columns]

# Calculate GDP growth rate
pwt_selected['gdp_growth_rate'] = pwt_selected.groupby('country')['rgdpe'].pct_change() * 100

# Rename 'csh_i' to 'savings_rate'
pwt_selected.rename(columns={'csh_i': 'savings_rate'}, inplace=True)

# Calculate population growth rate
pwt_selected['pop_growth_rate'] = pwt_selected.groupby('country')['popul'].pct_change() * 100

# Rename 'rtfpna' to 'technological_progress'
pwt_selected.rename(columns={'rtfpna': 'technological_progress'}, inplace=True)

# Rename 'cn' to 'capital_stock'
pwt_selected.rename(columns={'cn': 'capital_stock'}, inplace=True)

# Drop rows with missing values (if necessary)
pwt_selected = pwt_selected.dropna()

# Display the first few rows of the processed data
print(pwt_selected.head())

# Save the processed data to a new CSV file
pwt_selected.to_csv('pwt_processed.csv', index=False)

pwt = pwt_selected

pwt_country1 = pwt[pwt['country']=="Brazil"]
pwt_country2 = pwt[pwt['country']=="Canada"]


fig1 = go.Figure(go.Scatter(x=pwt_country1['year'], y=pwt_country1['gdp_growth_rate'], mode='lines', name="Brazil"))
fig1.add_trace(go.Scatter(x=pwt_country2['year'], y=pwt_country2['gdp_growth_rate'], mode='lines', name="Canada"))

fig1.update_layout(title_text="GDP growth rate", title_x=0.5)
fig1.add_annotation(
    text="Brazil" + " x " + "Canada",
    font=(dict(size=16)),
    xref="paper", yref="paper",
    x=0.5, y=-0.2,
    showarrow=False
)

fig1_html = plot(fig1, output_type='div')

pio.write_html(fig1,'gdp_growth.html')
