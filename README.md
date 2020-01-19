# Fast algorithm for the computation of the SZA and SAA
The implementation of the fast algorithm for computation of the
Solar Zenith Angle (aka SZA) and Solar Azimut Angle (aka SAA) based
on the logic proposed by Roberto Grena in 2012
(https://doi.org/10.1016/j.solener.2012.01.024).
The precision of the algorithm is 0.3 degrees for the SZA and 0.5
degrees for the SAA (mean-average error).

## Testing of the algorithm
Algorithm has been tested using PVLIB implementation of the SZA and SAA
computation which is precise up to 0.2 degrees (maximal error for both).

The PVLIB version is unfortunately much slower (which is the motivation
for writing of this algorithm).

## Usage
Algorithm requires the Pandas DatetimeIndex time array in the UTC.  Algorithm
also requires longitude and latitude of the place (in degrees).

You can run algorithm for testing purposes:
```
from sza_saa_grena import solar_zenith_and_azimuth_angle
# ...
# Some random time series:
time_array = pd.date_range("2020/1/1", periods=87_600, freq="10T", tz="UTC")
sza, saa = solar_zenith_and_azimuth_angle(longitude=-0.12435,  # London longitude
                                          latitude=51.48728,   # London latitude
                                          time_utc=time_array)
```

## Source
Five new algorithms for the computation of sun position from 2010 to 2110,
Roberto Grena, 2012, online: https://doi.org/10.1016/j.solener.2012.01.024