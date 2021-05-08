import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from uncertainties import ufloat

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

t, R_P, R_G, U, I = np.genfromtxt("daten.dat", delimiter="	", unpack=True)

#Widerstände in Temperatur umrechnen und in K umrechnen
T_P = 0.00134 * (R_P * 1000)**2 + 2.296 * (R_P * 1000) - 243.02 + 273.15
T_G = 0.00134 * (R_G * 1000)**2 + 2.296 * (R_G * 1000) - 243.02 + 273.15

#Mittlere Temperatur zwischen Gefäß und Probe bestimmen
T = (T_P + T_G) / 2

print(T_P, T_G, T)

#alpha bestimmen mit T
alpha = -8.163 * 10**-9 * T**4 + 7.39 * 10**-6 * T**3 - 2.5293 * 10**-3 * T**2 + 0.40685 * T - 11.3349

print(alpha)

#temporäre Arrays für C_p, C_v und T_plot erstellen
C_p = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
C_v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
T_plot = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
C_v_plot = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#C_p bestimmen (Formel: U * I * delta_t * M / m / delta_T)
for x in range(31):
    C_p[x] = U[x] * I[x] * 10**-3 * (t[x+1] - t[x]) * 60 * M / m / (T[x+1] - T[x])

print(C_p)

#C_v bestimmen
for x in range(31):
    C_v[x] = C_p[x] - 9 * (alpha[x+1] * 10**-6)**2 * k * 10**9 * T[x+1] * V
#    T_plot[x] = T[x+1]

print(C_v)

#Die größten Ausreißer ausfiltern also Wert 4, 5, 21 raus aus den Arrays
#Für die ungefilterte Version Zeile 48 verwenden an Stelle von dem hier und die temporären Arrays vergrößern und in Zeile 72 C_v_plot durch C_v ersetzen
for x in range(3):
    C_v_plot[x] = C_v[x]
    T_plot[x] = T[x]

for x in range(15):
    C_v_plot[x+3] = C_v[x+5]
    T_plot[x+3] = T[x+5]

for x in range(10):
    C_v_plot[x+18] = C_v[x+21]
    T_plot[x+18] = T[x+21]

#3R Linie zu markieren
x_plot = np.linspace(75, 310, 2)
R_plot = [3* R, 3 * R]

#C_v gegen T plotten
plt.plot(x_plot, R_plot, 'b-', label='3R', linewidth=1)
plt.plot(T_plot, C_v_plot, 'rx', label='Messwerte')
plt.xlabel(r'$T \, / \, \mathrm{K}$')
plt.ylabel(r'$C_v \, / \, \mathrm{J} \mathrm{Mol}^{-1} \mathrm{K}^{-1}$')
plt.legend()
plt.tight_layout()
plt.savefig('C_v_gefiltert.pdf')