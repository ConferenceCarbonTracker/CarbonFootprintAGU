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

## get location of three hubs
LOC1 = geolocator.geocode("Chicago, USA",timeout=30)
loc1 = (LOC1.latitude,LOC1.longitude)

LOC2 = geolocator.geocode("Paris, France",timeout=30)
loc2 = (LOC2.latitude,LOC2.longitude)

LOC3 = geolocator.geocode("Beijing, China",timeout=30)
loc3 = (LOC3.latitude,LOC3.longitude)

# preallocate dist vectors
dists1 = np.empty(n_locs)
dists2 = np.empty(n_locs)
dists3 = np.empty(n_locs)

## calculate distances relative to airport specified by loc
for i in range(n_locs):
    n = df["N"][i]
    lat = df["lat"][i]
    lon = df["lon"][i]

    dists1[i] = distance.distance((lat,lon),loc1).km
    dists2[i] = distance.distance((lat,lon),loc2).km
    dists3[i] = distance.distance((lat,lon),loc3).km

T = 0
n_virtual = 0
for i in range(n_locs):
    n = df["N"][i]
    dist = min((dists1[i],dists2[i],dists3[i]))

    if dist < 400:       # BUS / TRAIN / CAR at 60gCO2e / km / person
        T += dist*2*n*0.06      # kgCO2e
    elif dist < 1500:    # SHORT HAUL FLIGHT at 200gCO2e / km / person
        T += dist*2*n*0.2
    elif dist < 4000:    # LONG HAUL FLIGHT at 250gCO2e / km / person
        T += dist*2*n*0.25
    else:                # Virtual participation
        #T += dist*2*n*0.3
        n_virtual += n

T_SFO = 69334
print(T/1000)
#print(n_virtual/24008)
