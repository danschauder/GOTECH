from owslib.wms import WebMapService

class AllenCoralExtractor():
    def __init__(self):
        """
        Extracts data from the Allen Coral Atlas API
        """
        pass

    def test(self):
        wms = WebMapService('https://allencoralatlas.org/geoserver/ows?service=wms', version='1.3.0')
        print(wms.identification.type)