import os
import csv

from cs50 import SQL

db = SQL("sqlite:///growth.db")

with open('countries.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        db.execute("INSERT INTO countries (countrycode, country, year, rgdpo, emp, hc, ck) VALUES (?, ? , ?, ?, ?, ?, ?)", row['countrycode'], row['country'], row['year'], row['rgdpo'], row['emp'], row['hc'], row['ck'])


