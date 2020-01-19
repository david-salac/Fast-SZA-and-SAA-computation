import numpy as np
import pandas


def solar_zenith_and_azimuth_angle(longitude: float,
                                   latitude: float,
                                   time_utc: pandas.DatetimeIndex) -> tuple:
    """Function for a computation of the solar zenith and azimuth angle.

    Solar Zenith Angle is calculated with precision 0.3 degree in average
        (maximal error is 1.5 degree), and the Solar Azimuth Angle is
        calculated with precision 0.5 degree (maximal error is 2 degree).
        From Five new algorithms for the computation of sun position
        from 2010 to 2110, Roberto Grena, 2012, online:
        https://doi.org/10.1016/j.solener.2012.01.024

    Args:
        longitude (float): Longitude of the place (sensitive up to 4 digits
            precision)
        latitude (float): Latitude of the place (sensitive up to 4 digits
            precision)
        time_utc (pandas.core.indexes.datetimes.DatetimeIndex):
            The time in the UTC time zone on given place
            (sensible up to seconds)
    Returns:
        tuple: (Zenith, Azimuth) angles in degrees
    """
    year = time_utc.year.values
    month = time_utc.month.values
    day = time_utc.day.values
    day_hours = (time_utc.hour.values + time_utc.minute.values / 60.0
                 + time_utc.second.values / 3600.0)

    # The computation of the time:
    year_val = np.floor(365.25 * (year - 2000.0))
    month_val = np.floor(30.6001 * (month + 1.0))
    year_val_pc = np.floor(0.01 * year)

    time_vec = (year_val + month_val - year_val_pc + day
                + 0.0416667 * day_hours - 21958.0)

    # Arguments of the method:
    lat_rad = np.deg2rad(latitude)
    lon_rad = np.deg2rad(longitude)
    # Reasonable estimates for pressure and temperature
    pressure = 1.0  # unit: atmosphere
    temperature = 20.0  # unit: degree of celsius

    # Computation
    d_t = 96.4 + 0.567 * (year - 2061.0)
    te = time_vec + 1.1574e-5 * d_t
    wte = 0.0172019715 * te

    lambda_decl = (-1.388803 + 1.720279216e-2 * te + 3.3366e-2
                   * np.sin(wte - 0.06172) + 3.53e-4
                   * np.sin(2.0 * wte - 0.1163))

    epsilon = 4.089567e-1 - 6.19e-9 * te

    sl = np.sin(lambda_decl)
    cl = np.cos(lambda_decl)
    se = np.sin(epsilon)

    ce = np.sqrt(1.0 - se * se)

    r_asc = np.arctan2(sl * ce, cl)

    r_asc[r_asc < 0] += 2 * np.pi

    h_ang = ((1.7528311 + 6.300388099 * time_vec + lon_rad - r_asc + np.pi)
             % (2 * np.pi)) - np.pi

    # Get rid of negative values:
    h_ang[h_ang < -np.pi] += 2 * np.pi

    sp = np.sin(lat_rad)
    cp = np.sqrt((1.0 - sp * sp))
    sd = sl * se
    cd = np.sqrt(1.0 - sd * sd)
    s_h = np.sin(h_ang)
    c_h = np.cos(h_ang)

    se0 = sp * sd + cp * cd * c_h

    ep = np.arcsin(se0) - 4.26e-5 * np.sqrt(1.0 - se0 * se0)

    d_e = (0.08422 * pressure) / ((273.0 + temperature)
                                 * np.tan(ep + 0.003138 / (ep + 0.08919)))

    # Compute SZA and SAA and return values in degrees:
    return (np.rad2deg((np.pi / 2) - ep - d_e),
            np.rad2deg(np.pi + np.arctan2(s_h, c_h * sp - sd * cp / cd)))
