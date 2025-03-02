from ael_satellite_tools.preprocess import Himawari

lat = [-10, 50]
lon = [90, 180]
data_path = '/data/cloud2025/your_account/data_folder/'

himawari = Himawari(data_path=data_path,lat_range=lat,lon_range=lon)

### Set download time period -- 1
year = ['2025'] # Year: from 2015
mon = ['02']    # Month: 01 02 ... 12
day = ['08']    # Day: 01 02 ... 30 31
hour = ['03']   # Hour: 00 01 ... 23
minn = ['00']    # Minute: 00 10 20 30 40 50
### Set download time period -- 2
time_period = ['201901231200','201901250000']
time_delta = ['days=0','hours=5','minutes=0']
time_period = []
time_delta= []
# Set band type
band = ['TIR']  # band: VIS TIR SIR EXT
band_num = [1]      # band number: 1 2 ... 10
geo = ['sun.azm', 'sun.zth','sat.azm', 'sat.zth']

#band, band_num = himawari.band_name_convert(AHI_band)
#print(band,band_num)

time_list = himawari.generate_time_list(time_period=time_period,
                                        time_delta=time_delta,
                                        year=year,mon=mon,day=day,
                                        hour=hour,minn=minn)

file_list, zip_file_list, ftp_path_file_list = \
        himawari.generate_list(time_period=time_period,time_delta=time_delta,
                               year=year,mon=mon,day=day,hour=hour,minn=minn,
                               band=band,band_num=band_num,geo=geo,band4km=[])


# integrate from himawari.check_exist_sub_domain_file to himawari.generate_nc
himawari.pre_process(ftp_path_file_list,remove_list_flag=True)
