import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from cmocean import cm as cmo

## read data
path = "git/CarbonFootprintAGU/data/"
df = pd.read_csv(path+"locations_geolocated.csv")
n = len(df)

# read colormap
cpath = "/Users/milan/python/ScientificColourMaps5/"
lajolla = LinearSegmentedColormap.from_list("test",np.loadtxt(cpath+"lajolla/lajolla.txt"))
buda = LinearSegmentedColormap.from_list("test",np.loadtxt(cpath+"buda/buda.txt"))
hawaii = LinearSegmentedColormap.from_list("test",np.loadtxt(cpath+"hawaii/hawaii.txt"))
imola = LinearSegmentedColormap.from_list("test",np.loadtxt(cpath+"imola/imola.txt"))

## Great circle, equi-distant projection
# higher resolution for great circles
class AziEqui(ccrs.AzimuthalEquidistant):

    @property
    def threshold(self):
        return 1e3

SFOloc = (37.622452, -122.384071607814)

##
fig = plt.figure(figsize=(7.5,6))
proj = ccrs.AzimuthalEquidistant(central_latitude=SFOloc[0],central_longitude=SFOloc[1])
ax = fig.add_subplot(1,1,1,projection=proj)
ax.add_feature(cfeature.OCEAN,facecolor="#97BACD",zorder=-2)
ax.add_feature(cfeature.LAND,facecolor="white")
ax.add_feature(cfeature.COASTLINE,lw=1,alpha=0.2)
ax.add_feature(cfeature.BORDERS,lw=0.1,alpha=1)
ax.gridlines(color="#86A9BC",zorder=-1)

ax.set_xlim(-1.6e7,1.8e7)
ax.set_ylim(-1.2e7,1.5e7)

colr = "#D71455"
ax.scatter(df["lon"],df["lat"],0.2+3*np.sqrt(df["N"]),c=df["N"]**(1/6), transform=ccrs.Geodetic(), cmap=cmo.thermal,alpha=1,edgecolor="k",lw=0.1)

# for legend
nums = [1,50,250,1000]
for num in nums:
    ax.scatter(0,-90,0.2+3*np.sqrt(num),c=cmo.thermal(256*num**(1/6)/800),label="{:d}".format(num),transform=ccrs.Geodetic(),alpha=1,edgecolor="k",lw=0.1)
    
ax.scatter(SFOloc[0],SFOloc[1],80,c="lightgreen",marker="*",label="San Francisco",zorder=10,edgecolor="w",lw=0.5)

ax.set_title("Attendees of AGU Fall Meeting 2019",loc="left",fontweight="bold")
plt.legend(loc=4,title="# of participants")

plt.tight_layout()
plt.show()