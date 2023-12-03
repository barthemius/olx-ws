# Module with loading and preprocessing of the data to be visualised
#

import enum
import pandas as pd
import numpy as np
import os
from datetime import datetime


# Data set class with fields - time and dataframe
class DataSet:
    def __init__(self, time, data):
        self.time = time
        self.data = data.copy()

    def __str__(self):
        return "DataSet: time = {}".format(self.time)

    def price(self):
        return self.data.loc[:, "price"]

    def ppm2(self):
        return self.data.loc[:, "price_per_m2"]

    def rooms(self):
        return self.data.loc[:, "rooms"]

    def days_passed(self):
        dt = pd.DataFrame()
        dt["days_passed"] = (
            self.data["date_lastmod"].apply(datetime.fromisoformat)
            - self.data["date_created"].apply(datetime.fromisoformat)
        ).apply(lambda x: x.days)

        return dt


# Get csv filenames from the present directory
def get_filenames():
    filenames = []
    for filename in os.listdir(os.getcwd() + "/data"):
        if filename.endswith(".csv"):
            filenames.append(filename)
    return filenames


# Load data from csv files
def load_data(filenames):
    # Separate loading for olx and otodom data
    olx_data = []
    olx_time = []
    otodom_data = []
    otodom_time = []

    # Load data from both sources and extract date from filenames

    for filename in filenames:
        d = filename.split("_")[2]
        m = filename.split("_")[3]
        y = filename.split("_")[4][:-4]

        if "olx" in filename:
            olx_data.append(pd.read_csv("data/" + filename, index_col=0))
            olx_time.append(datetime.strptime(d + " " + m + " " + y, "%d %B %Y"))

        elif "otodom" in filename:
            otodom_data.append(pd.read_csv("data/" + filename, index_col=0))
            otodom_time.append(datetime.strptime(d + " " + m + " " + y, "%d %B %Y"))

    # Clean data
    # OLX First
    olx_clean = []
    for i, data in enumerate(olx_data):
        bloki1 = data[data["builttype"] == "blok"]
        bloki1.rename(
            columns={
                "price_per_m": "price_per_m2",
                "lastRefresh": "date_lastmod",
                "createdTime": "date_created",
            },
            inplace=True,
        )
        bloki1.drop(
            columns=[
                "id",
                "builttype",
                "location",
                "floor_select",
                "furniture",
                "market",
            ],
            inplace=True,
        )
        bloki1["rooms"] = bloki1["rooms"].map(
            {
                "one": 1,
                "two": 2,
                "three": 3,
                "four": 4,
                "five": 5,
                "six": 6,
                "seven": 7,
                "eight": 8,
                "nine": 9,
                "ten": 10,
            }
        )

        olx_clean.append(DataSet(olx_time[i], bloki1))

    # OTODOM Second
    otodom_clean = []
    for i, data in enumerate(otodom_data):
        bloki2 = data.dropna()
        bloki2 = bloki2[bloki2["builttype"] == "block"]
        bloki2 = bloki2[bloki2["build_year"] > 1900]
        bloki2 = bloki2.drop(columns=["builttype", "location", "floor", "market", "id"])

        otodom_clean.append(DataSet(otodom_time[i], bloki2))

    # Return data and time
    return olx_clean, otodom_clean
