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

**Importante**

Destacar, los campos `exp` y `iat` son *timestamps* ([epochs](https://espanol.epochconverter.com/)). El campo
`exp`  (fecha de expiración) tiene que ser mayor que `iat` (fecha de emisión del certificado), y dicha emisión la emitirá
el portal de Euskalmet. La fecha de expiración puede ponerse cualquiera, pero siempre más alta que la fecha de hoy.

Del mismo modo, el email tiene que ser el mismo que indicaste en la solicitud de Euskalmet.

## Usar la librería

Si por ejemplo, se quiere descargar las observaciones de una estación,

```
from euskalmet import Stations
estacion = Stations() # Inicializa el objeto
estacion.automatic_download("C017", multiprocess=True) # Descarga la información de la estación
```

Para más información, revisa la documentación.

## ¿Dudas, sugerencias?

Para cualquier duda, sugerencia o mejora, siéntete libre de abrir una issue en el repositorio.
