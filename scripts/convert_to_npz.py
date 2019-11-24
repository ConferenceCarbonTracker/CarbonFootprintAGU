import numpy as np

pathfolder = "/Users/milan/git/CarbonFootprintAGU/"
txtin = open(pathfolder+"data/optimization/nohup.out")

lats = np.arange(20,86,1)
lons = np.arange(-180,180,1)

T = np.zeros(len(lats)*len(lons))

for i,line in enumerate(txtin.readlines()):
    if line[:5] == "Trace":
        break
    else:
        t = line.split(",")[1]
        T[i] = int(t[3:])

txtin.close()

T = T.reshape(len(lats),len(lons))
np.savez(pathfolder+"data/optimization/emissions_grid_fine.npz",lat=lats,lon=lons,T=T)
