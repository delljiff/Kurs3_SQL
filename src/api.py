from abc import ABC, abstractmethod

from requests import get


class AbstractAPI(ABC):
    @abstractmethod
    def get_response(self):
        pass

    @abstractmethod
    def get_data(self):
        pass


class NominatimAPI(AbstractAPI):
    def __init__(self, country):
        self.__openstreetmap_url = "https://nominatim.openstreetmap.org/search"

        self.__headers = {
            "User-Agent": "test-app/1.0",
        }

        self.__params = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

    def get_response(self):
        response = get(
            self.__openstreetmap_url, params=self.__params, headers=self.__headers
        )
        response.raise_for_status()
        return response

    def get_data(self):
        data = self.get_response().json()[0]["boundingbox"]
        return data


class OpenSkyAPI(AbstractAPI):
    def __init__(self, coords):
        self.__opensky_url = "https://opensky-network.org/api/states/all?"

        self.__params = {
            "lamin": coords[0],
            "lamax": coords[1],
            "lomin": coords[2],
            "lomax": coords[3],
        }

    def get_response(self):
        response = get(self.__opensky_url, params=self.__params)
        response.raise_for_status()
        return response

    def get_data(self):
        data = self.get_response().json()["states"]
        airplanes = []

        for airplane in data:
            airplanes.append(
                {
                    "id": airplane[0],
                    "callsign": airplane[1].strip(),
                    "baro_altitude": airplane[7],
                    "on_ground": airplane[8],
                    "velocity": airplane[9],
                }
            )

        return airplanes


# nm = NominatimAPI("Canada")
# coords = nm.get_data()
# open_sky = OpenSkyAPI(coords)
# print(open_sky.get_data())


# api = APIAdapter()
# api.get_aeroplanes('Canada')
# print(api.aeroplanes)

"""
{
    "time": 1766142246,                 // UNIX-время сервера OpenSky (секунды)
    "states": [
        [
            "4b1812",                   // ICAO24 — уникальный идентификатор борта
            "SWR438A ",                 // Callsign — позывной рейса
            "Switzerland",              // Страна регистрации ВС
            1766166618,                 // time_position — время последнего обновления позиции
            1766166618,                 // last_contact — время последнего контакта
            -0.0168,                    // longitude — долгота (°)
            51.0888,                    // latitude — широта (°)
            4267.2,                     // baro_altitude — барометрическая высота (м)
            false,                      // on_ground — находится ли самолёт на земле
            189.7,                      // velocity — горизонтальная скорость (м/с)
            129.39,                     // true_track — курс (градусы)
            14.63,                      // vertical_rate — вертикальная скорость (м/с)
            null,                       // sensors — ID сенсоров (null = неизвестно)
            4282.44,                    // geo_altitude — геометрическая высота (м)
            "2061",                     // squawk — код ответчика (транспондера)
            false,                      // spi — специальный сигнал (emergency/priority)
            0                           // position_source — источник позиции
        ],
        ...
    ]
}
"""
