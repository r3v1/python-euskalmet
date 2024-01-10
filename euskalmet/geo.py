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

    def get_region_data(self, region_id: str) -> dict:
        """
        Devuelve los datos de una región dada de Euskalmet.

        Parameters
        ----------
        region_id : str
            Identificador de la región: `basque_country`, `europe`, `iberic_peninsula`.

        References
        ----------
        - https://opendata.euskadi.eus/api-euskalmet/?api=geolocations_regions#/regions/get_euskalmet_geo_regions__regionId_

        Examples
        --------
        >>> from euskalmet import Geo
        >>> geo = Geo()
        >>> geo.get_region_data("basque_country")
        {
            'oid': 'euskalmet/geo/regions/basque_country',
            'numericId': 0,
            'entityVersion': 0,
            'nameByLang': {
                'SPANISH': 'País Vasco',
                'BASQUE':
                'Euskal Herria'
            },
            'region': {
                'typeId': 'summarizedRegion',
                'key': 'euskalmet/geo/regions/basque_country',
                'regionId': 'basque_country'
            }
        }
        """

        endpoint = f"/euskalmet/geo/regions/{region_id}"
        data = self._download(endpoint)

        return data

    def get_zones(self, region_id: str) -> dict:
        """
        Devuelve la lista de zonas de una región de Euskalmet.

        Parameters
        ----------
        region_id : str
            Identificador de la región: `basque_country`, `europe`, `iberic_peninsula`.

        Returns
        -------
        dict
            Lista de zonas de una región de Euskalmet.
        """
        endpoint = f"/euskalmet/geo/regions/{region_id}/zones"
        data = self._download(endpoint)

        return data

    def get_region_zone_data(self, region_id: str, zone_id: str) -> dict:
        """
        Devuelve los datos de una zona dada de una región dada de Euskalmet.

        Parameters
        ----------
        region_id : str
            Identificador de la región: `basque_country`, `europe`, `iberic_peninsula`.
        zone_id : str
            Identificador de la zona.

        Returns
        -------
        dict
            Datos de una zona dada de una región dada de Euskalmet.

        Examples
        --------
        >>> from euskalmet import Geo
        >>> geo = Geo()
        >>> geo.get_region_zone_data("basque_country", "donostialdea")
        {
            'oid': 'euskalmet/geo/regions/basque_country/zones/donostialdea',
            'numericId': 0,
            'entityVersion': 0,
            'nameByLang': {
                'SPANISH': 'Donostialdea',
                'BASQUE': 'Donostialdea'
            },
            region': {
                'typeId': 'summarizedRegion',
                'key': 'euskalmet/geo/regions/basque_country',
                'regionId': 'basque_country'
            },
            'zone': {
                'typeId': 'summarizedRegionZone',
                'key': 'euskalmet/geo/regions/basque_country/zones/donostialdea',
                'regionId': 'basque_country',
                regionZoneId': 'donostialdea'
            }
        }
        """
        endpoint = f"/euskalmet/geo/regions/{region_id}/zones/{zone_id}"
        data = self._download(endpoint)

        return data

    def get_region_zone_locations(self, region_id: str, zone_id: str) -> dict:
        """
        Devuelve la lista de localidades de una zona de una región de Euskalmet.

        Parameters
        ----------
        region_id : str
            Identificador de la región: `basque_country`, `europe`, `iberic_peninsula`.
        zone_id : str
            Identificador de la zona.

        Returns
        -------
        dict
            Lista de localidades de una zona de una región de Euskalmet.

        Examples
        --------
        >>> from euskalmet import Geo
        >>> geo = Geo()
        >>> geo.get_region_zone_locations("basque_country", "donostialdea")
        [
            {
                'key': 'euskalmet/geo/regions/basque_country/zones/donostialdea/locations/donostia',
                'regionId': 'basque_country',
                'regionZoneId': 'donostialdea',
                'regionZoneLocationId': 'donostia'
            },
            {
                'key': 'euskalmet/geo/regions/basque_country/zones/donostialdea/locations/errenteria',
                'regionId': 'basque_country',
                'regionZoneId':
                'donostialdea',
                'regionZoneLocationId': 'errenteria'
            },
            {
                'key': 'euskalmet/geo/regions/basque_country/zones/donostialdea/locations/pasaia',
                'regionId': 'basque_country',
                'regionZoneId': 'donostialdea',
                'regionZoneLocationId': 'pasaia'
            }
        ]
        """
        endpoint = f"/euskalmet/geo/regions/{region_id}/zones/{zone_id}/locations"
        data = self._download(endpoint)

        return data

    def get_region_zone_location_data(self, region_id: str, zone_id: str, location_id: str) -> dict:
        """
        Devuelve los datos de una localidad dada de una zona dada de una región dada de Euskalmet.

        Parameters
        ----------
        region_id : str
            Identificador de la región: `basque_country`, `europe`, `iberic_peninsula`.
        zone_id : str
            Identificador de la zona.
        location_id : str
            Identificador de la localidad.

        Returns
        -------
        dict
            Datos de una localidad dada de una zona dada de una región dada de Euskalmet.

        Examples
        --------
        >>> from euskalmet import Geo
        >>> geo = Geo()
        >>> geo.get_region_zone_location_data("basque_country", "donostialdea", "donostia")
        {
            "oid": "euskalmet/geo/regions/basque_country/zones/donostialdea/locations/donostia",
            "numericId": 0,
            "entityVersion": 0,
            "nameByLang": {
                "SPANISH": "San Sebasti\u00e1n",
                "BASQUE": "Donostia"
            },
            "region": {
                "typeId": "summarizedRegion",
                "key": "euskalmet/geo/regions/basque_country",
                "regionId": "basque_country"
            },
            "zone": {
                "typeId": "summarizedRegionZone",
                "key": "euskalmet/geo/regions/basque_country/zones/donostialdea",
                "regionId": "basque_country",
                "regionZoneId": "donostialdea"
            },
            "regionZoneLocationId": {
                "typeId": "summarizedRegionZoneLocation",
                "key": "euskalmet/geo/regions/basque_country/zones/donostialdea/locations/donostia",
                "regionId": "basque_country",
                "regionZoneId": "donostialdea",
                "regionZoneLocationId": "donostia"
            }
        }
        """
        endpoint = f"/euskalmet/geo/regions/{region_id}/zones/{zone_id}/locations/{location_id}"
        data = self._download(endpoint)

        return data

    # TODO: Get basins


if __name__ == "__main__":
    geo = Geo()
    # print(geo.get_regions())
    # print(geo.get_region_data("basque_country"))

    # print(geo.get_zones("basque_country"))
    # print(geo.get_region_zone_data("basque_country", "donostialdea"))

    # print(geo.get_region_zone_locations("basque_country", "donostialdea"))
    print(geo.get_region_zone_location_data("basque_country", "donostialdea", "donostia"))
