import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
%matplotlib qt

## read data
path = "~/git/CarbonFootprintAGU/data/"
df = pd.read_csv(path+"locations.csv")
nlocs = len(df)

## TOTAL
emissions = np.empty(nlocs)              # total emissions per country

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

## bin them
d = np.arange(0,19000,500)
e_binned = np.empty(len(d)-1)

for i in range(len(d)-1):
    e_binned[i] = np.sum(e_sorted[np.logical_and(dist_sorted<d[i+1],dist_sorted>d[i])])

## plot

fig,ax = plt.subplots(1,1,figsize=(8,4))

ax.bar(np.arange(len(e_binned)),e_binned,alpha=0.8,edgecolor="k")

ax2 = ax.twinx()
ax.set_ylim(0,1e4)
T_SFO = 69334
ax2.set_ylim(0,1e4/T_SFO*100)
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
