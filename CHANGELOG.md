# 0.2
2022-10-10

## Added

- Se crea la clase `Geo` y `Weather` para la solicitud de información que tengan que ver con las
  regiones y las predicciones meteo respectivamente.


# 0.1
2022-10-10

## Added

- Refactoriza los métodos de `Euskalmet` creando clases para cada tipo de solicitud.
- Se crea la clase `Stations` para la solicitud de información que tengan que ver con las estaciones.

# 0.0.3
2022-09-29

## Added

- Se puede especificar la fecha de inicio de la búsqueda de mediciones en la función `automatic_download`.
- Ordena el CSV exportado por fecha.

## Fixed

- Si `get_readings_from` encuentra un enlace inválido (`raise EuskalmetException()`), captura la excepción y continua
  la búsqueda. Por ejemplo, en el pasado pudo existir un sensor que ahora no existe y viceversa.


# 0.0.1
2022-07-18

## Added

- Las siguientes llamadas a la API han sido implementadas:
  - `/euskalmet/stations/{station_id}/current`: devuelve los datos actuales de la estación dada.
  - `/euskalmet/sensors/{sensor_id}`: devuelve la lista de sensores de todas las estaciones.
  - `/euskalmet/readings/forStation/{station_id}/{sensor_id}/measures/{measure_type_id}/{measure_id}/at/{year}/{month}/{day}/{hour}`: devuelve las lecturas para una medida específica y una fecha específica.
- Además, se proporcionan métodos algo más complicados para obtener en `DataFrame`s:
  - Todas las lecturas de una estación desde una fecha dada.
  - La lista de sensores disponibles de una estación.
