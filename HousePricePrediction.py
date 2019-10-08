'''This project aims to predict the price of a house given just the loacation and date of sale.
My algorithm is described in the accompanying slideshow, but finds the selling price of 100 properties in the csv
sold close to that date (to consider the market prices at that time) and the selling price of 100 properties in the csv
sold close to the area (using geohashes to consider the market prices in the surrounding area). I take a weighted average 
of these to calculate the predicted price of the house in question.
This code goes through 100 properties selected at random from the database and prints the actual selling price,
followed by the predicted price and the percentage difference between the actual and predicted prices.
Then at the end of the 100 random properties, I calculated the median percentage difference between my
predictions and the actual prices.'''
#By Dean Connell

import csv
from datetime import date
import geohash2
import sqlite3
from statistics import median, mean
from random import randint

Rows = []
trash = []
with open('HouseData.csv', encoding='MAC_ROMAN') as myfile:
    CSVreader = csv.reader(myfile, delimiter=',')
    for row in list(CSVreader)[1:]:
        try:
            temp = row[0].split(",")
            Lat = float(temp[0])
            Lon = float(temp[1])
            Geohash = geohash2.encode(Lat, Lon, precision=9)
            Rows.append([Lat, Lon] + row[1:] + [Geohash])
        except Exception as e:
            trash.append("")


for a in range(len(Rows)):
    Rows[a][2] = str(Rows[a][2])
    Rows[a][3] = str(Rows[a][3])
    Rows[a][4] = (Rows[a][4]).split("/")
    Rows[a][4] = date(int(Rows[a][4][2]), int(Rows[a][4][1]), int(Rows[a][4][0]))
    Rows[a][5] = float(Rows[a][5])
    Rows[a][6] = str(Rows[a][6])


def diem_number(date):
    upper_date_bound = 100
    counter_below = 0
    counter_above = 0
    date_prices = []
    for d in range(0, len(Rows)):
        if (abs(date-Rows[d][4])).days < 10 and counter_below < upper_date_bound/2:
            date_prices.append(Rows[d][5])
            counter_below += 1
    for f in reversed(range(0, len(Rows))):
        if (abs(date-Rows[f][4])).days < 10 and counter_above < upper_date_bound/2:
            date_prices.append(Rows[f][5])
            counter_above += 1
    return median(date_prices)


def locus_number(geohash):
    geohash_sub = len(geohash)
    upper_location_bound = 100
    counter = 0
    location_prices = []
    for g in reversed(range(geohash_sub)):
        for h in range(len(Rows)):
            if geohash[:g] == (Rows[h][6])[:g] and counter < upper_location_bound:
                location_prices.append(Rows[h][5])
                counter += 1
    return median(location_prices)


list_of_percentages = []
for x in range(100):
    rand = randint(0, len(Rows))
    temp1 = Rows[rand][5]
    print(Rows[rand][5])
    diem = diem_number(Rows[rand][4])
    locus = locus_number(Rows[rand][6])
    locus_diem_number = ((locus*29) + (diem*11))/40
    temp2 = locus_diem_number
    print(locus_diem_number)
    percentage = ((abs(temp1-temp2)/temp1)*100)
    print(percentage)
    list_of_percentages.append(percentage)
    print("")

print(median(list_of_percentages))