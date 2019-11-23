import cartopy.io.shapereader as shpreader
import shapely.geometry as sgeom
from shapely.ops import unary_union
from shapely.prepared import prep
from geopy import distance
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

## get location via grid of points on the NH
lats = np.arange(30,75,5)
lons = np.arange(-180,180,10)

TT = np.zeros((len(lats),len(lons)))
npoints = np.prod(TT.shape)

k = 0
for i,x in enumerate(lats):
    for j,y in enumerate(lons):
        k += 1
        #if is_land(x,y):

        conference_location = (x,y)

        # preallocate dist vector
        dists = np.empty(n_locs)

        ## calculate distances relative to airport specified by loc
        for iloc in range(n_locs):
            ilat = df["lat"][iloc]
            ilon = df["lon"][iloc]

            dists[iloc] = distance.distance((ilat,ilon),conference_location).km

        T = 0
        for iloc in range(n_locs):
            n = df["N"][iloc]
            dist = dists[iloc]

            if dist < 400:       # BUS / TRAIN / CAR at 60gCO2e / km / person
                T += dist*2*n*0.06      # kgCO2e
            elif dist < 1500:    # SHORT HAUL FLIGHT at 200gCO2e / km / person
                T += dist*2*n*0.2
            elif dist < 8000:    # LONG HAUL FLIGHT at 250gCO2e / km / person
                T += dist*2*n*0.25
            else:                # SUPER LONG HAUL at 300gCO2e / km / person
                T += dist*2*n*0.3

        TT[i,j] = T
        #print("Sum of distances: {:d}".format(int(round(sum(dists)))))
        print("{:d}%, T={:d}".format(int(round(k/npoints*100)),int(round(T/1000))))

np.savez(pathfolder+"data/optimization/emissions_grid.npz",lat=lats,lon=lons,T=TT)
