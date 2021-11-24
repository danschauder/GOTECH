import subprocess, time
import numpy as np

class AllenCoralGeomorphicExtractor():
    def __init__(self, latitude_min=-82.882919311523, 
                        latitude_max=-79.850692749023, 
                        longitude_min=24.208717346191,
                        longitude_max=26.405982971191,
                        download_path='./downloads/'
                        ):
        """
        Extracts benthic data from the Allen Coral Atlas API
        """
        self.latitude_min=latitude_min
        self.latitude_max=latitude_max
        self.longitude_min=longitude_min
        self.longitude_max=longitude_max
        self.download_path=download_path

    def construct_url(self,latitude_min,latitude_max, longitude_min, longitude_max):
        return f"https://allencoralatlas.org/geoserver/ows?service=wfs&version=2.0.0&request=GetFeature&typeNames=coral-atlas:geomorphic_data_verbose&srsName=EPSG:3857&bbox={longitude_min},{latitude_min},{longitude_max},{latitude_max}&outputFormat=shape-zip"

    def extract_and_load_file(self,latitude_min, latitude_max, longitude_min, longitude_max):
        url=self.construct_url(latitude_min, latitude_max, longitude_min, longitude_max)
        fname=f'aca_geomorphic_{time.time_ns()}'
        subprocess.run(['wget', url, '-O',self.download_path+fname+'.zip'])
        subprocess.run(['unzip','-d',self.download_path+fname+'/',self.download_path+fname+'.zip'])
        ogr_cmd = 'ogr2ogr -f PostgreSQL'
        ogr_cmd= ogr_cmd + ' PG:"host=localhost port=5432 user=GOTECH dbname=coral_data"'
        ogr_cmd = ogr_cmd + f' {self.download_path+fname}/geomorphic_data_verbose.shp'
        ogr_cmd = ogr_cmd + ' -nln raw.aca_geomorphic -geomfield geom'
        subprocess.run(ogr_cmd, shell=True)
            
    def extract_and_load(self):
        if self.latitude_max-self.latitude_min>0.5 or self.longitude_max-self.longitude_min>0.5:
            x=np.arange(self.latitude_min,self.latitude_max,0.5)
            print(x)
            y=np.arange(self.longitude_min,self.longitude_max,0.5)
            xx, yy = np.meshgrid(x, y)
            xx = xx.ravel()
            yy = yy.ravel()
            for i in range(len(xx)):
                self.extract_and_load_file(xx[i],xx[i]+0.5,yy[i],yy[i]+0.5)
        else:
            self.extract_and_load_file(self.latitude_min,self.latitude_max,self.longitude_min,self.longitude_max)