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

# remove countries with no participants in any year
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
diffm = np.mean(diff,axis=1)
diffp10 = np.percentile(diff,10,axis=1)*100
diffp90 = np.percentile(diff,90,axis=1)*100

allyears = np.array([2012,2013,2014,2015,2016,2017,2018,2019])
# slope = np.zeros(len(sortargs))
# A = np.vstack([allyears, np.ones(len(allyears))]).T
#
# for i in range(len(sortargs)):
#     slope[i],_ = np.linalg.lstsq(A,N1[i,:],rcond=None)[0]

clow = "#ed8a00"
cmed = "#e8e42e"
chig = "#7dd8a0"
cvhi = "C0"
w = 0.2

## plotting
x = np.array(list(range(len(sortargs))))
fig,(ax0,ax) = plt.subplots(2,1,figsize=(8,8))

ax0.bar(allyears-1.5*w,hdi_low,width=w,color=clow,alpha=1.0,edgecolor="k",label="low")
ax0.bar(allyears-w/2,hdi_med,width=w,color=cmed,alpha=0.9,edgecolor="k",label="medium")
ax0.bar(allyears+w/2,hdi_hig,width=w,color=chig,alpha=0.9,edgecolor="k",label="high")
ax0.bar(allyears+1.5*w,hdi_vhi,width=w,color=cvhi,alpha=0.8,edgecolor="k",label="very high")

for i in range(len(allyears)):
    ax0.text(allyears[i]-1.5*w,0.5+hdi_low[i],"%.1f%%" % hdi_low[i],rotation=90,ha="center")
    ax0.text(allyears[i]-w/2,0.5+hdi_med[i],"%.1f%%" % hdi_med[i],rotation=90,ha="center")
    ax0.text(allyears[i]+w/2,0.5+hdi_hig[i],"%i%%" % hdi_hig[i],rotation=90,ha="center")
    ax0.text(allyears[i]+3*w/2+0.025,12.5,"%i%%" % hdi_vhi[i],rotation=90,ha="center")

ax0.legend(loc=2)

ax.scatter(x[hdi1==0],diffm[hdi1==0]*100,40,clow,alpha=1.0,edgecolor="k",label="low")
ax.scatter(x[hdi1==1],diffm[hdi1==1]*100,40,cmed,alpha=1.0,edgecolor="k",label="medium")
ax.scatter(x[hdi1==2],diffm[hdi1==2]*100,40,chig,alpha=1.0,edgecolor="k",label="high")
ax.scatter(x[hdi1==3],diffm[hdi1==3]*100,40,cvhi,alpha=1.0,edgecolor="k",label="very high")

ax.legend(loc=1,title="Human\ndevelopment\nindex",scatterpoints=3)

# error bars
for i in range(len(sortargs)):
    ax.plot([x[i],x[i]],[diffp10[i],diffp90[i]],"k",lw=0.7)


ax.plot([-0.5,len(sortargs)],[0,0],"k",lw=0.5)
ax.plot([-0.5,len(sortargs)],[incr_all,incr_all],"k--",lw=2,zorder=-4)
ax.text(0,8,"Average %i%%" % int(round(incr_all)),color="k",fontweight="bold")

ax.set_xticks(list(range(len(pop))))
ax.set_xticklabels(names1,rotation=90,fontsize=8)
ax0.set_xticks(allyears)

# ax.legend(loc=2)
ax0.set_title("a",loc="right",fontweight="bold")
ax.set_title("b",loc="right",fontweight="bold")

ax0.set_title("EGU attendees by human development index",loc="left")
ax.set_title("Change in attendees per country",loc="left")

# ax.set_xlabel("countries, sorted by attendees per capita")
ax.set_ylabel("annual change in attendees [%]")
ax0.set_ylabel("share in attendees [%]")

ax.set_xlim(-0.5,len(sortargs)-0.5)
ax.set_ylim(-40,140)
ax0.set_ylim(0,14)
ax0.set_xlim(2010.5,2019.5)

plt.tight_layout()
plt.savefig("plots/egu_attendees.png",dpi=200)
plt.savefig("plots/egu_attendees.pdf")
plt.close(fig)
