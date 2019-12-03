import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import Normalize,LinearSegmentedColormap
%matplotlib qt

T_current = 69334
T_DC = T_current*0.924
T_Chicago = T_current*0.877
T_biennial = T_current/2
T_Cbiennial = T_Chicago/2
T_virt17 = T_current*0.61
T_virt36 = T_current*0.26
T_b_virt17 = T_virt17/2
T_b_virt36 = T_virt36/2
T_b_virt36_c = 12988.577128271321/2
T_3hub_virt = 14602.318453989634

T_virt36/T_current

Ts = np.array([T_current,
                T_DC,
                T_Chicago,
                T_virt17,
                T_biennial,
                T_Cbiennial,
                T_b_virt17,
                T_virt36,
                T_3hub_virt,
                T_b_virt36,
                T_b_virt36_c])/T_current*100

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
fs = 12
ax.text(0,5,"AGU 2019",color="w",rotation=90,ha="center",fontsize=fs)
ax.text(1,5,"AGU in Washington DC",color="w",rotation=90,ha="center",fontsize=fs)
ax.text(2,5,"AGU in Chicago",color="w",rotation=90,ha="center",fontsize=fs)
ax.text(3,5,"Virtual for 17%",color="w",rotation=90,ha="center",fontsize=fs)
ax.text(4,5,"Biennial",color="w",rotation=90,ha="center",fontsize=fs)
ax.text(5,5,"Biennial &\nin Chicago",color="w",rotation=90,ha="center",fontsize=fs)
ax.text(6,40,"Biennial &\n17% virtual",color="k",rotation=90,ha="center",fontsize=fs)
ax.text(7,40,"Virtual for 36%",color="k",rotation=90,ha="center",fontsize=fs)
ax.text(8,40,"Chicago, Seoul,\nParis & 5% virtual",color="k",rotation=90,ha="center",fontsize=fs)
ax.text(9,40,"Biennial &\n36% virtual",color="k",rotation=90,ha="center",fontsize=fs)
ax.text(10,40,"Biennial, 36% virtual\n& in Chicago",color="k",rotation=90,ha="center",fontsize=fs)

ax.set_ylabel("emissions [%] compared to 2019")
ax.set_title("Reduction scenarios",loc="left",fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
