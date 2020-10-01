from datetime import datetime
import os

import pandas as pd
import requests

LATLON = (39.740887,-105.000378)


class CsvWriter():
    def __init__(self):
        self.csv_file = f"./data/adsbx_{datetime.now().year}_{datetime.now().month}.csv"

    def write(self, new_data):
        try: 
            df = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            df = pd.DataFrame()
        
        df = df.append(new_data, ignore_index=True)
        df.drop_duplicates()

        df.to_csv(self.csv_file, index=False)


def handle(data_writer=CsvWriter()):
    result_df = get_aircraft()

    if not result_df.empty:
        data_writer.write(new_data=result_df)


def get_aircraft():
    api_key = os.environ["RAPID_API_ADSBX_KEY"]
    url =  f"https://adsbexchange-com1.p.rapidapi.com/json/lat/{LATLON[0]}/lon/{LATLON[1]}/dist/10/"
    headers = {
        'x-rapidapi-host': "adsbexchange-com1.p.rapidapi.com",
        'x-rapidapi-key': api_key
    }

    response = requests.get(url, headers=headers)
    results = response.json()

    print(f"Number Aircraft Found: {results['total']}")

    return pd.DataFrame(results['ac'])

if __name__ == "__main__":
    handle()