import numpy as np
import pandas as pd

from src import handle

def test_calc_heading():
    latlon1 = (39.099912, -94.581213)
    latlon2 = (38.627089, -90.200203)

    result = handle.calc_heading(latlon1, latlon2)

    assert result == 96.51


def test_get_all_headings():
    data = [{'lat':39.099912, 'lon':-94.581213}, {'lat':38.627089, 'lon':-90.200203}]

    test_df = pd.DataFrame(data)

    result = handle.get_all_headings(test_df)

    assert result == [96.51]
    