import math
import os

import numpy as np
import pandas as pd
import requests

from db import CsvDB

LATLON = (39.740887, -105.000378)


def handle(db=CsvDB()):
    result_df = get_aircraft()

    if not result_df.empty:
        db.write(new_data=result_df)

    if len(result_df) > 0:
        aircraft_icaos = result_df["icao"].tolist()

        for icao in aircraft_icaos:
            df = db.read(icao, timespan_min=30)

            print(f"Pulling data for {icao}")
            check_aircraft_circling(df)


def get_aircraft():
    api_key = os.environ["ADSBX_API_KEY"]

    url = f"https://adsbexchange.com/api/aircraft/json/lat/{LATLON[0]}/lon/{LATLON[1]}/dist/10/"
    headers = {"api-auth": api_key, "accept-encoding": "gzip"}

    response = requests.get(url, headers=headers)
    results = response.json()

    print(f"Number Aircraft Found: {results['total']}")

    return pd.DataFrame(results["ac"])


def check_aircraft_circling(df, circling_threshold=1080):
    headings = get_all_headings(df)

    total_diff = total_heading_change(headings)

    print(f"Heading change: {total_diff}")

    return total_diff >= circling_threshold


def total_heading_change(headings):

    return sum(np.diff(headings))


def get_all_headings(df):
    df["next_lat"] = df["lat"].shift(-1, axis=0)
    df["next_lon"] = df["lon"].shift(-1, axis=0)

    headings = list(
        df.apply(
            lambda x: calc_heading(
                (x["lat"], x["lon"]), (x["next_lat"], x["next_lon"])
            ),
            axis=1,
        )
    )

    print(headings)

    return headings[:-1]


def calc_heading(latlon1, latlon2):

    latlon1 = tuple(x * math.pi / 180 for x in latlon1)
    latlon2 = tuple(x * math.pi / 180 for x in latlon2)

    x = math.cos(latlon2[0]) * math.sin(latlon2[1] - latlon1[1])
    y = math.cos(latlon1[0]) * math.sin(latlon2[0]) - math.sin(latlon1[0]) * math.cos(
        latlon2[0]
    ) * math.cos(latlon2[1] - latlon1[1])

    beta = math.atan2(x, y)

    return round(beta * 180 / math.pi, 2)


if __name__ == "__main__":
    handle()