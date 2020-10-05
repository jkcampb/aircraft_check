import os

import pandas as pd
import requests

from db import CsvDB

LATLON = (39.740887, -105.000378)


def handle(data_writer=CsvDB()):
    result_df = get_aircraft()

    if not result_df.empty:
        data_writer.write(new_data=result_df)


def get_aircraft():
    api_key = os.environ["ADSBX_API_KEY"]

    url = f"https://adsbexchange.com/api/aircraft/json/lat/{LATLON[0]}/lon/{LATLON[1]}/dist/10/"
    headers = {"api-auth": api_key, "accept-encoding": "gzip"}

    response = requests.get(url, headers=headers)
    results = response.json()

    print(f"Number Aircraft Found: {results['total']}")

    return pd.DataFrame(results["ac"])


if __name__ == "__main__":
    handle()