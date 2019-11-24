import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
%matplotlib qt

## read data
path = "~/git/CarbonFootprintAGU/data/"
df = pd.read_csv(path+"locations.csv")
nlocs = len(df)

## TOTAL
emissions = np.empty(nlocs)              # total emissions per location

for i in range(nlocs):
    n = df["N"][i]
    dist = df["dist"][i]

    if dist < 400:       # BUS / TRAIN / CAR at 60gCO2e / km / person
        e = dist*2*n*0.06      # kgCO2e
    elif dist < 1500:    # SHORT HAUL FLIGHT at 200gCO2e / km / person
        e = dist*2*n*0.2
    elif dist < 8000:    # LONG HAUL FLIGHT at 250gCO2e / km / person
        e = dist*2*n*0.25
    else:                # SUPER LONG HAUL at 300gCO2e / km / person
        e = dist*2*n*0.3

    emissions[i] = e


## sort them
sortarg = np.argsort(np.array(df["dist"]))
e_sorted = np.array(emissions)[sortarg][::-1]/1000  # tCO2e
dist_sorted = np.array(df["dist"])[sortarg][::-1]

sortarge = np.argsort(emissions/np.array(df["N"]))
n_sorted = np.array(df["N"])[sortarge]
dist_sorted_e = np.array(df["dist"])[sortarge]
N = np.sum(n_sorted)
dist17 = dist_sorted_e[np.where(np.cumsum(n_sorted)/N > (1-0.17))[0][0]]
dist36 = dist_sorted_e[np.where(np.cumsum(n_sorted)/N > (1-0.36))[0][0]]

## bin them
dx=500
d = np.arange(0,19000,dx)
e_binned = np.empty(len(d)-1)

for i in range(len(d)-1):
    e_binned[i] = np.sum(e_sorted[np.logical_and(dist_sorted<d[i+1],dist_sorted>d[i])])

## plot

fig,ax = plt.subplots(1,1,figsize=(8,4))

ax.axvline(x=dist17/dx-0.5,color="k",alpha=.5)
ax.axvline(x=dist36/dx-0.5,color="k",alpha=.5)

R1 = Rectangle((dist17/dx-0.5,0),25,11e3)
R2 = Rectangle((dist36/dx-0.5,0),25,11e3)
ax.add_collection(PatchCollection([R1,R2],alpha=.1,facecolor="C2"))
ax.text(dist17/dx-0.3,1e4,"17% of attendees")
ax.text(dist36/dx-0.3,1e4,"36%")

ax.bar(np.arange(len(e_binned)),e_binned,alpha=0.8,edgecolor="k")

ax2 = ax.twinx()
ax.set_ylim(0,11e3)
T_SFO = 69334
ax2.set_ylim(0,11e3/T_SFO*100)
ax2.set_ylabel("share of total emissions [%]")

every_n = 5
xtiks = np.arange(0,len(e_binned)-1,every_n)-0.5
xtiks[0] = 0.5
ax.set_xticks(xtiks)
ax.set_xticklabels(["{:d}km".format(d[1])]+["{:d}km".format(dd) for dd in d[every_n:-1:every_n]])
ax.set_xlim(-0.5,len(d)-1)

ax.set_title("Emissions per distance",loc="left",fontweight="bold")
ax.set_ylabel("emissions [tCO2e]")
ax.set_xlabel("Distance travelled")

plt.tight_layout()
