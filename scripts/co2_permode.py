import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

## read data
path = "../data/"
df = pd.read_excel(path+"data_processed.xlsx")

dist = np.array(df["Distance to Vienna"])
N = np.array(df["Numbers"])*np.array(df["Fraction"])
n = len(dist)

## SCENARIO REALISTIC
C1ic = sum([num*d*2*0.3 for num,d in zip(N,dist) if d >= 8000])/1000
C1lh = sum([num*d*2*0.25 for num,d in zip(N,dist) if d >= 1500 and d < 8000])/1000
C1sh = sum([num*d*2*0.2 for num,d in zip(N,dist) if d >= 700 and d < 1500])/1000
C1ra = sum([num*d*2*0.03 for num,d in zip(N,dist) if d < 700])/1000

## SCENARIO EUROPE BY RAIL
C2ic = sum([num*d*2*0.3 for num,d in zip(N,dist) if d >= 8000])/1000
C2lh = sum([num*d*2*0.25 for num,d in zip(N,dist) if d >= 1500 and d < 8000])/1000
C2sh = sum([num*d*2*0.03 for num,d in zip(N,dist) if d >= 700 and d < 1500])/1000
C2ra = sum([num*d*2*0.03 for num,d in zip(N,dist) if d < 700])/1000

C1v = [C1ic,C1lh,C1sh,C1ra]
C2v = [C2ic,C2lh,C2sh+C2ra]
C1 = sum(C1v)
C2 = sum(C2v)

## PLOT
cmap = matplotlib.cm.get_cmap('viridis')
colors = cmap(np.linspace(0,0.9,3))

fig,ax = plt.subplots(1,1,figsize=(10,3))

# REALISTIC

# wedges1, texts1, autotexts1 = ax1.pie([C1lh,C1sh,C1ra],labels=["Long-haul","Short-haul","Rail"],autopct="%.1f%%",colors=colors)
# plt.setp(autotexts1, size=8, weight="bold", color="white")
# ax1.axis('equal')
# ax1.set_title("a) Breakdown by mode of transport, total %d tC02e" % sum(S1),loc="left",weight="bold")
#
# # RAIL
# wedges2, texts2, autotexts2 = ax2.pie([C2lh,C2ra],labels=["Long-haul","Rail"],autopct="%.1f%%",colors=colors)
# plt.setp(autotexts2, size=8, weight="bold", color="white")
# ax2.axis('equal')
# ax2.set_title("b) All journeys <1500km by rail, total %d tC02e" % sum(S2),loc="left",weight="bold")

ax.barh(2,C1ic,color="C3",label="Super long-haul",edgecolor="k",alpha=0.9)
ax.barh(2,C1lh,left=C1ic,color="C1",label="Long-haul",edgecolor="k",alpha=0.9)
ax.barh(2,C1sh,left=C1ic+C1lh,color="C0",label="Short-haul",edgecolor="k",alpha=0.9)
ax.barh(2,C1ra,left=C1ic+C1lh+C1sh,color="C2",label="Rail",edgecolor="k",alpha=0.9)

ax.barh(1,C2ic,color="C3",edgecolor="k",alpha=0.9)
ax.barh(1,C2lh,left=C2ic,color="C1",edgecolor="k",alpha=0.9)
ax.barh(1,C2sh+C2ra,left=C2ic+C2lh,color="C2",edgecolor="k",alpha=0.9)

ax.text(C2*1.1,1,"-%.1f%%" % ((1-C2/C1)*100))

xs = 0
for x in C1v:
    ax.text(xs+200,2.25,"%2.1f%%" % (x/C1*100))
    xs = xs + x

xs = 0
for x in C2v:
    ax.text(xs+200,1.25,"%.1f%%" % (x/C2*100))
    xs = xs + x


ax.set_xlabel("Carbon emissions [tCO2e]")
ax.set_yticks([1,2])
ax.set_yticklabels(["EGU2019\nall travel\n<1500km by train","EGU 2019"])

ax.set_title("EGU 2019 emissions by mode of transport",loc="left")
ax.legend(loc=1)

ax.set_xlim(0,34000)

plt.tight_layout()
plt.show()
