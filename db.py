from datetime import datetime
import pandas as pd


class CsvDB:
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

    def read(self):
        try:
            df = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            df = pd.DataFrame()

        return df 