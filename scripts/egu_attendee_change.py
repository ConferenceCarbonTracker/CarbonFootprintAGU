import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
os.chdir("/Users/milan/git/CarbonFootprintAGU")

path = "data/egu"
filename = path+"/egu_attends.csv"

# save to npz
D = pd.read_csv(path+"/egu_attends.csv")

# to array
N = np.array(D.iloc[:,2:-1])
pop = np.array(D.iloc[:,1])
names = np.array(D.iloc[:,0])
hdi = np.array(D.iloc[:,-1])

all = N.sum(axis=0)
incr_all = ((all[1:]-all[:-1])/all[:-1]).mean()*100

hdi_low = N[hdi==0,:].sum(axis=0)/all*100
hdi_med = N[hdi==1,:].sum(axis=0)/all*100
hdi_hig = N[hdi==2,:].sum(axis=0)/all*100
hdi_vhi = N[hdi==3,:].sum(axis=0)/all*100

# remove countries with less than 5 participants
conly = (N > 0).all(axis=1)
N1 = N[conly,:]
names1 = names[conly]
hdi1 = hdi[conly]

# argsort by the total number of attendees over all years
sortargs = np.argsort(N1.sum(axis=1)/pop[conly])

N1 = N1[sortargs,:]
names1 = names1[sortargs]
hdi1 = hdi1[sortargs]

# mean relative annual change per country
diff = (N1[:,1:] - N1[:,:-1])/N1[:,:-1]
diffm = diff.mean(axis=1)
diffmax = diff.max(axis=1)
diffmin = diff.min(axis=1)

diffs = np.sort(diff,axis=1)*100

allyears = np.array([2012,2013,2014,2015,2016,2017,2018,2019])

## plotting
x = np.array(list(range(len(sortargs))))
fig,(ax0,ax) = plt.subplots(2,1,figsize=(8,8))

ax0.bar(allyears,hdi_vhi,color="C2",alpha=0.6,edgecolor="k",label="very high")
ax0.bar(allyears,hdi_hig,color="yellow",bottom=hdi_vhi,alpha=0.7,edgecolor="k",label="high")
ax0.bar(allyears,hdi_med,color="C1",bottom=hdi_hig+hdi_vhi,alpha=0.7,edgecolor="k",label="medium")
ax0.bar(allyears,hdi_low,color="C0",bottom=hdi_hig+hdi_vhi+hdi_med,alpha=0.7,edgecolor="k",label="low")

ax0.legend(loc=3,title="Human development")

ax.scatter(x[hdi1==0],diffm[hdi1==0]*100,40,"C0",alpha=0.7,edgecolor="k",label="low")
ax.scatter(x[hdi1==1],diffm[hdi1==1]*100,40,"C1",alpha=0.7,edgecolor="k",label="medium")
ax.scatter(x[hdi1==2],diffm[hdi1==2]*100,40,"yellow",alpha=0.7,edgecolor="k",label="high")
ax.scatter(x[hdi1==3],diffm[hdi1==3]*100,40,"C2",alpha=0.7,edgecolor="k",label="very high")

#ax.legend(loc=1,title="Human development",scatterpoints=3)

for i in range(len(sortargs)):
    ax.plot([x[i],x[i]],[diffs[i,1],diffs[i,-1]],"k",lw=0.4)


ax.plot([-0.5,len(sortargs)],[0,0],"k",lw=0.5)
ax.plot([-0.5,len(sortargs)],[incr_all,incr_all],"C0",lw=1,zorder=-4)

ax.set_xticks(list(range(len(pop))))
ax.set_xticklabels(names1,rotation=90,fontsize=8)

# ax.legend(loc=2)
ax0.set_title("a",loc="right",fontweight="bold")
ax.set_title("b",loc="right",fontweight="bold")

ax0.set_title("EGU attendees from less developed countries",loc="left")
ax.set_title("Change in attendees per country",loc="left")

ax.set_xlabel("countries, sorted by attendees per capita")
ax.set_ylabel("annual change in attendees [%]")
ax0.set_ylabel("share in attendees [%]")

ax.set_xlim(-0.5,len(sortargs)-0.5)
ax.set_ylim(-50,150)
ax0.set_ylim(70,100)

plt.tight_layout()
plt.show()
