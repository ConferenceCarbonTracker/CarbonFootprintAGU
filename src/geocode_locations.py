from geopy.geocoders import Nominatim
from geopy import distance
import matplotlib.pyplot as plt
geolocator = Nominatim()

## read data
pathfolder = "/Users/milan/git/CarbonFootprintAGU/"
txt = open(pathfolder+"data/locations_sorted_m.csv","r")
txtout = open(pathfolder+"data/locations_geolocated.csv","w")

txtout.write("N,country,state,city,lat,lon,dist\n")

## get location of SFO
SFO = geolocator.geocode("SFO",timeout=30)
SFOloc = (SFO.latitude,SFO.longitude)

## get locations from openstreet map database
for i,line in enumerate(txt.readlines()):

    linesplit = line.split(",")

    n = linesplit[0]                # number of participants per location
    country = linesplit[1].strip()  # get country
    if len(linesplit) == 4:         # some locations have a state code
        state = linesplit[2].strip()
        city = linesplit[3].strip()
        geostring = " ,".join([city,state,country])
    else:
        city = linesplit[2].strip()
        state = ""
        geostring = " ,".join([city,country])

    try:
        loc = geolocator.geocode(geostring,timeout=30)
        lat = loc.latitude
        lon = loc.longitude
        dist = distance.distance((lat,lon),SFOloc).km

    except:
        print("ERROR: Geolocation failed.")
        lat = 0.0
        lon = 0.0
        dist = -1.0

    outstring = ",".join([n,country,state,city,str(lat),str(lon),str(dist)])

    print(outstring)
    txtout.write(outstring+"\n")
    plt.pause(1)

txtout.close()