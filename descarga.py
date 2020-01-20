""" This script downloads grib files of GEFS Model (NOAA).
    Those files have a spatial resolution of 0.5 Degrees and
    includes the mean and spread of the ensemble for the most
    commonly used parameters.
    
    Diego Quintero
    2019""" 
import urllib.request
import pdb
import rlcompleter
from datetime import datetime
import os
import numpy as np
pdb.Pdb.complete=rlcompleter.Completer(locals()).complete 

date = datetime(2019,10,21)
days_for_download = 7 
download_step_hours = 3
path = '/home/diego/Documentos/Pronosticos_Luker/'

# Create a folder for the downloaded data
try:
    os.mkdir(path + date.strftime('%Y%m%d'))
    print('Path ' + path + date.strftime('%Y%m%d'), ' Created')
except FileExistsError:
    print('Path ' + date.strftime('%Y%m%d'), ' Already existed')

download_range = np.arange(0, days_for_download*24 + 7, download_step_hours)

# Ensemble avg and spr download
j = 0
for i in download_range:
    total_files_to_download =len(download_range) 
    if i < 10:
        i_str = '00' + str(i)
    elif i < 100:
        i_str = '0' + str(i)
    else: 
        i_str = str(i)

    for ens_est in ['avg', 'spr']:
        url = 'ftp://ftp.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.' +\
              date.strftime('%Y%m%d') +  '/00/pgrb2ap5/ge' + ens_est + '.t00z.pgrb2a.0p50.f' + i_str
        try:
            urllib.request.urlretrieve(url, path               
                 + date.strftime('%Y%m%d') + '/' + url.split('/')[-1])
            print(url + ' Done!   ' + str(round(100*(((j + 1)/2)/total_files_to_download), 1)) + '% Downloaded')
        except:
            print('Error downloading!!')
            pdb.set_trace()
            break
        j += 1

