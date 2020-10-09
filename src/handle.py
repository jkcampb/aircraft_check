import math
import os

import pandas as pd
import requests

from src.db import CsvDB

LATLON = (39.740887, -105.000378)


def handle(db=CsvDB()):
    result_df = get_aircraft()

    aircraft_icaos = result_df["icao"].tolist()

    if not result_df.empty:
        db.write(new_data=result_df)

    for icao in aircraft_icaos:
        check_aircraft_circling(db, icao)


def get_aircraft():
    api_key = os.environ["ADSBX_API_KEY"]

    url = f"https://adsbexchange.com/api/aircraft/json/lat/{LATLON[0]}/lon/{LATLON[1]}/dist/10/"
    headers = {"api-auth": api_key, "accept-encoding": "gzip"}

    response = requests.get(url, headers=headers)
    results = response.json()

    print(f"Number Aircraft Found: {results['total']}")

    return pd.DataFrame(results["ac"])


def check_aircraft_circling(db, icao):
    df = db.read(icao, timespan_min=30)
    df.sort_values("posttime", axis=1, inplace=True)

    heading_delta = calc_heading(df)


def calc_heading(latlon1, latlon2):

    latlon1 = tuple(x * math.pi / 180 for x in latlon1)
    latlon2 = tuple(x * math.pi / 180 for x in latlon2)

    x = math.cos(latlon2[0]) * math.sin(latlon2[1] - latlon1[1])
    y = math.cos(latlon1[0]) * math.sin(latlon2[0]) \
         - math.sin(latlon1[0]) * math.cos(latlon2[0]) * math.cos(latlon2[1] - latlon1[1])

    beta = math.atan2(x,y)

    return beta * 180 / math.pi


if __name__ == "__main__":
    handle()