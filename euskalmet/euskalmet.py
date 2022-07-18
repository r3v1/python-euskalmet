import configparser
import datetime
import json
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from typing import Union

import jwt
import numpy as np
import pandas as pd
import pytz
import requests
from tqdm import tqdm
import os
from exceptions import EuskalmetException


# TODO: Introducir loggers

class Euskalmet:
    """
    Objeto para el acceso a la API de Euskalmet.

    Antes de comenzar, es necesario tener una cuenta en la API de Euskalmet
    y obtener un token de acceso en la `web`_.

    Por un lado, hay que soliticar las claves en la web de la `API`_ y guardarla
    en ``~/.config/euskalmet/privateKey.pem``.

    Por otro lado, hay que definir un fichero de configuración en el directorio
    ``~/.config/euskalmet/settings.cfg`` con la siguiente información:

    .. code-block:: ini

        [PAYLOAD]
        ; Issuer (emisor): description issuer description, ex. company name
        iss =
        ; Timestamp expiration: Ex. 1616081478
        exp =
        ; Emission timestamp: Ex. 1618673478
        iat =
        ; Api key owner email: Ex. name@company.com
        email =


    .. _`web`: https://www.opendata.euskadi.eus/api-euskalmet/-/how-to-use-meteo-rest-services/
    .. _`API`: https://api.euskadi.eus/met01uiApiKeyUsersWar/index.jsp#/

    Examples
    --------
    >>> from euskalmet import Euskalmet
    >>> euskalmet = Euskalmet()
    >>> station_id = "C017"  # Selecciona una estación
    >>> euskalmet.automatic_download(station_id, multiprocess=True)
    """

    def __init__(self, ):
        # Define las rutas
        self.data_dir = Path("~/.euskalmet").expanduser() / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Define las URLs
        self.base_url = "https://api.euskadi.eus"

        # Define los ficheros para generar el payload
        self.config_dir = Path("~/.config/euskalmet").expanduser()
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Private key
        self._private_key_path = self.config_dir / "privateKey.pem"
        assert self._private_key_path.is_file(), f"No se encuentra el fichero de clave privada " \
                                                 f"en {self._private_key_path}"

        # Read config file
        cfg_file = self.config_dir / "settings.cfg"
        assert cfg_file.is_file(), f"No se encuentra el fichero de configuración en {cfg_file}"

        self.config = configparser.ConfigParser()
        self.config.read(cfg_file)

        self.tz = pytz.timezone("Europe/Madrid")

    def _get_header(self) -> dict:
        """
        Devuelve el header para la petición.

        Returns
        -------
        dict
            Header con la autenticación para la petición
            
        See Also
        --------
        - https://www.opendata.euskadi.eus/api-euskalmet/-/how-to-use-meteo-rest-services/
        """
        payload = {
            "aud": "met01.apikey",
            "iss": self.config["PAYLOAD"]["iss"],
            "exp": int(self.config["PAYLOAD"]["exp"]),
            "version": "1.0.0",
            "iat": int(self.config["PAYLOAD"]["iat"]),
            "email": self.config["PAYLOAD"]["email"],
        }
        myToken = jwt.encode(payload, open(self._private_key_path, "rb").read(), algorithm="RS256")
        return {'Authorization': f'Bearer {myToken}', "Accept": "application/json"}

    def _download(self, endpoint: str) -> dict:
        """
        Descarga los datos desde la API.

        Parameters
        ----------
        endpoint: str
            Endpoint de la API

        Returns
        -------
        dict
            Datos descargados o información de error.
            
        Raises
        ------
        EuskalmetException
        """
        headers = self._get_header()
        r = requests.get(self.base_url + endpoint, headers=headers)

        if r.status_code >= 300:
            # print(f"[!] Error {r.status_code}: {self.base_url + endpoint}")
            raise EuskalmetException({"error": r.status_code, "reason": r.reason, "url": self.base_url + endpoint})
        else:
            return json.loads(r.text)

    # ------------------------------------------------------------------------------------ #
    #           Métodos de la API de Euskalmet para los datos de las estaciones            #
    # ------------------------------------------------------------------------------------ #

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

    def get_sensor_info(self, sensor_id: str) -> dict:
        """
        Devuelve la lista de sensores de todas las estaciones

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

    def get_station_readings(self,
                             station_id: str,
                             sensor_id: str,
                             measure_type_id: str,
                             measure_id: str,
                             year: Union[str, int],
                             month: Union[str, int],
                             day: Union[str, int],
                             hour: Union[str, int]) -> dict:
        """
        Devuelve las lecturas para una medida específica y
        una fecha específica.

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
        url = f"/euskalmet/readings/forStation/{station_id}/{sensor_id}/measures/{measure_type_id}/{measure_id}/" \
              f"at/{int(year):04}/{int(month):02}/{int(day):02}/{int(hour):02}"

        data = self._download(url)

        return data

    # ------------------------------------------------------------------------------------ #
    #               Métodos útiles para agilizar la obtención de datos
    # ------------------------------------------------------------------------------------ #

    def get_station_sensors(self, station_id: str) -> dict:
        """
        Devuelve la lista de sensores de una estación dada.

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
            sensors_info = {x: self.get_sensor_info(x)["meteors"] for x in sensor_ids}
            with open(station_file_data, "w") as fp:
                json.dump(sensors_info, fp, indent=4)

        with open(station_file_data, "r") as fp:
            sensors_info = json.load(fp)

        return sensors_info

    def get_readings_from(self, start_date: pd.Timestamp, station_id: str) -> pd.DataFrame:
        """
        Devuelve todas las lecturas de una estación desde una fecha dada.

        Parameters
        ----------
        start_date: pd.Timestamp
            Fecha de inicio de la búsqueda
        station_id: str
            Id de la estación

        Returns
        -------
        pd.DataFrame
            DataFrame con las lecturas de la estación. Las fechas
            están en timezone Europe/Madrid.

        Examples
        --------
        >>> from euskalmet import Euskalmet
        >>> euskalmet = Euskalmet()
        >>> euskalmet.get_readings_from(pd.Timestamp('2022-05-19 17:00:00+0000', tz='UTC', freq='H'), "C017")
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
                args = dict(sensor_id=sensor_id,
                            station_id=station_id,
                            measure_type_id=measure_type["measureType"],
                            measure_id=measure_type["measureId"],
                            year=start_date.year,
                            month=start_date.month,
                            day=start_date.day,
                            hour=start_date.hour
                            )

                # Download new readings
                data = self.get_station_readings(**args)

                # Process data
                dt = pd.Timestamp(datetime.datetime.fromtimestamp(int(data["dateRange"][6:16])), tz=self.tz)
                idx = [
                    pd.Timestamp(f"{dt.tz_convert('utc'):%Y-%m-%d} {x['lowerEndPointDesc']}", tz="utc")
                    for x in data["slots"]
                ]
                idx = pd.to_datetime(idx, utc=True).tz_convert(self.tz)

                v = np.array([np.nan if x is None else x for x in data["values"]])
                if measure_type["measureId"] in ["max_speed", "speed_sigma", "mean_speed"]:
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

    def automatic_download(self, station_id: str, multiprocess: bool = True):
        """
        Descarga las últimas observaciones de la estación dada. Si el fichero
        con observaciones existe, parte de la última hora registrada hasta ahora
        para descargar nuevos datos. Si no existe, parte desde el 01-11-2021.

        Finalmente, las guarda en un fichero CSV en ~/.eskalmet/data/.

        Parameters
        ----------
        station_id: str
            Id de la estación
        multiprocess: bool
            Si es True, se utiliza multiprocessing para descargar las lecturas.
        """
        obs_output = self.data_dir / f"{station_id}_OBS_MERGED.csv"

        if obs_output.is_file():
            # Empezar desde la última hora guardada en el fichero
            obs = pd.read_csv(obs_output, index_col=["DATE"], parse_dates=["DATE"]).tz_convert(self.tz)
            start_date = obs.index.max()
        else:
            # Empezar desde los últimos 30 días
            start_date = pd.Timestamp(datetime.datetime.utcnow(), tz="utc").tz_convert(self.tz) - pd.Timedelta(days=60)
        end_date = pd.Timestamp(datetime.datetime.utcnow(), tz="utc").tz_convert(self.tz) - pd.Timedelta(hours=1)

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
            t_.set_description(f"[{station_id}] Obteniendo lecturas para {dates[i]} - {dates[i + 5]}")

            if multiprocess:
                # Multiprocess
                f = partial(self.get_readings_from, station_id=station_id)
                with Pool(processes=os.cpu_count() - 1 or 1) as pool:
                    dfs = pool.map(f, dates[i:i + 6])
                df = pd.concat(dfs)
            else:
                # Single process
                df = pd.concat([self.get_readings_from(dt, station_id=station_id) for dt in dates[i:i + 6]])

            if not df.empty:
                # Guardar las observaciones
                if obs_output.is_file():
                    obs = pd.read_csv(obs_output, index_col=["DATE"], parse_dates=["DATE"]).tz_convert(self.tz)

                    idx = df.index.intersection(obs.index)
                    obs.update(df.loc[idx])

                    # Añadir nuevas
                    idx = df.index.difference(obs.index)
                    df = pd.concat([obs, df.loc[idx]])

                df.to_csv(obs_output)


if __name__ == "__main__":
    euskalmet = Euskalmet()

    station_id = "C017"
    euskalmet.automatic_download(station_id, multiprocess=True)
