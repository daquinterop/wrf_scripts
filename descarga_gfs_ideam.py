import pdb
import rlcompleter
from datetime import datetime
import os
import numpy as np
pdb.Pdb.complete=rlcompleter.Completer(locals()).complete 

date = datetime.today()
date = datetime(date.year,date.month,date.day)
days_for_download = 7 
download_step_hours = 3
path = '/home/diego/Documentos/Pronosticos_Luker/'

# Create a folder for the downloaded data
try:
    os.mkdir(path + date.strftime('%Y%m%d'))
    print('Path ' + path + date.strftime('%Y%m%d'), ' Created')
except FileExistsError:
    print('Path ' + date.strftime('%Y%m%d'), ' Already existed')


url = 'http://bart.ideam.gov.co/wrfideam/new_modelo/WRF00COLOMBIA/tif/geoTIFFprechorario%s00Z.zip' % date.strftime('%d%m%Y')
os.system('proxy_on unal')
os.system('wget -U "Opera 11.0" "%s" -O %s/%s' % (url, 
                               date.strftime('%Y%m%d'), url.split('/')[-1]))
os.chdir('%s' % date.strftime('%Y%m%d')) 
os.system('unzip  -o  %s' % (url.split('/')[-1]))
