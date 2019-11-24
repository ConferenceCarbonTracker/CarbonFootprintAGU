import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from cmocean import cm as cmo
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
%matplotlib qt

## read data
path = "~/git/CarbonFootprintAGU/data/"
df = pd.read_csv(path+"locations.csv")
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
ax.text(0,-5.01e6,"5,000km",**alignment,alpha=0.5)
ax.text(0,-10.02e6,"10,000km",**alignment,alpha=0.5)


ax.set_xlim(-1.6e7,1.8e7)
ax.set_ylim(-1.2e7,1.5e7)

# scatter locations
colr = "#D71455"
vmax = 0.9
nmax = df["N"].max()*0.7
cmap = plt.get_cmap("inferno_r")
ax.scatter(df["lon"],df["lat"],1+3*np.sqrt(df["N"]),
    c=cmap(0.1+((df["N"]/nmax)**(1/4))*vmax), transform=ccrs.Geodetic(),edgecolor="k",lw=0.4)

# for legend
nums = [1,10,50,250,1000]
for num in nums:
    ax.scatter(0,-90,1+3*np.sqrt(num),c=[cmap(0.1+((num/nmax)**(1/4))*vmax)],label="{:d}".format(num),transform=ccrs.Geodetic(),alpha=1,edgecolor="k",lw=0.5)

# add SF star
ax.scatter(SFOloc[0],SFOloc[1],100,c="lightgreen",marker="*",label="San Francisco",zorder=10,edgecolor="k",lw=0.5)

ax.set_title("Attendees of AGU Fall Meeting 2019",loc="left",fontweight="bold")
plt.legend(loc=4,title="# of attendees")
