import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import Normalize,LinearSegmentedColormap
%matplotlib qt

T_current = 69334
T_DC = 60000
T_optimloc = 55000
T_biennial = T_current/2
T_virt17 = T_current*0.61
T_virt36 = T_current*0.26
T_b_virt17 = T_virt17/2
T_b_virt36 = T_virt36/2

Ts = np.array([T_current,T_DC,T_optimloc,T_biennial,
                T_virt17,T_virt36,T_b_virt17,T_b_virt36])/T_current*100

cpath = "/Users/milan/python/ScientificColourMaps5/"
hawaii = LinearSegmentedColormap.from_list("test",np.loadtxt(cpath+"hawaii/hawaii.txt"))

vmax=100
cmap = hawaii.reversed()

fig,ax = plt.subplots(1,1,figsize=(8,4))

ax.bar(np.arange(len(Ts)),Ts,color=cmap(Ts/vmax),alpha=0.9,edgecolor="k")

yoffset=0.5
for i in range(1,len(Ts)):
    ax.text(i,Ts[i]+yoffset,"-{:d}%".format(int(round(100-Ts[i]))),ha="center")

ax.set_xticks([])
ax.text(0,5,"AGU 2019",color="w",rotation=90,ha="center",fontsize=16)
ax.text(1,5,"AGU in Washington DC",color="w",rotation=90,ha="center",fontsize=16)
ax.text(2,5,"in optimal location",color="w",rotation=90,ha="center",fontsize=16)
ax.text(3,5,"Biennial",color="w",rotation=90,ha="center",fontsize=16)
ax.text(4,5,"Virtual for\n17% attendees",color="w",rotation=90,ha="center",fontsize=16)
ax.text(5,35,"Virtual for\n36% attendees",color="k",rotation=90,ha="center",fontsize=16)
ax.text(6,40,"Biennial and\n17% virtual",color="k",rotation=90,ha="center",fontsize=16)
ax.text(7,40,"Biennial and\n36% virtual",color="k",rotation=90,ha="center",fontsize=16)

ax.set_ylabel("emissions [%] compared to 2019")
ax.set_title("Reduction scenarios",loc="left",fontweight="bold")
plt.tight_layout()
