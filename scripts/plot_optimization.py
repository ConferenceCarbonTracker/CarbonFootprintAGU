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
dat = np.load(pathfolder+"data/optimization/emissions_grid_fine.npz")
lat = dat["lat"]
lon = np.hstack((dat["lon"],180))   # extend lon to 180
T = np.concatenate((dat["T"],np.matrix(dat["T"][:,0]).T),axis=1)
xx,yy = np.meshgrid(lon,lat)

SFOloc = (37.622452, -122.384071607814)
IADloc = (38.9522097, -77.4534242937754)
WAAloc = (49.8537377,-97.2923083)
MSPloc = (44.879703,-93.2355128)
ORDloc = (41.9741625,-87.9095101)
MKEloc = (42.9457931,-87.908131)

# plot in percent
T_SFO = 69334
Tr = T/T_SFO*100

# find minimum
Tmin = np.unravel_index(np.argmin(Tr),Tr.shape)

# find emissions at given locations
IADe = Tr[np.where(lat == int(round(IADloc[0])))[0][0],np.where(lon == int(round(IADloc[1])))[0][0]]
WAAe = Tr[np.where(lat == int(round(WAAloc[0])))[0][0],np.where(lon == int(round(WAAloc[1])))[0][0]]
MSPe = Tr[np.where(lat == int(round(MSPloc[0])))[0][0],np.where(lon == int(round(MSPloc[1])))[0][0]]
ORDe = Tr[np.where(lat == int(round(ORDloc[0])))[0][0],np.where(lon == int(round(ORDloc[1])))[0][0]]
MKEe = Tr[np.where(lat == int(round(MKEloc[0])))[0][0],np.where(lon == int(round(MKEloc[1])))[0][0]]

##
fig = plt.figure(figsize=(6,6))
plt.subplots_adjust(left=0.03, bottom=0.15, right=0.97, top=0.95, wspace=0, hspace=0)
#proj = ccrs.NorthPolarStereo(central_longitude=-100)
#proj = ccrs.PlateCarree()
proj = ccrs.LambertConformal(central_longitude=-96.0, central_latitude=40.0)
ax = fig.add_subplot(1,1,1,projection=proj,aspect="auto")
pos = ax.get_position()
cax = fig.add_axes([pos.x0,0.1,pos.width,0.03])

ax.add_feature(cfeature.BORDERS,lw=0.2)
ax.add_feature(cfeature.OCEAN,alpha=.5,zorder=8)
ax.coastlines(resolution="50m",zorder=9)
ax.add_feature(cfeature.LAKES,facecolor="#97BACD",alpha=0.2,edgecolor="grey")
states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='110m',
        facecolor='none')

ax.add_feature(states_provinces, edgecolor='gray',zorder=1)

#ax.set_extent([-180, 180, 20, 90], ccrs.PlateCarree())
ax.set_extent([-120, -70, 22, 65])
#ax.set_ylim(-8e6,4e6)
#ax.set_xlim(-7e6,7e6)

# scatter locations
levs = np.arange(85,116,1)
q = ax.contourf(xx,yy,Tr,levs,transform=ccrs.PlateCarree(),cmap=cmo.tempo,extend="max")
ax.contour(xx,yy,Tr,[90,100],transform=ccrs.PlateCarree(),colors=("white",))
cbar = plt.colorbar(q,cax=cax,orientation="horizontal")
cbar.set_label("% of emissions relative to San Francisco")
cbar.set_ticks([85,90,95,100,105,110,115])
cbar.ax.axvline(x=0.5, c='w')
cbar.ax.axvline(x=1/6, c='w')

# add SF and Washington, Winnipeg star
ax.scatter(SFOloc[1],SFOloc[0],100,c="C3",marker="*",
    label=" 100%   San Francisco",zorder=10,edgecolor="k",lw=0.5,
    transform=ccrs.PlateCarree())

ax.scatter(IADloc[1],IADloc[0],100,c="C1",marker="*",
    label="{:1.1f}%   Washington DC".format(IADe),zorder=10,edgecolor="k",lw=0.5,
    transform=ccrs.PlateCarree())

ax.scatter(ORDloc[1],ORDloc[0],100,c="yellow",marker="*",
    label="{:1.1f}%   Chicago".format(ORDe),zorder=10,edgecolor="k",lw=0.5,
    transform=ccrs.PlateCarree())

ax.scatter(MKEloc[1],MKEloc[0],100,c="C0",marker="*",
    label="{:1.1f}%   Milwaukee".format(MKEe),zorder=10,edgecolor="k",lw=0.5,
    transform=ccrs.PlateCarree())

ax.scatter(WAAloc[1],WAAloc[0],100,c="cyan",marker="*",
    label="{:1.1f}%   Winnipeg".format(WAAe),zorder=10,edgecolor="k",lw=0.5,
    transform=ccrs.PlateCarree())

ax.scatter(MSPloc[1],MSPloc[0],100,c="C2",marker="*",
    label="{:1.1f}%   Minneapolis".format(MSPe),zorder=10,edgecolor="k",lw=0.5,
    transform=ccrs.PlateCarree())

ax.scatter(lon[Tmin[1]],lat[Tmin[0]],100,c="lightgreen",marker="*",
    label="{:1.1f}%   Optimal".format(Tr.min()),zorder=10,edgecolor="k",lw=0.5,
    transform=ccrs.PlateCarree())

ax.text(SFOloc[1]+4,SFOloc[0]-4,"100%",color="w",rotation=-35,transform=ccrs.PlateCarree())
ax.text(-109.5,41,"90%",color="w",rotation=-45,transform=ccrs.PlateCarree())

ax.set_title("Optimal location of AGU Fall Meeting",loc="left",fontweight="bold")
ax.legend(loc=(0.1,0.65))
