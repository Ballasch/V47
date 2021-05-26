import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from uncertainties import ufloat

C_v, T, Theta_T = np.genfromtxt("C_v_und_T.dat", delimiter="     ", unpack=True)

#print(C_v, T, Theta_T)

#Theta_D/T in Theta_D umrechnen 
Theta_D = Theta_T * T

print(Theta_D)

plt.plot(C_v, Theta_D, 'rx')
plt.xlabel(r'$C_V \, / \, \mathrm{J} \, \mathrm{K}^{-1} \mathrm{mol}^{-1}$')
plt.ylabel(r'$\theta_D \, / \, \mathrm{K}$')
plt.tight_layout()
plt.savefig('Theta_C_V.pdf')

#Mitteln
Theta_D_gemittelt = 0

for x in range(11):
    Theta_D_gemittelt = Theta_D_gemittelt + Theta_D[x]

Theta_D_gemittelt = Theta_D_gemittelt / 11

#Mittelwertsfehler berechnen (Standartabweichung / sqrt(n))
err = 0
for x in range(11):
    err = (Theta_D_gemittelt - Theta_D[x])**2 + err
Theta_D_gemittelt_err = np.sqrt(err / (11**2 - 11))

Debye = ufloat(Theta_D_gemittelt, Theta_D_gemittelt_err)

print(Debye)