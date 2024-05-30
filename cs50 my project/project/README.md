# Web Application to Analize Economic Data with Sollow Model

## Video Demo:  <URL HERE>

## Description

This project involves creating a web app using Python, Jinja, SQL (sqlite3), and ChartJS for real-time data analysis on a SQL database. The database is constructed from raw data obtained from the [Penn World Table](https://www.rug.nl/ggdc/productivity/pwt/?lang=en). After processing the data, we apply the [Solow Model](https://en.wikipedia.org/wiki/Solow%E2%80%93Swan_model) to determine the output and capital in the steady state for 118 countries.

By analyzing the data and applying the Solow Growth Model, we offer valuable insights into the steady-state economies of various nations. This understanding is crucial for promoting sustainable economic growth and improving the quality of life globally.

Explore our detailed findings and interactive visualizations to learn more about the economic growth patterns and steady states of countries worldwide.

We use the pandas library in Python to analyze the raw data and create dataframes from the database.


## Features

- **Acess with login**:
  - To utilize this appliation, it's necessary to create a login and password on the initial page.
  - You can't choose a login that already exists in the database.


- **Dynamic Tables and Charts**:
  - Ranked dynamic table and charts for countries from 1955 to 2019.
  - Dynamic charts to compare raw and manipulated data for two selected countries.
  - Dynamic charts showing the evolution of output and capital in the steady state for a chosen country.

- **Technology Stack**:
  - **Python**: For data processing and backend logic.
  - **Jinja**: For templating HTML.
  - **SQL (sqlite3)**: For database management.
  - **ChartJS and Plotly**: For creating interactive charts.

## Methodology

1. **Data Collection**:
   - The raw data is sourced from the [Penn World Table](https://www.rug.nl/ggdc/productivity/pwt/?lang=en).

2. **Data Processing**:
   - Data is manipulated using the pandas library to create meaningful dataframes.
   - The Solow Model is applied to calculate the steady-state output and capital.

3. **Visualization**:
   - Interactive visualizations are created using ChartJS to display the analysis results.
   - Comparisons and rankings are dynamically generated for selected countries over the years.

## Backend Features
Our web application is written in python and we use pandas, plotly.graph_objects, cs50, flask, flask_session and werkzeug.security libraries to construct owr app.

We create some modules in.py extension to organize better our code.

- **app.py**: The app.py is the main program in our code and this file content many functions that are described bellow:

   1. **def after_request()**: ensure responses aren't cached.
   2. **def index()**: leaves to index page in HTML files.
   3. **def login()**: conect to a table in database, and verify with login and password are correct. If they are correct, connect session and redirect to the index page.
   4. **def logout()**: disconnet the session login that already exists
   5. **def register()**: register a new user and set the password.
   6. **def growth()**: display HTML file content "growth.html".
   7. **def pwt()**: conect to the database, create a pwt data to be rendered in HTML file.
   8. **def compare()**: get the data from database, to compare two countries in many variables types. Create figures if ploty to be rendered in a HTML file.
   9. **def sollow()**: display HTML file contents a definition of sollow model in "sollow.html" file
   10. **def change_data()**: get information of the database calculate output an capital in the steady state and create a dataframe with variables that will be used in the Sollow's model.
   11. **def analisys()**: fromw the database, create the data to be used in a dinamical graphic to analize the steady state of countries arround the world.
   12. **def analysis2()**: romw the database, create the data to be used in a dinamical graphic to analize the steady state of an selected country over the years.

- **helpers.py**: This program was taken from a lesson of CS50 Lessons, and it have two functions:
   1. **def apology()**: helps to render error messages in HTML using Python
   2. **def login_required()**: forces users in the home page to identify yourselfs before see contents marked with this function.

- **sollow.py**: This module was created to manipulate the raw data and calculcate the output and capital in the steady state from Sollow's model. It have three functions:

   1. **def ss_capital_per_worker()**: calculate the steady state capital to a country.
   2. **def ss_output_per_worker()**: calculate the steady state output to a country.
   3. **def get_sollowdf()**: get the database information and transforms in a dataframe that be used to analize the Sollow's Model.


## Frontend Features
The web pages use Jinja, JavaScript, and ChartJs to create HTML files, tables and dinamic graphics to be visualized for the users.

We choose a simplest visualization from the HTML to be more readable for the the users. We also inmplements Katex in HTML files to the formulas better visualized.


## Learning and Development

We utilized [OpenAI](https://chatgpt.com/) and CS50's duck debugger (ddb)to enhance our understanding of various tools, improve our code, and create content for this project. While AI tools facilites our work, our primary goal was to learn and develop new skills in web development and data analysis.

## How to Use

1. **Installation**:
   - Clone the repository.
   - Install the required Python packages using `pip install -r requirements.txt`.

2. **Running the App**:
   - Execute the main application file: `python app.py`.
   - Open your web browser and go to `http://localhost:5000` to access the app.

3. **Exploring Data**:
   - Use the provided interface to select countries and view their economic growth data.
   - Compare and analyze the data through the dynamic charts and tables.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

---

We hope this project provides valuable insights and fosters further learning and development in the field of economic data analysis.
