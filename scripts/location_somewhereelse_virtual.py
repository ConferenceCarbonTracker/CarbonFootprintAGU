import cartopy.io.shapereader as shpreader
import shapely.geometry as sgeom
from shapely.ops import unary_union
from shapely.prepared import prep
from geopy.geocoders import Nominatim
from geopy import distance
import matplotlib.pyplot as plt
geolocator = Nominatim()
import pandas as pd
import numpy as np

## read data
pathfolder = "~/git/CarbonFootprintAGU/"
df = pd.read_csv(pathfolder+"data/locations.csv")
n_locs = len(df)

## get location of ANY AIRPORT
LOC = geolocator.geocode("Chicago, USA",timeout=30)
loc = (LOC.latitude,LOC.longitude)

# preallocate dist vector
dists = np.empty(n_locs)

## calculate distances relative to airport specified by loc
for i in range(n_locs):
    n = df["N"][i]
    lat = df["lat"][i]
    lon = df["lon"][i]

    dists[i] = distance.distance((lat,lon),loc).km

## set dists to zero for X% of virtual participants
sortarge = np.argsort(dists)
n_sorted = np.array(df["N"])[sortarge]
dist_sorted = np.array(dists)[sortarge]
N = np.sum(n_sorted)
dist17 = dist_sorted[np.where(np.cumsum(n_sorted)/N > (1-0.17))[0][0]]
dist36 = dist_sorted[np.where(np.cumsum(n_sorted)/N > (1-0.36))[0][0]]

dists[dists > dist36] = 0.0

T = 0
for i in range(n_locs):
    n = df["N"][i]
    dist = dists[i]

    if dist < 400:       # BUS / TRAIN / CAR at 60gCO2e / km / person
        T += dist*2*n*0.06      # kgCO2e
    elif dist < 1500:    # SHORT HAUL FLIGHT at 200gCO2e / km / person
        T += dist*2*n*0.2
    elif dist < 8000:    # LONG HAUL FLIGHT at 250gCO2e / km / person
        T += dist*2*n*0.25
    else:                # SUPER LONG HAUL at 300gCO2e / km / person
        T += dist*2*n*0.3

T_SFO = 69334
T/1000
