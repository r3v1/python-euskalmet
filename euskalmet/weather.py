from datetime import datetime
from typing import Union

import pandas as pd

from euskalmet import Euskalmet


class Weather(Euskalmet):
    def __init__(self, region_id: str):
        super().__init__()

        self.region_id = region_id

    def get_weather_region(
        self,
        at: Union[str, datetime, pd.Timestamp],
        forecast_date: Union[str, datetime, pd.Timestamp],
    ) -> dict:
        """
        Obtiene la predicción meteorológica de un día
        para un día concreto.

        Parameters
        ----------
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
            "regionId": self.region_id,
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


if __name__ == "__main__":
    weather = Weather("basque_country")
    print(weather.get_weather_region("2022-10-10", "2022-10-11"))
