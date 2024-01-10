import datetime
import json
import os
from functools import partial
from multiprocessing import Pool
from typing import Union

import numpy as np
import pandas as pd
from tqdm import tqdm

from euskalmet import Euskalmet
from euskalmet.exceptions import EuskalmetException


class Stations(Euskalmet):
    def __init__(self):
        super().__init__()

    def get_stations(self) -> dict:
        """
        Devuelve la lista de estaciones disponibles.

        Returns
        -------
        dict
            Diccionario con las estaciones.

        References
        ----------
        - https://www.opendata.euskadi.eus/api-euskalmet/?api=stations_station
        """
        endpoint = "/euskalmet/stations"
        data = self._download(endpoint)

        return data

    def get_current_station_data(self, station_id: str) -> dict:
        """
        Devuelve los datos actuales de la estación dada.

        Parameters
        ----------
        station_id: str
            Id de la estación

        Returns
        -------
        dict
            Datos de la estación.

        References
        ----------
        - https://www.opendata.euskadi.eus/api-euskalmet/?api=stations_station#/Station%20at%20a%20date/get_euskalmet_stations__station_id__current
        """
        endpoint = f"/euskalmet/stations/{station_id}/current"
        data = self._download(endpoint)

        return data

    def get_station_readings(
        self,
        station_id: str,
        sensor_id: str,
        measure_type_id: str,
        measure_id: str,
        year: Union[str, int],
        month: Union[str, int],
        day: Union[str, int],
        hour: Union[str, int],
    ) -> dict:
        """
        Devuelve las lecturas para una medida específica y una fecha específica.

        Parameters
        ----------
        station_id: str
            Id de la estación
        sensor_id: str
            Id del sensor
        measure_type_id: str
            Id del tipo de medida
        measure_id: str
            Id de la medida
        year: str, int
            Año de la lectura en formato YYYY
        month: str, int
            Mes de la lectura en formato MM
        day: str, int
            Dia de la lectura en formato DD
        hour: str, int
            Hora de la lectura en formato HH

        Returns
        -------
        dict
            Lecturas de la estación.

        References
        ----------
        - https://www.opendata.euskadi.eus/api-euskalmet/?api=stations_readings#/Readings/get_euskalmet_readings_forStation__station_id___sensor_id__measures__measureTypeId___measureId__at__YYYY___MM___DD___HH_
        """
        url = (
            f"/euskalmet/readings/forStation/{station_id}/{sensor_id}/measures/{measure_type_id}/{measure_id}/"
            f"at/{int(year):04}/{int(month):02}/{int(day):02}/{int(hour):02}"
        )

        data = self._download(url)

        return data

    def get_sensors(self) -> dict:
        """
        Devuelve la lista de sensores de todas las estaciones.

        Parameters
        ----------
        sensor_id: str
            Id del sensor

        Returns
        -------
        dict
            Datos de la estación.

        References
        ----------
        - https://www.opendata.euskadi.eus/api-euskalmet/?api=stations_sensors#/Sensors/get_euskalmet_sensors__sensor_id_
        """
        endpoint = f"/euskalmet/sensors"
        data = self._download(endpoint)

        return data

    def get_sensor(self, sensor_id: str) -> dict:
        """
        Devuelve la lista de sensores de la estación dada.

        Parameters
        ----------
        sensor_id: str
            Id del sensor

        Returns
        -------
        dict
            Datos de la estación.

        References
        ----------
        - https://www.opendata.euskadi.eus/api-euskalmet/?api=stations_sensors#/Sensors/get_euskalmet_sensors__sensor_id_
        """
        endpoint = f"/euskalmet/sensors/{sensor_id}"
        data = self._download(endpoint)

        return data

    # ------------------------------------------------------------------------------------ #
    #               Métodos útiles para agilizar la obtención de datos
    # ------------------------------------------------------------------------------------ #

    def get_station_sensors(self, station_id: str) -> dict:
        """
        Devuelve la lista de sensores de la estación.

        Como es un recurso que se utiliza mucho, se cachea en memoria.

        Parameters
        ----------
        station_id: str
            Id de la estación

        Returns
        -------
        dict
            Diccionario con los sensores de la estación.
        """
        station_file_data = self.data_dir / f"{station_id}_info.json"
        if not station_file_data.is_file():
            info = self.get_current_station_data(station_id)
            sensor_ids = [x["sensorKey"].split("/")[-1] for x in info["sensors"]]
            sensors_info = {x: self.get_sensor(x)["meteors"] for x in sensor_ids}
            with open(station_file_data, "w") as fp:
                json.dump(sensors_info, fp, indent=4)

        with open(station_file_data, "r") as fp:
            sensors_info = json.load(fp)

        return sensors_info

    def get_readings_from(self, station_id: str, start_date: pd.Timestamp) -> pd.DataFrame:
        """
        Devuelve todas las lecturas de una estación desde una fecha dada.

        Parameters
        ----------
        station_id: str
            Id de la estación
        start_date: pd.Timestamp
            Fecha de inicio de la búsqueda

        Returns
        -------
        pd.DataFrame
            DataFrame con las lecturas de la estación. Las fechas
            están en timezone Europe/Madrid.

        Examples
        --------
        >>> from stations import Stations
        >>> estacion = Stations("C017")
        >>> estacion.get_readings_from(pd.Timestamp('2022-05-19 17:00:00+0000', tz='UTC', freq='H'))
                                   precipitation  irradiance  ...  max_speed  station
        DATE                                                  ...
        2022-05-19 19:00:00+02:00            0.0       239.7  ...     12.348     C017
        2022-05-19 19:10:00+02:00            0.0       193.6  ...      9.180     C017
        2022-05-19 19:20:00+02:00            0.0       171.8  ...      8.460     C017
        2022-05-19 19:30:00+02:00            0.0       148.6  ...      7.416     C017
        2022-05-19 19:40:00+02:00            0.0       127.5  ...      6.696     C017
        2022-05-19 19:50:00+02:00            0.0       105.5  ...      6.336     C017
        """
        # Recoger primero todos los sensores que tiene la estación
        sensors_info = self.get_station_sensors(station_id)

        # Convertir a UTC
        start_date = start_date.tz_convert("utc")

        # Descargar las medidas de cada sensor
        readings = []
        for sensor_id, values in sensors_info.items():
            for measure_type in values:
                args = dict(
                    station_id=station_id,
                    sensor_id=sensor_id,
                    measure_type_id=measure_type["measureType"],
                    measure_id=measure_type["measureId"],
                    year=start_date.year,
                    month=start_date.month,
                    day=start_date.day,
                    hour=start_date.hour,
                )

                # Download new readings
                try:
                    data = self.get_station_readings(**args)
                except EuskalmetException as e:
                    continue

                # Process data
                dt = pd.Timestamp(
                    datetime.datetime.fromtimestamp(int(data["dateRange"][6:16])),
                    tz=self.tz,
                )
                idx = [
                    pd.Timestamp(
                        f"{dt.tz_convert('utc'):%Y-%m-%d} {x['lowerEndPointDesc']}",
                        tz="utc",
                    )
                    for x in data["slots"]
                ]
                idx = pd.to_datetime(idx, utc=True).tz_convert(self.tz)

                v = np.array([np.nan if x is None else x for x in data["values"]])
                if measure_type["measureId"] in [
                    "max_speed",
                    "speed_sigma",
                    "mean_speed",
                ]:
                    # Convertir m/s a km/h
                    v *= 3.6
                tmp = pd.DataFrame({"DATE": idx, data["measure"]: v})
                tmp.set_index("DATE", inplace=True)

                readings.append(tmp)

        if len(readings) > 0:
            df = pd.concat(readings, axis=1)
            df["station"] = station_id
        else:
            df = pd.DataFrame()

        return df

    def automatic_download(
        self,
        station_id: str,
        multiprocess: bool = True,
        start_date: Union[str, pd.Timestamp] = None,
    ):
        """
        Descarga las últimas observaciones de la estación dada. Si el fichero con observaciones
        existe, parte de la última hora registrada hasta ahora para descargar nuevos datos. Si no
        existe, parte desde el 01-11-2021.

        Finalmente, las guarda en un fichero CSV en ~/.eskalmet/data/.

        Parameters
        ----------
        multiprocess: bool
            Si es True, se utiliza multiprocessing para descargar las lecturas.
        start_date: str, pd.Timestamp
            Fecha de inicio de la búsqueda
        """
        obs_output = self.data_dir / f"{station_id}_OBS_MERGED.csv"
        if start_date is not None:
            start_date = pd.Timestamp(start_date, tz="utc").tz_convert(self.tz)
        elif obs_output.is_file():
            # Empezar desde la última hora guardada en el fichero
            obs = pd.read_csv(obs_output, index_col=["DATE"], parse_dates=["DATE"]).tz_convert(
                self.tz
            )
            start_date = obs.index.max()
        else:
            # Empezar desde los últimos 30 días
            start_date = pd.Timestamp(datetime.datetime.utcnow(), tz="utc").tz_convert(
                self.tz
            ) - pd.Timedelta(days=30)
        end_date = pd.Timestamp(datetime.datetime.utcnow(), tz="utc").tz_convert(
            self.tz
        ) - pd.Timedelta(hours=1)

        start_date = start_date.floor("H")
        end_date = end_date.floor("H")

        dates = pd.date_range(start_date, end_date, freq="H")

        # Rellenar con horas anteriores para que sea múltiplo de 6
        i = 1
        while len(dates) % 6 != 0:
            dates = pd.date_range(start_date - pd.Timedelta(hours=i), end_date, freq="H")
            i += 1

        t_ = tqdm(range(0, len(dates) - 5, 6))
        for i in t_:
            t_.set_description(
                f"[{station_id}] Obteniendo lecturas para {dates[i]} - {dates[i + 5]}"
            )

            if multiprocess:
                # Multiprocess
                func = partial(self.get_readings_from, station_id)
                with Pool(processes=os.cpu_count() - 1 or 1) as pool:
                    dfs = pool.map(func, dates[i : i + 6])
                df = pd.concat(dfs)
            else:
                # Single process
                df = pd.concat([self.get_readings_from(station_id, dt) for dt in dates[i : i + 6]])

            if not df.empty:
                # Guardar las observaciones
                if obs_output.is_file():
                    obs = pd.read_csv(
                        obs_output, index_col=["DATE"], parse_dates=["DATE"]
                    ).tz_convert(self.tz)

                    idx = df.index.intersection(obs.index)
                    obs.update(df.loc[idx])

                    # Añadir nuevas
                    idx = df.index.difference(obs.index)
                    df = pd.concat([obs, df.loc[idx]])

                df.sort_index(inplace=True)
                df.to_csv(obs_output)


if __name__ == "__main__":
    estacion = Stations()
    estacion.automatic_download("C017", multiprocess=False)
