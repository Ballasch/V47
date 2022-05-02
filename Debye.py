import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from uncertainties import ufloat
import seaborn as sns 

sns.set(style="darkgrid")
sns.set_palette("magma")
C_v, T, Theta_T, Theta_D= np.genfromtxt("C_v_und_T_neu.csv", delimiter=",", unpack=True)

#print(C_v, T, Theta_T)



plt.plot(C_v, Theta_D, 'k.')
plt.xlabel(r'$C_V \, / \, \mathrm{J} \, \mathrm{K}^{-1} \mathrm{mol}^{-1}$')
plt.ylabel(r'$\theta_D \, / \, \mathrm{K}$')
plt.tight_layout()
plt.savefig('build/Theta_C_V.pdf')

plt.clf()
plt.close()


plt.plot(T, Theta_D, 'k.')
plt.xlabel(r'$T \, / \, \mathrm{K}$')
plt.ylabel(r'$\theta_D \, / \, \mathrm{K}$')
plt.tight_layout()
plt.savefig('build/Theta_T.pdf')
# #Mitteln
# Theta_D_gemittelt = 0

# for x in range(11):
#     Theta_D_gemittelt = Theta_D_gemittelt + Theta_D[x]

# Theta_D_gemittelt = Theta_D_gemittelt / 11

# #Mittelwertsfehler berechnen (Standartabweichung / sqrt(n))
# err = 0
# for x in range(11):
#     err = (Theta_D_gemittelt - Theta_D[x])**2 + err
# Theta_D_gemittelt_err = np.sqrt(err / (11**2 - 11))

# Debye = ufloat(Theta_D_gemittelt, Theta_D_gemittelt_err)

# print(Debye)