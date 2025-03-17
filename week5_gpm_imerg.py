import netCDF4 as nc
import numpy as np
import glob
import numpy.ma as ma

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.colors import ListedColormap

###read data
files = sorted(glob.glob('/data/dadm1/obs/GPM_IMERG/GPM_3IMERGHH.07/2021/213/*.HDF5'))
print(files[10])
re = nc.Dataset(files[10], 'r',  format='NETCDF4_CLASSIC')
print(re)

grid = re.groups['Grid']
print(grid)

prec = np.array(grid.variables['precipitation'])
intermediate = grid.groups['Intermediate']
irprec = np.array(intermediate.variables['IRprecipitation'])

### adjust lon lat
gpm_lon = np.arange(5,35996,10)/100
gpm_lat = np.arange(-8995,8996,10)/100
print(gpm_lat.shape)

print(prec.shape)
pp = np.zeros((3600,1800))
pp[0:1800,:] = prec[0,1800:3600,:]
pp[1800:3600,:] = prec[0,0:1800,:]
tpp = pp.T
print(tpp.shape)
###

print(gpm_lat[975],gpm_lat[1400])
print(gpm_lon[1000],gpm_lon[1600])


### plotting unit
# color map
cmap1 = mpl.cm.Blues(np.linspace(0,1,10))
self_cmap = np.vstack((cmap1[2],cmap1[4],cmap1[6]))
colors = [ (0.79,0.79,0.79,0.) ]
cmap = mpl.colors.ListedColormap(self_cmap)
cmap.set_extremes(over=cmap1[8])
cmap.set_extremes(under=colors[0])

# plot grid
xi, yi = np.meshgrid(gpm_lon[1000:1600],gpm_lat[975:1400])

fig,ax1 = plt.subplots(1,1,figsize=(27,10),tight_layout=True)
m = Basemap(llcrnrlon=100, urcrnrlon=160, llcrnrlat=7.5, urcrnrlat=50,resolution='i')
m.drawcoastlines(linewidth=1.5,color='gold')
m.drawparallels(np.arange(-10., 61., 10), labels=[1, 0, 0, 0], linewidth=0.01, color='k', fontsize=20)
m.drawmeridians(np.arange(100., 181., 10), labels=[0, 0, 0, 1], linewidth=0.01, color='k', fontsize=20)
masked_pp = ma.masked_where(tpp < 0, tpp)
pr = m.contourf(xi,yi,masked_pp[975:1400,1000:1600],vmin=2,vmax=30,cmap=cmap,levels=[2,10,20,30],extend='both',zorder=3)
c_pr = plt.colorbar(pr,extend='both',orientation='vertical',pad=0.033,fraction=0.010,aspect=16,anchor=(0.0,0.026))
c_pr.ax.tick_params(labelsize=15)
plt.text(163,7.7,'Pr [mm/hr]',fontsize=15)
plt.savefig('gpm_plot_demo.png',dpi=200)
