import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp
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

t0, R_P, R_G, U0, I0 = np.genfromtxt("daten_neu.csv", delimiter=",", skip_header=3, unpack=True)

#Bei der Messung wurde der Komma falsch platziert. Dafür wird korrigiert
R_P = R_P*0.1
R_G = R_G*0.1

#Widerstände in Temperatur umrechnen und in K umrechnen
T_P = unp.uarray(0.00134 * (R_P * 1000)**2 + 2.296 * (R_P * 1000) - 243.02 + 273.15, 0)
T_G = unp.uarray(0.00134 * (R_G * 1000)**2 + 2.296 * (R_G * 1000) - 243.02 + 273.15, 0)

#Mittlere Temperatur zwischen Gefäß und Probe bestimmen
T_m = (T_P + T_G) / 2

#temporäre uArrays für t, T, U, I, alpha, C_p, C_v, C_v_plot, T_plot erstellen mit Fehler
err0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
err1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
err2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
t = unp.uarray(err0, err0)
T = unp.uarray(err0, err0)
U = unp.uarray(err0, err0)
I = unp.uarray(err0, err0)
alpha = unp.uarray(err0, err0)
C_p = unp.uarray(err1, err1)
C_v = unp.uarray(err1, err1)
C_v_plot = unp.uarray(err2, err2)
T_plot = unp.uarray(err2, err2)

#nur Temperaturen mit T<170K verwenden, also die ersten 15
for x in range(15):
    t[x] = t0[x]
    T[x] = T_m[x]
    U[x] = U0[x]
    I[x] = I0[x]

print(T)

#alpha bestimmen mit T
for x in range(15):
    alpha[x] = - ufloat(8.2, 0.7) * 10**-9 * T[x]**4 + ufloat(7.4, 0.5) * 10**-6 * T[x]**3 - ufloat(2.5, 0.1) * 10**-3 * T[x]**2 + ufloat(0.41, 0.02) * T[x] - ufloat(11.3, 0.6)

print(alpha)

#C_p bestimmen (Formel: U * I * delta_t * M / m / delta_T)
for x in range(14):
    C_p[x] = U[x] * I[x] * 10**-3 * (t[x+1] - t[x]) * 60 * M / m / (T[x+1] - T[x])

#C_v bestimmen
for x in range(14):
    C_v[x] = C_p[x] - 9 * (alpha[x+1] * 10**-6)**2 * k * 10**9 * T[x+1] * V

print(C_v)

#Die größten Ausreißer ausfiltern also Wert 4 und 5 raus aus den Arrays
for x in range(3):
    C_v_plot[x] = C_v[x]
    T_plot[x] = T[x]

for x in range(9):
    C_v_plot[x+3] = C_v[x+5]
    T_plot[x+3] = T[x+5]

print(C_v_plot, T_plot)

#lineare Regression
def lin(x, a, b):
    return a * x + b

params, covariance_matrix = curve_fit(lin, unp.nominal_values(C_v_plot), unp.nominal_values(T_plot), p0=(1, 1))
uncertainties = np.sqrt(np.diag(covariance_matrix))
for name, value, uncertainty in zip('ab', params, uncertainties):
    print(f'{name} = {value:8.12f} +- {uncertainty:.12f}')

x_plot = np.linspace(10, 29, 2)

plt.errorbar(unp.nominal_values(C_v_plot), unp.nominal_values(T_plot), xerr = unp.std_devs(C_v_plot), fmt='rx', label='Messwerte')
plt.plot(x_plot, params[0]*x_plot + params[1], 'b-', label=r'Regression', linewidth=1)
plt.xlabel(r'$C_v \, / \, \mathrm{J} \mathrm{Mol}^{-1} \mathrm{K}^{-1}$')
plt.ylabel(r'$T \, / \, \mathrm{K}$')
plt.legend()
plt.tight_layout()
plt.savefig('Debye.pdf')