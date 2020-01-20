import pdb
import rlcompleter
from datetime import datetime, timedelta
import os
from osgeo import gdal
import numpy as np
from scipy import interpolate
import pandas as pd
from itertools import product
from collections import defaultdict
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

pdb.Pdb.complete=rlcompleter.Completer(locals()).complete 
hours = mdates.HourLocator()
date = datetime.today()
date = datetime(date.year,date.month,date.day)
path = '/home/diego/Documentos/Pronosticos_Luker/'
pluv = pd.read_csv('Puntos.csv')
os.chdir(date.strftime('%Y%m%d'))
point_x = list(pluv['x']) 
point_y = list(pluv['y'])

raster_list = []
for day, hour in product(range(1, 8), range(24)):
    ds = gdal.Open('PREC1H_{:02d}{:02d}{:04d}_fcst_DIA{:d}{:02d}HLC.tif'.format(date.day,
                   date.month, date.year, day, hour), gdal.GA_ReadOnly)
    rb = ds.GetRasterBand(1)
    data = rb.ReadAsArray()
    if day == 1 and hour == 0:
        gt = ds.GetGeoTransform()
        llon = gt[0]; ulat = gt[3]
        rlon = llon + ds.RasterXSize*gt[1]
        llat = ulat + ds.RasterYSize*gt[5]
        ny = ds.RasterYSize; nx = ds.RasterXSize
    lons = np.linspace(llon, rlon, ds.RasterXSize)
    lats = np.linspace(llat, ulat, ds.RasterYSize)
    raster_list.append(data)

dic_points = defaultdict() 
#Para Nearestndinterpolator
#latM, lonM = np.meshgrid(lats, lons)
#points = np.array((latM.flatten(), lonM.flatten())).T

for name, x, y in zip(pluv[pluv.columns[0]], point_x, point_y):
    point_list = []
    date_list = []
    for hour, raster in enumerate(raster_list):
        f = interpolate.RectBivariateSpline(lons, lats, raster, kx=1, ky=1)
        #f = interpolate.NearestNDInterpolator(points, raster.flatten())
        point_z = f(x, y)
        point_list.append(float(point_z))
        date_list.append(date + timedelta(days=hour/24))
    dic_points['{:s}'.format(name)] = point_list
df = pd.DataFrame(dic_points)
df.index = date_list
df.round(1).to_csv('{:s}_Alt.csv'.format(date.strftime('%Y%m%d')), sep='\t')
#Guardar plot para los puntos
ymax = np.ceil(df.max().max())
for i in df.columns:
    fig, ax = plt.subplots(figsize=(15, 4))
    ax.bar(df.index, df[i], width=0.03)
    ax.set_ylim(0, ymax)
    ax.set_xlim(df.index.min(), df.index.max())
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Precipitación - mm')
    ax.set_title('Precipitación Horaria - {:s}'.format(i))
    ax.xaxis.set_minor_locator(hours)
    ax.grid(which='major')
    plt.savefig('{:s}.png'.format(i.translate({ord(' '): None})))
tmpstr = ''
for i in df.columns:
    tmpstr = tmpstr + i.translate({ord(' '): None}) + '.png '
tmpstr = tmpstr + ' {:s}_Alt.csv'.format(date.strftime('%Y%m%d'))
os.system('zip {:s}_Alt.zip {:s}'.format(date.strftime('%Y%m%d'), tmpstr))

