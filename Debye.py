import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from uncertainties import ufloat
#import seaborn as sns 

#sns.set(style="darkgrid")
#sns.set_palette("magma")
C_v, T, Theta_T, Theta_D= np.genfromtxt("C_v_und_T_neu.csv", delimiter=",", unpack=True)

#print(C_v, T, Theta_T)



plt.plot(C_v, Theta_D, 'k.')
plt.xlabel(r'$C_V \, / \, \mathrm{J} \, \mathrm{K}^{-1} \mathrm{mol}^{-1}$')
plt.ylabel(r'$\theta_D \, / \, \mathrm{K}$')
plt.tight_layout()
plt.savefig('build/Theta_C_V.pdf')

plt.clf()
plt.close()


#Plot 2 versuchen auszufriemeln
def gerade(x,a,m):
    return a*x+m

a = 2
b =1

T_oben = T[Theta_D > gerade(T,a,b)]
T_unten = T[Theta_D < gerade(T,a,b)]

Theta_oben = Theta_D[Theta_D > gerade(T,a,b)]
Theta_unten = Theta_D[Theta_D < gerade(T,a,b)]

params1, covariance_matrix = np.polyfit(T_oben, Theta_oben, deg=1, cov=True)
errors1 = np.sqrt(np.diag(covariance_matrix))

params2, covariance_matrix = np.polyfit(T_unten, Theta_unten, deg=1, cov=True)
errors2 = np.sqrt(np.diag(covariance_matrix))

plt.plot(T, gerade(T, *params1))
plt.plot(T, gerade(T, *params2))
print(params1)
print(errors1)

print(params2)
print(errors2)


plt.plot(T, Theta_D, 'k.', label='Messwerte')
plt.xlabel(r'$T \, / \, \mathrm{K}$')
plt.ylabel(r'$\theta_D \, / \, \mathrm{K}$')
plt.legend()
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

