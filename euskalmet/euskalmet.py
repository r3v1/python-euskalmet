import configparser
import json
from pathlib import Path

import jwt
import pytz
import requests
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

    def __init__(self):
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
        assert self._private_key_path.is_file(), (
            f"No se encuentra el fichero de clave privada " f"en {self._private_key_path}"
        )

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
        return {"Authorization": f"Bearer {myToken}", "Accept": "application/json"}

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
            raise EuskalmetException(
                {
                    "error": r.status_code,
                    "reason": r.reason,
                    "url": self.base_url + endpoint,
                }
            )
        else:
            return json.loads(r.text)
