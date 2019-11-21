import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd

## read data
path = "git/CarbonFootprintAGU/data/"
df = pd.read_csv(path+"locations_geolocated.csv")
n = len(df)

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
ax.scatter(df["lon"],df["lat"],0.2+3*np.sqrt(df["N"]),c=colr, transform=ccrs.Geodetic(), alpha=.6,edgecolor="k",lw=0.1)

# for legend
nums = [1,50,250,1000]
for num in nums:
    ax.scatter(0,-90,0.2+3*np.sqrt(num),c=colr,label="{:d}".format(num),transform=ccrs.Geodetic(),alpha=.6)

ax.set_title("Attendees of AGU Fall Meeting 2019",loc="left",fontweight="bold")
plt.legend(loc=4,title="# of participants")

plt.tight_layout()
plt.show()