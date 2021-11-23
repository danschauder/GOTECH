import subprocess, time

class AllenCoralBenthicExtractor():
    def __init__(self, latitude_min=-83.047, 
                        latitude_max=-82.65, 
                        longitude_min=24.5,
                        longitude_max=24.78,
                        download_path='./downloads/',
                        unzip_path='./downloads/aca_benthic/'
                        ):
        """
        Extracts benthic data from the Allen Coral Atlas API
        """
        self.latitude_min=latitude_min
        self.latitude_max=latitude_max
        self.longitude_min=longitude_min
        self.longitude_max=longitude_max
        self.download_path=download_path
        self.unzip_path=unzip_path

    def construct_url(self,latitude_min,latitude_max, longitude_min, longitude_max):
        return f"https://allencoralatlas.org/geoserver/ows?service=wfs&version=2.0.0&request=GetFeature&typeNames=coral-atlas:benthic_data_verbose&srsName=EPSG:3857&bbox={longitude_min},{latitude_min},{longitude_max},{latitude_max}&outputFormat=shape-zip"

    def extract_and_load_file(self,latitude_min, latitude_max, longitude_min, longitude_max):
        url=self.construct_url(latitude_min, latitude_max, longitude_min, longitude_max)
        fname=f'aca_benthic_{time.time_ns()}.zip'
        subprocess.run(['wget', url, '-O',self.download_path+fname])
        subprocess.run(['unzip','-d',self.unzip_path+fname,self.download_path+fname])
        ogr_cmd = 'ogr2ogr -f PostgreSQL'
        ogr_cmd= ogr_cmd + ' PG:"host=localhost port=5432 user=GOTECH dbname=coral_data"'
        ogr_cmd = ogr_cmd + ' ./downloads/aca_benthic/benthic_data_verbose.shp'
        ogr_cmd = ogr_cmd + ' -nln raw.aca_benthic -geomfield geom'
        subprocess.run(ogr_cmd, shell=True)
    
    def extract_and_load(self):
        self.extract_and_load_file(self.latitude_min,
                                    self.latitude_max,
                                    self.longitude_min,
                                    self.longitude_max)
