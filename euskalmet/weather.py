from datetime import datetime
from typing import Union

import pandas as pd

from euskalmet import Euskalmet


class Weather(Euskalmet):
    def __init__(self):
        super().__init__()

    def get_weather_region(
        self,
        region_id: str,
        at: Union[str, datetime, pd.Timestamp],
        forecast_date: Union[str, datetime, pd.Timestamp],
    ) -> dict:
        """
        Obtiene la predicción meteorológica de un día para un día concreto.

        Parameters
        ----------
        region_id: str
            Identificador de la región: `basque_country`, `europe`, `iberic_peninsula`.
        at: str, datetime, pd.Timestamp
            Fecha en la que se realiza la predicción.
        forecast_date: str, datetime, pd.Timestamp
            Fecha a predecir.

        Returns
        -------
        DataFrame
            Predicción meteorológica.

        References
        ----------
        - https://www.opendata.euskadi.eus/api-euskalmet/?api=weather_region#/
        """
        at = pd.Timestamp(at)
        forecast_date = pd.Timestamp(forecast_date)

        params = {
            "regionId": region_id,
            "YYYY": f"{at.year:04}",
            "MM": f"{at.month:02}",
            "DD": f"{at.day:02}",
            "YYYYMMDD": forecast_date.strftime("%Y%m%d"),
        }
        endpoint = "/euskalmet/weather/regions/{regionId}/forecast/at/{YYYY}/{MM}/{DD}/for/{YYYYMMDD}".format(
            **params
        )
        data = self._download(endpoint)

        return data

    def get_weather_forecast_region_zone_location(
        self,
        region_id: str,
        zone_id: str,
        location_id: str,
        at: Union[str, datetime, pd.Timestamp],
        forecast_date: Union[str, datetime, pd.Timestamp],
    ) -> dict:
        """
        Obtiene la predicción meteorológica de un día para un día concreto.

            Parameters
            ----------
            at: str, datetime, pd.Timestamp
                Fecha en la que se realiza la predicción.
            forecast_date: str, datetime, pd.Timestamp
                Fecha a predecir.
            region_id: str
                Identificador de la región: `basque_country`, `europe`, `iberic_peninsula`.
            zone_id: str
                Identificador de la zona.
            location_id: str
                Identificador de la localización.

            Returns
            -------
            DataFrame
                Predicción meteorológica.

            References
            ----------
            - https://opendata.euskadi.eus/api-euskalmet/?api=weather_region_zone_location#/Weather%20Forecast/get_euskalmet_weather_regions__regionId__zones__zoneId__locations__locId__forecast_at__YYYY___MM___DD__for__YYYYMMDD_

            Examples
            --------
            >>> from euskalmet import Weather
            >>> weather = Weather("basque_country")
            >>> weather.get_weather_forecast_region_zone_location("2021-07-12", "2021-07-13", "basque_country", "donostialdea", "donostia")
            {
            "oid": "euskalmet/weather/regions/basque_country/zones/donostialdea/locations/donostia/forecast/at/2024/01/10/for/20240110",
            "numericId": 0,
            "entityVersion": 0,
            "at": "2024-01-10T12:23:38Z",
            "for": "2024-01-10T11:00:00Z",
            "region": {
                "typeId": "summarizedRegion",
                "key": "euskalmet/geo/regions/basque_country",
                "regionId": "basque_country"
            },
            "regionZone": {
                "typeId": "summarizedRegionZone",
                "key": "euskalmet/geo/regions/basque_country/zones/donostialdea",
                "regionId": "basque_country",
                "regionZoneId": "donostialdea"
            },
            "regionZoneLocation": {
                "typeId": "summarizedRegionZoneLocation",
                "key": "euskalmet/geo/regions/basque_country/zones/donostialdea/locations/donostia",
                "regionId": "basque_country",
                "regionZoneId": "donostialdea",
                "regionZoneLocationId": "donostia"
            },
            "temperature": {
                "value": 5.05,
                "unit": "CELSIUS_DEGREE"
            },
            "temperatureRange": {
                "min": 3.0,
                "max": 7.1,
                "unit": "CELSIUS_DEGREE"
            },
            "forecastText": {
                "SPANISH": "Cielo cubierto y lluvia. Viento sur; girar\u00e1 al norte por la tarde. Temperaturas m\u00e1ximas sin demasiados cambios.",
                "BASQUE": "Zerua estalita egongo da eta euria egingo du. Hego-haizea ibiliko da, arratsaldean iparraldera aldatuko da. Tenperatura maximoetan aldaketa handirik ez."
            }
        }
        """
        at = pd.Timestamp(at)
        forecast_date = pd.Timestamp(forecast_date)

        params = {
            "regionId": region_id,
            "zoneId": zone_id,
            "locId": location_id,
            "YYYY": f"{at.year:04}",
            "MM": f"{at.month:02}",
            "DD": f"{at.day:02}",
            "YYYYMMDD": forecast_date.strftime("%Y%m%d"),
        }
        endpoint = "/euskalmet/weather/regions/{regionId}/zones/{zoneId}/locations/{locId}/forecast/at/{YYYY}/{MM}/{DD}/for/{YYYYMMDD}".format(
            **params
        )
        data = self._download(endpoint)

        return data

    def get_last_measures_report_region_zone_location(
        self,
        region_id: str,
        zone_id: str,
        location_id: str,
        forecast_date: Union[str, datetime, pd.Timestamp],
    ) -> dict:
        """
        Obtiene el último informe de medidas de una localización.

        Parameters
        ----------
        region_id: str
            Identificador de la región: `basque_country`, `europe`, `iberic_peninsula`.
        zone_id: str
            Identificador de la zona.
        location_id: str
            Identificador de la localización.
        forecast_date: str, datetime, pd.Timestamp
            Fecha del informe.

        Returns
        -------
        dict
            Último informe de medidas.
        """
        forecast_date = pd.Timestamp(forecast_date)

        params = {
            "regionId": region_id,
            "zoneId": zone_id,
            "locId": location_id,
            "YYYY": f"{forecast_date.year:04}",
            "MM": f"{forecast_date.month:02}",
            "DD": f"{forecast_date.day:02}",
        }
        endpoint = "/euskalmet/weather/regions/{regionId}/zones/{zoneId}/locations/{locId}/reports/for/{YYYY}/{MM}/{DD}/last".format(
            **params
        )
        data = self._download(endpoint)

        return data


if __name__ == "__main__":
    import json

    today = pd.Timestamp.today()
    weather = Weather()
    # print(weather.get_weather_region("basque_country", today, today))
    # print(json.dumps(weather.get_weather_forecast_region_zone_location("basque_country", "donostialdea", "donostia", today, today), indent=4))
    print(
        json.dumps(
            weather.get_last_measures_report_region_zone_location(
                "basque_country", "donostialdea", "donostia", today
            ),
            indent=4,
        )
    )
