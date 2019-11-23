import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from cmocean import cm as cmo
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection

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
ax.add_feature(cfeature.BORDERS,lw=0.2)

# background image
ax.stock_img()

# circles
patches = []
patches.append(Circle((0, 0), 5e6))     # 5000km 
patches.append(Circle((0, 0), 1e7))     # 10000km
p = PatchCollection(patches, alpha=.5, facecolor="none",edgecolor="k",lw=0.5)
#p.set_array(np.array(colors))
ax.add_collection(p)

# text of circles
alignment = {'ha': 'center', 'va': 'top'}
ax.text(0,-5.01e6,"5000km",**alignment,alpha=0.5)
ax.text(0,-10.02e6,"10000km",**alignment,alpha=0.5)


ax.set_xlim(-1.6e7,1.8e7)
ax.set_ylim(-1.2e7,1.5e7)

# scatter locations
colr = "#D71455"
ax.scatter(df["lon"],df["lat"],1+3*np.sqrt(df["N"]),c=df["N"]**(1/6), transform=ccrs.Geodetic(), cmap=cmo.thermal,alpha=1,edgecolor="k",lw=0.1)

# for legend
nums = [1,50,250,1000]
for num in nums:
    ax.scatter(0,-90,1+3*np.sqrt(num),c=[cmo.thermal(256*num**(1/6)/800)],label="{:d}".format(num),transform=ccrs.Geodetic(),alpha=1,edgecolor="k",lw=0.5)
    
# add SF star
ax.scatter(SFOloc[0],SFOloc[1],100,c="lightgreen",marker="*",label="San Francisco",zorder=10,edgecolor="k",lw=0.5)

ax.set_title("Attendees of AGU Fall Meeting 2019",loc="left",fontweight="bold")
plt.legend(loc=4,title="# of attendees")

plt.tight_layout()
plt.show()