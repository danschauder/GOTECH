import pandas as pd
import numpy as np
import geopandas as gp
import os
import requests
import lxml
import urllib
import time
from bs4 import BeautifulSoup
from pydap.client import open_url
from sqlalchemy import create_engine
from multiprocessing import Pool

class CALIPSOExtractor():
    def __init__(self,years=['2020'],months=['01','02','03','04','05','06'],verbose=False):
        self.years=years
        self.months=months
        self.verbose=verbose
        self.baseurl = 'https://opendap.larc.nasa.gov/opendap/CALIPSO/LID_L1-Standard-V4-10'

    def get_calipso_data(self,url,lat_range=[24.208717346191,26.405982971191],lon_range=[-82.882919311523,-79.850692749023]):
        """
        Function to download CALIPSO data for a given url
        """
        dataset = open_url(url)
        lat_vals = dataset['Latitude'][:].data
        lon_vals = dataset['Longitude'][:].data
        filter_array = np.zeros((lat_vals.shape[0],4))
        filter_array[:,0:1]=np.asarray(lat_vals>=lat_range[0])
        filter_array[:,1:2]=np.asarray(lat_vals<=lat_range[1])
        filter_array[:,2:3]=np.asarray(lon_vals>=lon_range[0])
        filter_array[:,3:4]=np.asarray(lon_vals<=lon_range[1])
        indices=np.all(filter_array,axis=1).nonzero()[0]
        if len(indices>0):
            min_index=np.min(indices)
            max_index=np.max(indices)
            data_dict={}
            data_dict['Latitude']=np.array(dataset['Latitude'][min_index:max_index+1].data).ravel()
            data_dict['Longitude']=np.array(dataset['Longitude'][min_index:max_index+1].data).ravel()
            data_dict['Land_Water_Mask']=np.array(dataset['Land_Water_Mask'][min_index:max_index+1].data).ravel()
            data_dict['time_UTC']=np.array(dataset['Profile_UTC_Time'][min_index:max_index+1]).astype('float').ravel()
            backscatter_532=dataset['Perpendicular_Attenuated_Backscatter_532'][min_index:max_index+1,:].data
            for i in range(backscatter_532.shape[1]):
                data_dict[f'perp_bs_532_{i+1}']=backscatter_532[:,i]
            # perp_bs_532_578=np.array(dataset['Perpendicular_Attenuated_Backscatter_532'][min_index:max_index+1,578:579]).ravel()
            # perp_bs_532_579=np.array(dataset['Perpendicular_Attenuated_Backscatter_532'][min_index:max_index+1,579:580]).ravel()
            # perp_bs_532_580=np.array(dataset['Perpendicular_Attenuated_Backscatter_532'][min_index:max_index+1,580:581]).ravel()
            # perp_bs_532_581=np.array(dataset['Perpendicular_Attenuated_Backscatter_532'][min_index:max_index+1,581:582]).ravel()
            # perp_bs_532_582=np.array(dataset['Perpendicular_Attenuated_Backscatter_532'][min_index:max_index+1,582:583]).ravel()
            df = pd.DataFrame(data=data_dict)
            return df

    def get_filenames(self):
        self.files=[]
        for year in self.years:
            for month in self.months:
                r=requests.get(f'{self.baseurl}/{year}/{month}/')
                soup = BeautifulSoup(r.text, 'lxml')
                for a in soup.find_all('a',href=True):
                    link = a['href']
                    if link.startswith('CAL') and link[-3:]=='hdf':
                        self.files.append((year, month, link))
        if self.verbose:
            print(f'Found a total of {len(self.files)} CALIPSO files')

    def download_files(self,file):
        if self.verbose:
            print(f'Fetching and appending data for file {file}')
        df = self.get_calipso_data(f'{self.baseurl}/{file[0]}/{file[1]}/{file[2]}')
        if df is not None:
            gdf = gp.GeoDataFrame(df,geometry=gp.points_from_xy(df.Longitude,df.Latitude))
            gdf['geometry']=gdf['geometry'].set_crs(epsg=4326)
            engine = create_engine('postgresql://{}@{}:{}/{}'.format("GOTECH", "127.0.0.1",5432, "coral_data"))
            gdf.to_postgis(name='calipso',con=engine,if_exists='append',schema='raw')
            if self.verbose:
                print('Added data')
            return True
        else:
            if self.verbose:
                print('Skipping file, all records outside bounding box')
                # print('.')
            return False

    def parallelized_download(self,num_workers):
        #Do the first one individually to avoid conflicts with create table statements
        table_exists=False
        while not table_exists:
            file = self.files.pop()
            table_exists = self.download_files(file)

        ## After the table has been created, parallelize the remaining downloads
        with Pool(num_workers) as p:
            p.map(self.download_files,self.files)

    def extract_and_load(self):
        start=time.time()
        self.get_filenames()
        self.parallelized_download(24)
        if self.verbose:
            print(f'Total time elapsed: {time.time()-start} seconds')

# if __name__=="__main__":
#     extractor = CALIPSOExtractor()
#     extractor.get_calipso_data('https://opendap.larc.nasa.gov/opendap/CALIPSO/LID_L1-Standard-V4-11/2021/04/CAL_LID_L1-Standard-V4-11.2021-04-02T07-41-12ZN.hdf')
        
