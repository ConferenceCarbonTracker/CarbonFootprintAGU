import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from cmocean import cm as cmo
%matplotlib qt

## read colormaps

cpath = "/Users/milan/python/ScientificColourMaps5/"
davos = LinearSegmentedColormap.from_list("test",np.loadtxt(cpath+"davos/davos.txt"))
lajolla = LinearSegmentedColormap.from_list("test",np.loadtxt(cpath+"lajolla/lajolla.txt"))
batlow = LinearSegmentedColormap.from_list("test",np.loadtxt(cpath+"batlow/batlow.txt"))
bamako = LinearSegmentedColormap.from_list("test",np.loadtxt(cpath+"bamako/bamako.txt"))

## read data
pathfolder = "/Users/milan/git/CarbonFootprintAGU/"
dat = np.load(pathfolder+"data/optimization/emissions_grid.npz")
lat = dat["lat"]
lon = np.hstack((dat["lon"],180))   # extend lon to 180
T = np.concatenate((dat["T"],np.matrix(dat["T"][:,0]).T),axis=1)
xx,yy = np.meshgrid(lon,lat)

SFOloc = (37.622452, -122.384071607814)
IADloc = (38.9522097, -77.4534242937754)
WAAloc = (49.8537377,-97.2923083)

# plot in percent
T_SFO = 69334000
Tr = T/T_SFO*100

# find minimum
Tmin = np.unravel_index(np.argmin(Tr),Tr.shape)

##
fig = plt.figure(figsize=(6,6))
plt.subplots_adjust(left=0.03, bottom=0.15, right=0.97, top=0.95, wspace=0, hspace=0)
proj = ccrs.NorthPolarStereo(central_longitude=-100)
ax = fig.add_subplot(1,1,1,projection=proj,aspect="auto")
pos = ax.get_position()
cax = fig.add_axes([pos.x0,0.1,pos.width,0.03])

ax.add_feature(cfeature.BORDERS,lw=0.2)
ax.coastlines()
ax.add_feature(cfeature.LAKES,facecolor="#97BACD",alpha=0.2,edgecolor="grey")

ax.set_extent([-180, 180, 20, 90], ccrs.PlateCarree())
ax.set_ylim(-8e6,4e6)
ax.set_xlim(-7e6,7e6)

# scatter locations
levs = np.arange(80,150,5)
q = ax.contourf(xx,yy,Tr,levs,transform=ccrs.PlateCarree(),cmap=batlow.reversed(),extend="max")
ax.contour(xx,yy,Tr,[100],transform=ccrs.PlateCarree(),colors=("white",))
cbar = plt.colorbar(q,cax=cax,orientation="horizontal")
cbar.set_label("% of emissions relative to San Francisco")

# add SF and Washington, Winnipeg star
ax.scatter(SFOloc[1],SFOloc[0],100,c="lightgreen",marker="*",
    label="San Francisco",zorder=10,edgecolor="k",lw=0.5,
    transform=ccrs.PlateCarree())

ax.scatter(IADloc[1],IADloc[0],100,c="C3",marker="*",
    label="Washington DC",zorder=10,edgecolor="k",lw=0.5,
    transform=ccrs.PlateCarree())

ax.scatter(WAAloc[1],WAAloc[0],100,c="C1",marker="*",
    label="Winnipeg",zorder=10,edgecolor="k",lw=0.5,
    transform=ccrs.PlateCarree())

ax.scatter(lon[Tmin[1]],lat[Tmin[0]],100,c="C0",marker="*",
    label="Optimal",zorder=10,edgecolor="k",lw=0.5,
    transform=ccrs.PlateCarree())

ax.set_title("Optimal location of AGU Fall Meeting",loc="left",fontweight="bold")
ax.legend(loc=2)
