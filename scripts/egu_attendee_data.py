import pandas as pd
import numpy as np
import os
os.chdir("/Users/milan/git/CarbonFootprintAGU")

path = "data/egu"
filename = path+"/egu_allyears.xlsx"
allyears = [2012,2013,2014,2015,2016,2017,2018,2019]
allcountries_doubles = []

for year in allyears:
    sheet = pd.read_excel("data/egu/egu_allyears.xlsx",sheet_name=str(year))
    countries = list(sheet.iloc[0:,0])

    for i in range(len(countries)):
        countries[i] = countries[i].strip()

    allcountries_doubles.extend(countries)

allcountries = list(set(allcountries_doubles))
allcountries.sort()
ncountries = len(allcountries)
ncountries

# preallocate
attendees = np.zeros((ncountries,len(allyears)),dtype=np.int)

for i,year in enumerate(allyears):
    sheet = pd.read_excel("data/egu/egu_allyears.xlsx",sheet_name=str(year))

    countries = list(sheet.iloc[0:,0])
    n = list(sheet.iloc[0:,1])

    for j,c in enumerate(countries):
        attendees[allcountries.index(c.strip()),i] = n[j]

# change some country names manually
allcountries[allcountries.index("Bolivia, Plurinational State Of")] = "Bolivia"
allcountries[allcountries.index("Congo, The Democratic Republic Of The")] = "Congo"
allcountries[allcountries.index("Iran, Islamic Republic Of")] = "Iran"
allcountries[allcountries.index("Korea, Democratic People's Republic Of")] = "North Korea"
allcountries[allcountries.index("Korea, Republic Of")] = "South Korea"
allcountries[allcountries.index("Macedonia, The Former Yugoslav Republic Of")] = "Macedonia"
allcountries[allcountries.index("Moldova, Republic Of")] = "Moldova"
allcountries[allcountries.index("Palestinian Territory, Occupied")] = "Palestine"
allcountries[allcountries.index("Tanzania, United Republic Of")] = "Tanzania"
allcountries[allcountries.index("Venezuela, Bolivarian Republic Of")] = "Venezuela"
allcountries[allcountries.index("Virgin Islands, British")] = "Virgin Islands"

## save to csv
csvout = open(path+"/egu_attends.csv","w",encoding="utf-8")
csvout.write("country, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019\n")
for i,country in enumerate(allcountries):
    csvout.write(country)
    for j in range(len(allyears)):
       csvout.write(", "+str(attendees[i,j]))

    csvout.write("\n")

csvout.close()

# save to npz
np.savez(path+"/egu_attends.npz",attendees=attendees)
