from euskalmet import Euskalmet


class Geo(Euskalmet):
    def __init__(self):
        super().__init__()

    def get_regions(self) -> dict:
        """
        Devuelve la lista de regiones de Euskalmet.

        Devuelve un listado de resúmenes de todas las  regiónes de
        Euskalmet. Esta lista está compuesta por un objeto resumen
        que proporciona la información necesaria para acceder a los
        datos completos de cada región y un dato resumen de cada región
        registrada.

        References
        ----------
        - https://www.opendata.euskadi.eus/api-euskalmet/?api=geolocations_regions#/regions/get_euskalmet_geo_regions

        Examples
        --------
        >>> from euskalmet import Geo
        >>> geo = Geo()
        >>> geo.get_regions()
        [
            {
                'key': 'euskalmet/geo/regions/basque_country',
                'regionId': 'basque_country'
            },
            {
                'key': 'euskalmet/geo/regions/europe',
                'regionId': 'europe'
            },
            {
                'key': 'euskalmet/geo/regions/iberic_peninsula',
                'regionId': 'iberic_peninsula'
            }
        ]
        """

        endpoint = "/euskalmet/geo/regions"
        data = self._download(endpoint)

        return data


if __name__ == "__main__":
    geo = Geo()
    print(geo.get_regions())
