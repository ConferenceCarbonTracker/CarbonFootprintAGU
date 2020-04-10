import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
os.chdir("/Users/milan/git/CarbonFootprintAGU")

path = "data/egu"
filename = path+"/egu_attends.csv"

# save to npz
D = pd.read_csv(path+"/egu_attends.csv")

# to array
N = np.array(D.iloc[:,2:])
pop = np.array(D.iloc[:,1])

# scientists per million inhabitants
scientist_density = (N.T/pop).T

SDs = np.sort(scientist_density,axis=0)
SDsum = np.sum(scientist_density,axis=0)
SDa = np.cumsum(SDs/SDsum,axis=0)
SDa.shape

## plotting
fig,ax = plt.subplots(1,figsize=(8,6))
for i in range(8):
    ax.plot(SDa[:,i],label=str(2012+i))

ax.plot([0,len(pop)-1],[0,1],"k")

ax.set_xticks(list(range(len(pop))))
ax.set_xticklabels([])

ax.legend(loc=2)
ax.set_title("Conference country inequality",loc="left")
ax.set_xlabel("countries, sorted")
ax.set_ylabel("cumulative attendee density")

ax.set_xlim(0,len(pop)-1)
ax.set_ylim(0,1)

plt.tight_layout()
plt.show()
