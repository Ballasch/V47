import csv

import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns
import uncertainties.unumpy as unp
from scipy.optimize import curve_fit
from uncertainties import ufloat

#sns.set(style="darkgrid")
#sns.set_palette("magma")
#Masse Probe in kg
m = 0.342
#Molmasse Kupfer in kg/mol
M = 0.06355
#Kompressionsmodul Kupfer in GPa
k = 140
#Molvolumen Kupfer in m^3/mol
V = 7.11 * 10**-6
#Universelle Gaskonstante
R = 8.31439

t, R_P, R_G, U, I = np.genfromtxt("daten_neu.csv", delimiter=",", skip_header=3, unpack=True,encoding='latin-1')
anzahlDaten = t.size
err0 = [0 for i in range(anzahlDaten)]

Ablesen = [0.1 for i in range(anzahlDaten)]

#Bei der Messung wurde der Komma falsch platziert. Dafür wird korrigiert
R_P = R_P*0.1
R_G = R_G*0.1
#Wir wollen übrigens Ohm, nicht Kiloohm haben. Nicht vergessen nachfolgend in Code anzupassen
R_P = R_P*1000
R_G = R_G*1000

R_P = unp.uarray(R_P, Ablesen)
R_G = unp.uarray(R_G, Ablesen)

#Widerstände in Temperatur umrechnen und in K umrechnen mit 0 als Fehler
T_P = 0.00134 * R_P**2 + 2.296 * R_P - 243.02 + 273.15
T_G = 0.00134 * R_G**2 + 2.296 * R_G  - 243.02 + 273.15

#Wieso? Warum gehen wir nicht einfach davon aus das die Widerstände falsch abgelesen wurden?
#T_P = unp.uarray(T_P, T_P*0.002)
#T_G = unp.uarray(T_G, T_G*0.002)

#Mittlere Temperatur zwischen Gefäß und Probe bestimmen
T = (T_P + T_G) / 2


#Mit Fehler für die Berechnung von C_P
#T2 = unp.uarray(T,0.002*T )
U2 = unp.uarray(U, Ablesen)
I2 = unp.uarray(I, Ablesen)
t2 = unp.uarray(t, 5)

#alpha bestimmen mit T
#alpha = - ufloat(8.2, 0.7) * 10**-9 * unp.nominal_values(T)**4 + ufloat(7.4, 0.5) * 10**-6 * unp.nominal_values(T)**3 - ufloat(2.5, 0.1) * 10**-3 * unp.nominal_values(T)**2 + ufloat(0.41, 0.02) * unp.nominal_values(T) - ufloat(11.3, 0.6)
alpha = - 8.2 * 10**-9 * unp.nominal_values(T)**4 + 7.4 * 10**-6 * unp.nominal_values(T)**3 - 2.5 * 10**-3 * unp.nominal_values(T)**2 +0.41 * unp.nominal_values(T) - 11.3

#temporäre uArrays für C_p, C_v und T_plot erstellen

C_p = unp.uarray(err0, err0)
C_v = unp.uarray(err0, err0)
#T_plot = unp.uarray(err0, err0)
#C_v_plot = unp.uarray(err0, err0)

#Zeitdifferenz ist ein fester Wert für uns
t_diff = 1.5
t_diff_fehler = ufloat(1.5,0.11785113019775792) #fehler resultiert aus +/- 5s Fehler bei der Zeitmessung
#C_p bestimmen (Formel: U * I * delta_t * M / m / delta_T)

for x in range(anzahlDaten-1):
    C_p[x] = U2[x] * I2[x] * 10**-3 * t_diff_fehler * 60 * M / m / (T_P[x+1] - T_P[x])




#C_v bestimmen
for x in range(anzahlDaten-1):
    C_v[x] = C_p[x] - 9 * (alpha[x+1] * 10**-6)**2 * k * 10**9 * T_P[x+1] * V
#    T_plot[x] = T[x+1]


writeTable = np.array([t,np.around(unp.nominal_values(R_P), decimals=4), np.around(unp.nominal_values(R_G), decimals=4), np.around(unp.nominal_values(T_P), decimals=3), np.around(unp.nominal_values(T_G), decimals=3), np.around(unp.nominal_values(T), decimals=3), np.around(U, decimals=3), np.around(I, decimals=3), np.around(unp.nominal_values(C_p), decimals=3), np.around(unp.nominal_values(C_v), decimals=3)])
with open('datendat-copy.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['t','R_P', 'R_Z', 'T_P', 'T_Z', 'T',  'U', 'I', 'C_p', 'C_V'])
    rows = zip(*writeTable)
    writer.writerows(rows)
with open('datendat-copy-cut1.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['t','R_P', 'R_Z', 'T_P', 'T_Z', 'T',  'U', 'I', 'C_p', 'C_V'])
    rows = zip(*writeTable[:,:31])
    writer.writerows(rows)
with open('datendat-copy-cut2.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['t','R_P', 'R_Z', 'T_P', 'T_Z', 'T',  'U', 'I', 'C_p', 'C_V'])
    rows = zip(*writeTable[:,31:62])
    writer.writerows(rows)
with open('datendat-copy-cut3.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['t','R_P', 'R_Z', 'T_P', 'T_Z', 'T',  'U', 'I', 'C_p', 'C_V'])
    rows = zip(*writeTable[:,62:-1])
    writer.writerows(rows)
#Die größten Ausreißer ausfiltern also Wert 4, 5, 21 raus aus den Arrays
#Für die ungefilterte Version Zeile 51 verwenden an Stelle von dem hier und in Zeile 39 err1 durch err0 2 mal ersetzen und in Zeile 75 C_v_plot durch C_v ersetzen
# for x in range(3):
#     C_v_plot[x] = C_v[x]
#     T_plot[x] = T[x]

# for x in range(15):
#     C_v_plot[x+3] = C_v[x+5]
#     T_plot[x+3] = T[x+5]

# for x in range(10):
#     C_v_plot[x+18] = C_v[x+21]
#     T_plot[x+18] = T[x+21]

#3R Linie zu markieren

C_v_plot = C_v[1:-1]
T_plot = T[1:-1]

x_plot = np.linspace(75, 310, 2)
R_plot = [3 * R, 3 * R]

print("Errors:")
print(unp.std_devs(C_v_plot))

def debye():
    return 0
def einstein():
    return 0
#C_v gegen T plotten
plt.plot(x_plot, R_plot, 'b-', label='3R', linewidth=1)
plt.errorbar(unp.nominal_values(T_plot), unp.nominal_values(C_v_plot), yerr = unp.std_devs(C_v_plot),fmt = "k.", label='Messwerte')
plt.xlabel(r'$T \, / \, \mathrm{K}$')
plt.ylabel(r'$C_V \, / \, \mathrm{J} \, \mathrm{K}^{-1} \mathrm{mol}^{-1}$')

plt.ylim(10,40)
plt.legend()
plt.tight_layout()
plt.grid()
plt.savefig('build/C_V_gefiltert.pdf')

plt.clf()
plt.close()


C_v_plot = C_v
T_plot = T
plt.plot(x_plot, R_plot, 'b-', label='3R', linewidth=1)
plt.errorbar(unp.nominal_values(T_plot), unp.nominal_values(C_v_plot), 
             yerr = unp.std_devs(C_v_plot),fmt = "k.", elinewidth=0.5, label='Messwerte')
plt.xlabel(r'$T \, / \, \mathrm{K}$')
plt.ylabel(r'$C_V \, / \, \mathrm{J} \, \mathrm{K}^{-1} \mathrm{mol}^{-1}$')

#plt.ylim(10,32)
plt.ylim(10,32)
plt.xlim(75,310)
plt.legend(loc='lower right')
plt.grid()
plt.tight_layout()

plt.savefig('build/C_V.pdf')
