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

land_shp_fname = shpreader.natural_earth(resolution='50m',
                                       category='physical', name='land')

land_geom = unary_union(list(shpreader.Reader(land_shp_fname).geometries()))
land = prep(land_geom)

def is_land(x, y):
    return land.contains(sgeom.Point(x, y))

## read data
pathfolder = "/Users/milan/git/CarbonFootprintAGU/"
df = pd.read_csv(pathfolder+"data/locations.csv")
n_locs = len(df)

## get location of ANY AIRPORT
LOC = geolocator.geocode("IAD",timeout=30)
loc = (LOC.latitude,LOC.longitude)

# preallocate dist vector
dists = np.empty(n_locs)

## calculate distances relative to airport specified by loc
for i in range(n_locs):
    n = df["N"][i]
    lat = df["lat"][i]
    lon = df["lon"][i]

    dists[i] = distance.distance((lat,lon),loc).km

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
T/1000/T_SFO*100
