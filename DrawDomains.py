import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import numpy as np


def draw_screen_poly(lats, lons, m):
    x, y = m(lons, lats)
    xy = zip(x, y)
    poly = Polygon(list(xy), facecolor=None, edgecolor='k', linewidth=2, alpha=0.15)
    plt.gca().add_patch(poly)
    # lats = [-30, 30, 30, -30]
    # lons = [-50, -50, 50, 50]


deg_m = 111e3
d01 = {'ref_lat': 6.274, 'ref_lon': -75.108, 'e_we': 350, 'e_sn': 375, 'dx': 4000, 'name': 'col_2dom_1.3km_2'}
d02 = {'i_start': 60, 'j_start': 55, 'e_we': 350, 'e_sn': 375, 'grid_ratio': 3, 'parent': d01}
# d01 = {'ref_lat':5.324, 'ref_lon':-75.643, 'e_we':451, 'e_sn':526, 'dx':4000, 'name':'col_2dom_1.3km'}
# d02 = {'i_start':92, 'j_start':88, 'e_we':802, 'e_sn':1051, 'grid_ratio':3, 'parent':d01}
# d01 = {'ref_lat':4.109, 'ref_lon':-75.807, 'e_we':65, 'e_sn':100, 'dx':20000, 'name':'col_2dom_4km'}
# d02 = {'i_start':12, 'j_start':17, 'e_we':206, 'e_sn':337, 'grid_ratio':5, 'parent':d01}

d01Corners = {'lllat': d01['ref_lat'] - (d01['e_sn'] * d01['dx'] / deg_m) / 2,
              'lllon': d01['ref_lon'] - (d01['e_we'] * d01['dx'] / deg_m) / 2,
              'urlat': d01['ref_lat'] + (d01['e_sn'] * d01['dx'] / deg_m) / 2,
              'urlon': d01['ref_lon'] + (d01['e_we'] * d01['dx'] / deg_m) / 2}

d02Corners = {'lllat': d01Corners['lllat'] - (d01Corners['lllat'] - d01Corners['urlat']) * \
                       d02['j_start'] / d01['e_sn'],
              'lllon': d01Corners['lllon'] - (d01Corners['lllon'] - d01Corners['urlon']) * \
                       d02['i_start'] / d01['e_we'],
              'urlat': None, 'urlon': None}

d02Corners['urlat'] = d02Corners['lllat'] + d02['e_sn'] * (d02['parent']['dx'] / d02['grid_ratio']) / deg_m
d02Corners['urlon'] = d02Corners['lllon'] + d02['e_we'] * (d02['parent']['dx'] / d02['grid_ratio']) / deg_m
lats = [d02Corners['urlat'], d02Corners['lllat'], d02Corners['lllat'], d02Corners['urlat']]
lons = [d02Corners['urlon'], d02Corners['urlon'], d02Corners['lllon'], d02Corners['lllon']]
fig = plt.figure(figsize=(6, 6))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
m = Basemap(projection='merc', lon_0=d01['ref_lon'], lat_0=d01['ref_lat'], lat_ts=d01['ref_lat'],
            llcrnrlat=d01Corners['lllat'], llcrnrlon=d01Corners['lllon'],
            urcrnrlat=d01Corners['urlat'], urcrnrlon=d01Corners['urlon'],
            rsphere=6371200., resolution='h', area_thresh=100)
draw_screen_poly(lats, lons, m)
m.drawcoastlines()
m.drawstates()
m.drawcountries()
draw_screen_poly(lats, lons, m)
# draw parallels.
parallels = np.arange(-90., 90, 2.)
m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
# draw meridians
meridians = np.arange(180., 360., 2.)
m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)
plt.title('Dominio {:s}'.format(d01['name']))
plt.show()
