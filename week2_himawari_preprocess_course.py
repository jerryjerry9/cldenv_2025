from ael_satellite_tools.preprocess import Himawari
import matplotlib.pyplot as plt
import numpy as np

lat = [-10, 50]
lon = [90, 180]
data_path = '/data/cloud2025/your_account/data_folder/'

himawari = Himawari(data_path=data_path,lat_range=lat,lon_range=lon)
print(himawari.lat_range)
print(himawari.lon_range)
print(himawari.data_path)

himawari.information(detail=False)

### Set download time period -- 1
year = ['2025']      # Year: from 2015
mon = ['02']         # Month: 01 02 ... 12
day = ['08']         # Day: 01 02 ... 30 31
hour = ['03']        # Hour: 00 01 ... 23
minn = ['00']        # Minute: 00 10 20 30 40 50
### Set download time period -- 2
time_period = ['201901231200','201901250000']
time_delta=['days=0','hours=5','minutes=0']
# Set band type
band = ['EXT','VIS','TIR']  # band: VIS TIR SIR EXT
band_num = [1]              # band number: 1 2 ... 10
geo = []                    # ['sun.azm', 'sun.zth','sat.azm', 'sat.zth']

file_list, zip_file_list, ftp_path_file_list = himawari.generate_list(time_period=[], 
                  time_delta=[], year=year, mon=mon, day=day, hour=hour, 
                  minn=minn, band=band, band_num=band_num, geo=geo)

#himawari.check_exist_sub_domain_file(ftp_path_file_list, remove_list_flag=True, extend_lonlat_range=True)

output_file_list = himawari.download(ftp_path_file_list, download_flag=True)

output_file_list, data_array = himawari.unzip(output_file_list)

output_file_list, np_binary_data = himawari.read_binary(output_file_list, data_array, binary_type=[])

band_tbb = himawari.convert(output_file_list, np_binary_data)

#himawari.generate_binary(file_name,data_array)

sub_band_tbb, sub_lon, sub_lat = himawari.sub_domain_extract(band_tbb)

himawari.generate_nc(output_file_list, sub_band_tbb, sub_lon, sub_lat, nc_output=True)

