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
    def __init__(self,years=['2021'],months=['04'],verbose=False):
        self.years=years
        self.months=months
        self.verbose=verbose
        self.baseurl = 'https://opendap.larc.nasa.gov/opendap/CALIPSO/LID_L1-Standard-V4-11'

    def get_calipso_data(self,url,lat_range=[15.0,29.0],lon_range=[-90.0,-60.6]):
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
            lat = np.array(dataset['Latitude'][min_index:max_index+1].data)
            latitude = lat.ravel()
            lon = np.array(dataset['Longitude'][min_index:max_index+1].data)
            longitude = lon.ravel()
            time_UTC = np.array(dataset['Profile_UTC_Time'][min_index:max_index+1]).astype('float')
            time_UTC=time_UTC.ravel()
            perp_bs_532_578=np.array(dataset['Perpendicular_Attenuated_Backscatter_532'][min_index:max_index+1,578:579]).ravel()
            perp_bs_532_579=np.array(dataset['Perpendicular_Attenuated_Backscatter_532'][min_index:max_index+1,579:580]).ravel()
            perp_bs_532_580=np.array(dataset['Perpendicular_Attenuated_Backscatter_532'][min_index:max_index+1,580:581]).ravel()
            perp_bs_532_581=np.array(dataset['Perpendicular_Attenuated_Backscatter_532'][min_index:max_index+1,581:582]).ravel()
            perp_bs_532_582=np.array(dataset['Perpendicular_Attenuated_Backscatter_532'][min_index:max_index+1,582:583]).ravel()
            df = pd.DataFrame(data={'time_UTC':time_UTC,
                                'Latitude': latitude,
                                    'Longitude':longitude,
                                'perp_bs_532_578':perp_bs_532_578,
                                'perp_bs_532_579':perp_bs_532_579,
                                'perp_bs_532_580':perp_bs_532_580,
                                'perp_bs_532_581':perp_bs_532_581,
                                'perp_bs_532_582':perp_bs_532_582,})
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
        # start=time.time()
        # print(len(files))
        ## Initialize a Pandas DataFrame with the first file
        # df = self.get_calipso_data(f'{self.baseurl}/{files[0][0]}/{files[0][1]}/{files[0][2]}')
        # for idx, file in enumerate(files[1:]):
        if self.verbose:
            print(f'Fetching and appending data for file {file}')
        df = self.get_calipso_data(f'{self.baseurl}/{file[0]}/{file[1]}/{file[2]}')
        # if df is not None and df_new is not None:
        #     df = pd.concat([df,df_new])

        #     print(f'File {idx} downloaded. Total time elapsed: {time.time()-start} seconds')
        #     if df is not None:
        #         print(df.shape)
        #     else:
        #         print('no matches found yet')
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
            return False

    def parallelized_download(self,num_workers):
        ##Do the first one individual to avoid conflicts with create table statements
        table_exists=False
        while not table_exists:
            file = self.files.pop()
            table_exists = self.download_files(file)

        ## After the table has been created, paralellize the remaining downloads
        # with Pool(num_workers) as p:
        #     p.map(self.download_files,self.files)

    def extract_and_load(self):
        self.get_filenames()
        self.parallelized_download(16)
        
