# Python Euskalmet

![](https://img.shields.io/pypi/v/python-euskalmet) ![](https://img.shields.io/pypi/dm/python-euskalmet)

Librería cliente de la API de datos de Euskalmet. Permite obtener y manejar la información de la API de datos abiertos
de Euskadi. Cuenta con una serie de modelos de datos y métodos preparados para poder utilizarlos de forma fácil y
accesible.

La información que recoge y utiliza esta librería es propiedad de la Agencia Vasca de Meteorología.

**ATENCIÓN: Esta librería está en desarrollo y por ello, faltan muchas llamadas a la API de datos de Euskalmet. Abre un
issue o un pull request si quieres que esta librería tenga más funcionalidades. Mi tiempo da para lo que da :)**

## Instalación

Utiliza pip para instalar la librería:

```pip install python-euskalmet```

## Configuración

Es importante crear un directorio de configuración en ``~/.config/python-euskalmet`` para que la librería pueda
guardar la configuración.

### API Key

Obtén tu clave de API en la siguiente [web](https://api.euskadi.eus/met01uiApiKeyUsersWar/index.jsp#/). Luego, hay que soliticar las claves en la [web](https://www.opendata.euskadi.eus/api-euskalmet/-/how-to-use-meteo-rest-services/) y guardarla
en ``~/.config/euskalmet/privateKey.pem``.

### Ficheros de configuración

Por otro lado, hay que definir un fichero de configuración en el directorio ``~/.config/euskalmet/settings.cfg`` con
la siguiente información:

```
[PAYLOAD]
; Issuer (emisor): description issuer description, ex. company name
iss =
; Timestamp expiration: Ex. 1696081478
exp =
; Emission timestamp: (today's epoch)
iat =
; Api key owner email: Ex. name@company.com
email =
```

## Usar la librería

La clase principal de la librería es la clase Euskalmet.

```
euskalmet = Euskalmet() # Inicializa el objeto

station_id = "C017"  # Define el identificador de la estación
euskalmet.automatic_download(station_id, multiprocess=True) # Descarga la información de la estación
```

Para más información, revisa la documentación.

## ¿Dudas, sugerencias?

Para cualquier duda, sugerencia o mejora, siéntete libre de abrir una issue en el repositorio.