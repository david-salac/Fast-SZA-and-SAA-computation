#ifndef WEATHER_TO_POWER_SOLARANGLES_H
#define WEATHER_TO_POWER_SOLARANGLES_H

#include <ctime>
#include <vector>
#include <tuple>

class SolarAngles {
public:
    static std::tuple<double, double> solarZenithAndAzimuthAngle(double longitude, double latitude,
            std::time_t timeStamp);

};


#endif //WEATHER_TO_POWER_SOLARANGLES_H
