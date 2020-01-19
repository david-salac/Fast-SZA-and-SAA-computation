import unittest
import pvlib
import pandas as pd
import numpy as np

from sza_saa_grena import solar_zenith_and_azimuth_angle


class TestSZASAA(unittest.TestCase):
    """Test the algorithm using PVLIB implementation of the SZA and SAA
        computation."""

    def test_sza_saa(self):
        time_array = pd.date_range("2020/1/1", periods=87_600, freq="10T",
                                   tz="UTC")
        lat, lon = 51.48728, -0.12435
        # Value computed using Grena's algorithm:
        sza_c, saa_c = solar_zenith_and_azimuth_angle(lon, lat, time_array)
        # Value computed using PVLIB:
        sza_saa_pvlib = \
            pvlib.location.solarposition.get_solarposition(time_array,
                                                           lat,
                                                           lon)

        sza_e, saa_e = sza_saa_pvlib['zenith'], sza_saa_pvlib['azimuth']

        # Test the average error:
        self.assertTrue(np.mean(np.abs(sza_c - sza_e)) < 0.2)
        self.assertTrue(np.mean(np.abs(saa_c - saa_e)) < 0.2)

        # Test the maximal error
        sza_max = np.max(np.abs(sza_c - sza_e))
        saa_max_array = np.abs(saa_c - saa_e)
        saa_max_array[saa_max_array > 300] = \
            saa_max_array[saa_max_array > 300] - 360
        saa_max = np.max(np.abs(saa_max_array))

        self.assertTrue(sza_max < 1.2)
        self.assertTrue(saa_max < 1.2)
