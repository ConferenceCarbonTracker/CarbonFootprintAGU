import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from cmocean import cm as cmo
%matplotlib qt

# read data
pathfolder = "/Users/milan/git/CarbonFootprintAGU/"
dat = np.load(pathfolder+"data/optimization/emissions_grid.npz")
lat = dat["lat"]
lon = dat["lon"]
T = dat["T"]

T[T == 0] = np.nan

lon[lon < 0] += 360

xx,yy = np.meshgrid(lon,lat)

## Great circle, equi-distant projection
# higher resolution for great circles
class AziEqui(ccrs.AzimuthalEquidistant):

    @property
    def threshold(self):
        return 1e3

SFOloc = (37.622452, -122.384071607814)

##
fig = plt.figure(figsize=(7.5,6))
# proj = ccrs.RotatedPole(pole_longitude=90, pole_latitude=0)
proj = ccrs.PlateCarree()
ax = fig.add_subplot(1,1,1,projection=proj)
ax.add_feature(cfeature.BORDERS,lw=0.2)
ax.coastlines()
#ax.set_extent([-179,179,-20,90])


#ax.set_xlim(-,1.8e7)
#ax.set_ylim(-1.2e7,1.5e7)

# scatter locations
colr = "#D71455"
ax.pcolormesh(xx,yy,T,transform=proj)

# add SF star
ax.scatter(SFOloc[0],SFOloc[1],100,c="lightgreen",marker="*",label="San Francisco",zorder=10,edgecolor="k",lw=0.5)

ax.set_title("Attendees of AGU Fall Meeting 2019",loc="left",fontweight="bold")
plt.imshow(T)
