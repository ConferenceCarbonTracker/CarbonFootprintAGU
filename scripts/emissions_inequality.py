import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

## read data
path = "git/CarbonFootprintAGU/"
df1 = pd.read_csv(path+"data/emissions_per_country.csv")
df2 = pd.read_csv(path+"data/emissions_per_state.csv")

ncountries = len(df1)
nstates = len(df2)

T = sum(df1["emissions [tCO2e]"])
N = sum(df1["N"])

## Sort by carbon emissions from lowest country/state to highest
emissions_c = np.array(df1["emissions [tCO2e]"])[1:]    # cut off USA
emissions_s = np.array(df2["emissions [tCO2e]"])
n_c = np.array(df1["N"])[1:]
n_s = np.array(df2["N"])
names_c = np.array(df1["country"])[1:]
names_s = np.array(df2["state"])

pc_emissions_c = np.array(df1["emissions_per_capita [tCO2e]"])[1:]
pc_emissions_s = np.array(df2["emissions_per_capita [tCO2e]"])

emissions = np.hstack((emissions_c,emissions_s))
pc_emissions = np.hstack((pc_emissions_c,pc_emissions_s))
numbers = np.hstack((n_c,n_s))
names = np.hstack((names_c,names_s))

# sort them
sortarg = np.argsort(pc_emissions)
emissions_sorted = emissions[sortarg]
numbers_sorted = numbers[sortarg]
names_sorted = names[sortarg]

ccarbon = np.array(np.cumsum(emissions_sorted))
cnumbers = np.array(np.cumsum(numbers_sorted))

ccarbonpercent = ccarbon/T*100
cnumpercent = cnumbers/N*100

# for rectangles
x = np.vstack((cnumpercent,cnumpercent)).flatten("F")
y1 = np.hstack((ccarbonpercent[0],np.vstack((ccarbonpercent[:-1],ccarbonpercent[:-1])).flatten("F"),ccarbonpercent[-1]))
y2 = np.hstack((ccarbonpercent[0],np.vstack((ccarbonpercent[1:],ccarbonpercent[1:])).flatten("F"),ccarbonpercent[-1]))

## change state names to Statename, USA
n_countries = [1,10,16,22,43,45,50,70,71,80,82,83,99,106,138]
names_sorted[1] = "California, USA"
names_sorted[10] = "Colorado, USA"
names_sorted[16] = "Texas, USA"
names_sorted[43] = "Maryland, USA"
names_sorted[45] = "New York, USA"
names_sorted[50] = "Massachussets, USA"
## PLOT
fig,ax = plt.subplots(1,1,figsize=(5.08,5))

# SCENARIO 1
i1 = 98
l1, = ax.plot([cnumpercent[i1],cnumpercent[i1]],[0,ccarbonpercent[i1]],"C0")
ax.plot([0,cnumpercent[i1]],[ccarbonpercent[i1],ccarbonpercent[i1]],"C0")
ax.text(cnumpercent[i1]+2,10,"{:d}%".format(int(round(100-cnumpercent[i1]))),color="C0")
ax.text(38,ccarbonpercent[i1]+1,"{:d}%".format(int(round(ccarbonpercent[i1]))),color="C0")
ax.arrow(cnumpercent[i1]+5,9,11.5,0,head_width=0.5,color="C0")
ax.arrow(cnumpercent[i1]+5.2,9,-4,0,head_width=0.5,color="C0")

# SCENARIO 2
i2 = 69
ax.plot([cnumpercent[i2],cnumpercent[i2]],[0,ccarbonpercent[i2]],"C2")
ax.plot([0,cnumpercent[i2]],[ccarbonpercent[i2],ccarbonpercent[i2]],"C2")
ax.text(cnumpercent[i2]+2,4,"{:d}%".format(int(round(100-cnumpercent[i2]))),color="C2")
ax.text(1,ccarbonpercent[i2]+1,"{:d}%".format(int(round(ccarbonpercent[i2]))),color="C2")
ax.arrow(cnumpercent[i2]+5,3,30.5,0,head_width=0.5,color="C2")
ax.arrow(cnumpercent[i2]+5.2,3,-4,0,head_width=0.5,color="C2")

# A FEW COUNTRIES NUMBERED
for n,j in enumerate(n_countries):
    ax.text(cnumpercent[j-1]+0.2, ccarbonpercent[j]+0.2,chr(97+n), fontsize=8,ha="right")

# RECTANGLES
ax.fill_between(x,y1,y2,alpha=0.3,color="k")

# LEGEND
countrynames = ["      {:s}".format(names_sorted[n]) for i,n in enumerate(n_countries)]
ax.legend([l1,]*len(countrynames),countrynames,title="Countries or states",loc=2,handlelength=0,fontsize=7)

for i,n in enumerate(n_countries):
    ax.text(4,91.4-3.535*i,chr(97+i),fontsize=7,color="k",zorder=10)


ax.set_xlim(0.0,100.0)
ax.set_ylim(0.0,100.0)

ax.set_title("Sorted carbon emissions",loc="left")

ax.set_xlabel("% of participants, sorted by per capita emission")
ax.set_ylabel("% of total emissions")

plt.tight_layout()
plt.show()
plt.savefig(path+"plots/emissions_inequality.png",dpi=200)
plt.close(fig)
