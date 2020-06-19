package solar_angles

import (
	"math"
	"time"
)

type SzaAndSaa struct {
	/// Structure that encapsulates computed SZA and SAA
	///
	/// Attributes:
	///     SZA (float64): Solar Zenith Angle
	///     SAA (float64): Solar Azimuth Angle
	SZA float64
	SAA float64
}

func SolarZenithAndAzimuthAngle(longitude, latitude float64, timeSeries []time.Time) []SzaAndSaa {
	/// Function that returns solar zenith and azimuth angle sequence at given location and for given time series.
	///
	/// Solar Zenith Angle is calculated with precision 0.3 degree in average (maximal error is 1.5 degree), and
	///     the Solar Azimuth Angle is calculated with precision 0.5 degree (maximal error is 2 degree).
	///     From Five new algorithms for the computation of sun position from 2010 to 2110, Roberto Grena, 2012,
	///     online: https://doi.org/10.1016/j.solener.2012.01.024
	///
	/// Args:
	///     longitude (float64): Longitude of the location in degrees.
	///         latitude (float64): Latitude of the location in degrees.
	///     time_series ([]time.Time): Time series for which the zenith and azimuth angle is computed
	///
	/// Returns:
	///     []float64: The sequence of solar zenith and azimuth angles
	year := make([]float64, len(timeSeries))
	month := make([]float64, len(timeSeries))
	day := make([]float64, len(timeSeries))
	dayHours := make([]float64, len(timeSeries))

	// Array with results
	resultSzaSaa := make([]SzaAndSaa, len(timeSeries))

	for i, timeStamp := range timeSeries {
		// Time vectors:
		year[i] = float64(timeStamp.Year())
		month[i] = float64(timeStamp.Month())
		day[i] = float64(timeStamp.Day())
		dayHours[i] = float64(timeStamp.Hour()) + float64(timeStamp.Minute()) / 60.0 +
			float64(timeStamp.Second()) / 3600.0

		// Time transformation:
		var yearVal float64 = math.Floor(365.25 * (year[i] - 2000.0))
		var monthVal float64 = math.Floor(30.6001 * (month[i] + 1.0))
		var yearValPc float64 = math.Floor(0.01 * year[i])
		var timeVec float64 = yearVal + monthVal - yearValPc + day[i] +
			0.0416667 * dayHours[i] - 21958.0

		// Transform latitude/longitude to radians
		var latRad float64 = math.Pi * latitude / 180.0
		var lonRad float64 = math.Pi * longitude / 180.0

		// Reasonable estimates for pressure and temperature
		var pressure float64 = 1.0  // unit: atmosphere
		var temperature float64 = 20.0  // unit: degree of celsius

		// Computation
		var dT float64 = 96.4 + 0.567 * (year[i] - 2061.0)
		var te float64 = timeVec + 1.1574e-5 * dT
		var wte float64 = 0.0172019715 * te

		var lambdaDecl float64 = -1.388803 + 1.720279216e-2 * te + 3.3366e-2 * math.Sin(wte - 0.06172) + 3.53e-4 *
			math.Sin(2.0 * wte - 0.1163)

		var epsilon float64 = 4.089567e-1 - 6.19e-9 * te

		var sl float64 = math.Sin(lambdaDecl)
		var cl float64 = math.Cos(lambdaDecl)
		var se float64 = math.Sin(epsilon)

		var ce float64 = math.Sqrt(1.0 - se * se)

		var rAsc float64 = math.Atan2(sl * ce, cl)
		// Get rid of negative values in rAsc
		if rAsc < 0 {
			rAsc += 2 * math.Pi
		}
		var hAng float64 = math.Mod(1.7528311 + 6.300388099 * timeVec + lonRad - rAsc + math.Pi, 2 * math.Pi) -
			math.Pi
		// Get rid of negative values in hAng
		if hAng < 0 {
			hAng += 2 * math.Pi
		}

		var sp float64 = math.Sin(latRad)
		var cp float64 = math.Sqrt(1.0 - sp * sp)
		var sd float64 = sl * se
		var cd float64 = math.Sqrt(1.0 - sd * sd)
		var sH float64 = math.Sin(hAng)
		var cH float64 = math.Cos(hAng)

		var se0 float64 = sp * sd + cp * cd * cH

		var ep float64 = math.Asin(se0) - 4.26e-5 * math.Sqrt(1.0 - se0 * se0)

		var dE float64 = (0.08422 * pressure) / ((273.0 + temperature) * math.Tan(ep + 0.003138 / (ep + 0.08919)))

		resultSzaSaa[i] = SzaAndSaa{
			SZA: (180.0/math.Pi) * ((math.Pi / 2) - ep - dE),
			SAA: (180.0/math.Pi) * (math.Pi + math.Atan2(sH, cH * sp - sd * cp / cd))}
	}

	return resultSzaSaa
}
