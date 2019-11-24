import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from cmocean import cm as cmo
import cartopy.io.shapereader as shpreader
from matplotlib.patches import Rectangle, Arrow
from matplotlib.collections import PatchCollection
%matplotlib qt

## read data
path = "~/git/CarbonFootprintAGU/data/"
df = pd.read_csv(path+"locations.csv")
n = len(df)

## Great circle, equi-distant projection
# higher resolution for great circles

SFOloc = (37.622452, -122.384071607814)

##
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.LambertConformal(central_longitude=180+SFOloc[1]))
ax.set_extent([-13, 36, 40, 64], crs=ccrs.Geodetic())

ax.add_feature(cfeature.OCEAN,facecolor="#4381a2",zorder=-2)
ax.add_feature(cfeature.LAND,facecolor="0.9")
ax.coastlines(resolution="50m")
ax.add_feature(cfeature.BORDERS,lw=0.5,alpha=1)
ax.add_feature(cfeature.LAKES,facecolor="#4381a2",zorder=0.1)

# rectangle to hide shetland
patch = [Rectangle((-3.5e6,3.8e6),2e5,2e5)]
p = PatchCollection(patch,facecolor="#4381a2",zorder=2)
ax.add_collection(p)

ax.text(0.5,0.92,"San Francisco",alpha=0.5,transform=ax.transAxes,ha="center",va="top")
parrow = [Arrow(-3.3e6,4.05e6,0,2e5,width=2e5)]
ax.add_collection(PatchCollection(parrow,color="lightgreen",alpha=0.9))

colr = "#D71455"
vmax = 0.9
nmax = df["N"].max()*0.2
cmap = plt.get_cmap("inferno_r")
ax.scatter(df["lon"],df["lat"],0.1+7*np.sqrt(df["N"]),
        c=cmap(((df["N"]/nmax)**(1/4))*vmax), transform=ccrs.Geodetic(),
        alpha=.9,edgecolor="k",lw=0.3,zorder=2)

# for legend
nums = [1,10,50,250]
for num in nums:
    ax.scatter(0,0,0.1+7*np.sqrt(num),c=[cmap(((num/nmax)**(1/4))*vmax)],
        label="{:d}".format(num),transform=ccrs.Geodetic(),edgecolor="k",lw=0.3)

ax.set_title("Attendees of AGU Fall Meeting 2019",loc="left",fontweight="bold")
plt.legend(loc=3,title="# of attendees")
