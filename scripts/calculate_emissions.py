import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

## read data
path = "git/CarbonFootprintAGU/data/"
df = pd.read_csv(path+"locations.csv")
nlocs = len(df)

## TOTAL

T = 0.0

for i in range(nlocs):
    n = df["N"][i]
    dist = df["dist"][i]
    
    if dist < 400:       # BUS / TRAIN / CAR at 60gCO2e / km / person
        T += dist*2*n*0.06      # kgCO2e
    elif dist < 1500:    # SHORT HAUL FLIGHT at 200gCO2e / km / person
        T += dist*2*n*0.2
    elif dist < 8000:    # LONG HAUL FLIGHT at 250gCO2e / km / person
        T += dist*2*n*0.25
    else:                # SUPER LONG HAUL at 300gCO2e / km / person
        T += dist*2*n*0.3
    
print("Total emissions: {:d} tCO2e".format(int(T/1000)))

n_total = sum(df["N"])
print("per capita emission: {:d} kgCO2e".format(int(T/n_total)))