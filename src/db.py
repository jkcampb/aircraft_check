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

    def read(self, icao, timespan_min):
        # Pull only a icao for the most recent timestamp_min minutes
        # TODO: write test
        try:
            df = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            print("New file, returning empty DF")
            df = pd.DataFrame()
            return df

        df_filter = (df["icao"] == icao) & \
            (df["postime"] >= (datetime.now().timestamp() - timespan_min * 60) * 1000)

        result = df[df_filter].sort_values("postime")

        return result
