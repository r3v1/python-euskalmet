# 0.0.1
2022-07-18

### Added

- Las siguientes llamadas a la API han sido implementadas:
  - `/euskalmet/stations/{station_id}/current`: devuelve los datos actuales de la estación dada.
  - `/euskalmet/sensors/{sensor_id}`: devuelve la lista de sensores de todas las estaciones.
  - `/euskalmet/readings/forStation/{station_id}/{sensor_id}/measures/{measure_type_id}/{measure_id}/at/{year}/{month}/{day}/{hour}`: devuelve las lecturas para una medida específica y una fecha específica.
- Además, se proporcionan métodos algo más complicados para obtener en `DataFrame`s:
  - Todas las lecturas de una estación desde una fecha dada.
  - La lista de sensores disponibles de una estación. 