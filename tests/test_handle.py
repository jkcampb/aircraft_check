from src import handle

def test_calc_heading():
    latlon1 = (39.099912, -94.581213)
    latlon2 = (38.627089, -90.200203)

    result = handle.calc_heading(latlon1, latlon2)

    assert abs(result - 96.51) < 0.01