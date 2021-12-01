from urllib.request import urlretrieve

class NEOExtractor():
    def __init__(self, 
                years=[2014],
                download_path='../downloads/'):
        self.download_path=download_path
        self.years=years
        self.leap_years=[i for i in range(2000,2060,4)]

    def get_neo_data(self):
        url='https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A0012021008.L3m_8D_CHL_chlor_a_4km.nc'
        destination=self.download_path + 'A0012021008.L3m_8D_CHL_chlor_a_4km.nc'
        urlretrieve(url,destination)
        


if __name__=="__main__":
    extractor=NEOExtractor()
    extractor.get_neo_data()
    # print(extractor.leap_years)