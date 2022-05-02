import matplotlib.pyplot as plt
import numpy as np
import csv 
from uncertainties import ufloat
t,R_P,R_Z,T_P,T_Z,T,U,I,C_p,C_V = np.genfromtxt("datendat-copy.csv", delimiter=",", skip_header=1, unpack=True)

C_V_kurz = C_V[np.where(T<170)]
T_kurz = T[np.where(T<170)]

C_V_kurz= C_V_kurz[1:]
T_kurz = T_kurz[1:]
debyeFunc = np.genfromtxt("debyeFunktion", delimiter=",", unpack=True)

debyeFunc = debyeFunc[1:]

thetaT = []
for cv in C_V_kurz:
    idx = (np.abs(debyeFunc - cv)).argmin()
    thetaT.append(np.unravel_index(idx,debyeFunc.shape))

thetaT = np.array(thetaT)
thetaTs = np.array([float('.'.join(str(elem) for elem in thetaT[i])) for i in range(thetaT.shape[0])])

#Correct thetaT here

thetaD = thetaTs*T_kurz


#print(C_V_kurz[np.where(thetaTs==0)])

with open('C_v_und_T_neu.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['C_V', 'T', 'theta/T', 'theta'])
    rows = zip(C_V_kurz, T_kurz, thetaTs, np.around(thetaD,decimals=3))
    writer.writerows(rows)


print(np.mean(thetaD),np.std(thetaD, ddof=1) / np.sqrt(np.size(thetaD)))

print("Vergleich mit der Theorie")
print(ufloat(545.5, 58.6)/ufloat( 332.102,0) - 1 )
print(545.5/332 - 1)

print("Minimale Messung:")
print(np.amin(thetaD[np.where(thetaD!=0)]))
#x = np.linspace(0, 10, 1000)
#y = x ** np.sin(x)
#
#plt.subplot(1, 2, 1)
#plt.plot(x, y, label='Kurve')
#plt.xlabel(r'$\alpha \:/\: \si{\ohm}$')
#plt.ylabel(r'$y \:/\: \si{\micro\joule}$')
#plt.legend(loc='best')
#
#plt.subplot(1, 2, 2)
#plt.plot(x, y, label='Kurve')
#plt.xlabel(r'$\alpha \:/\: \si{\ohm}$')
#plt.ylabel(r'$y \:/\: \si{\micro\joule}$')
#plt.legend(loc='best')
#
## in matplotlibrc leider (noch) nicht möglich
#plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
#plt.savefig('build/plot.pdf')
