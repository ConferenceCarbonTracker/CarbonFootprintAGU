import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from cmocean import cm as cmo
from matplotlib.colors import Normalize,LinearSegmentedColormap
%matplotlib qt

## read data
path = "~/git/CarbonFootprintAGU/"
df1 = pd.read_csv(path+"data/emissions_per_country.csv")
df2 = pd.read_csv(path+"data/emissions_per_state.csv")

ncountries = len(df1)
nstates = len(df2)

T = sum(df1["emissions [tCO2e]"])

## create colormap
vmax=20000
cmap = plt.get_cmap("plasma")

nstates_disp = nstates
nstates_text = 8
ncountries_disp = 12
yoffset = 50
sum_other_countries = sum(df1["emissions [tCO2e]"][ncountries_disp:])


# plotting
fig,ax = plt.subplots(1,1,figsize=(8,5))

ax.bar(0,sum(df2["emissions [tCO2e]"][nstates_disp:]),
    color=cmap(df1["emissions [tCO2e]"][0]/vmax),
    edgecolor="k")
for i in np.arange(nstates_disp)[::-1]:
    ax.bar(0,df2["emissions [tCO2e]"][i],
        bottom=sum(df2["emissions [tCO2e]"][i+1:]),
        color=cmap(df1["emissions [tCO2e]"][0]/vmax),
        edgecolor="k")

for i in np.arange(nstates_text)[::-1]:
    ax.text(-0.3,sum(df2["emissions [tCO2e]"][i+1:])+yoffset,df2["state"][i])

ax.bar(np.arange(1,ncountries_disp),df1["emissions [tCO2e]"][1:ncountries_disp],
        color=cmap(df1["emissions [tCO2e]"][1:ncountries_disp]/vmax),
        edgecolor="k")
ax.bar(ncountries_disp,sum_other_countries,color=cmap(sum_other_countries/vmax),
        edgecolor="k")

# percent on the top
for i in range(ncountries_disp):
    ax.text(i,df1["emissions [tCO2e]"][i]+yoffset,
        "{:d}%".format(int(round(df1["emissions [tCO2e]"][i]/T*100))),ha="center")

ax.text(ncountries_disp,sum_other_countries+yoffset,
    "{:d}%".format(int(round(sum_other_countries/T*100))),ha="center")

ax.set_xlim(-0.6,ncountries_disp+0.6)
ax.set_ylim(0,17e3)
ax.set_ylabel("tonnes of CO2e")

# xticks
country_strings = list(df1["country"][:ncountries_disp])+["All other\ncountries"]
country_strings[0] = "United\nStates"
country_strings[3] = "United\nKingdom"
country_strings[6] = "South\nKorea"
country_strings[11] = "Switzer\nland"
ax.set_xticks(np.arange(ncountries_disp+1))
ax.set_xticklabels(country_strings,rotation=90)

ax.set_title("Emissions per country",loc="left",fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
#ax.spines["bottom"].set_visible(False)
#plt.savefig(path+"plots/emissions_country.png",dpi=200)
