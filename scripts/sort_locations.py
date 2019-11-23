import numpy as np

pathfolder = "/local/home/kloewer/agu/"
txt = open(pathfolder+"processed/all_authors.txt","r")
txtout = open(pathfolder+"processed/locations_sorted.txt","w")

all_locs = []

for line in txt.readlines():

    loc = line.split(",")[1:]
    loc = [s.strip() for s in loc][::-1]

    all_locs.append((", ".join(loc)).strip())

# SORT IT
all_locs = list(np.sort(all_locs))

# COUNT IT
locs = []
n_per_loc = []
j = 0

for i,loc in enumerate(all_locs[:-1]):
    j += 1
    if loc != all_locs[i+1]:
        locs.append(loc)
        n_per_loc.append(j)
        j = 0


for n,loc in zip(n_per_loc,locs):
    txtout.write(str(n)+", "+loc+"\n")

txtout.close()