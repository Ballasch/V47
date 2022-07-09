import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp
from scipy.optimize import curve_fit
from uncertainties import ufloat

from Molwaerme import C_v_plot, T_plot

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

t,R_P,R_Z,T_P,T_Z,T,U,I,C_p,C_V = np.genfromtxt("datendat-copy.csv", delimiter=",", skip_header=1, unpack=True)



#lineare Regression
def lin(x, a, b):
    return a * x + b

C_v_plot = C_V[1:-3]
T_plot = T[1:-3]
C_V_errors = [ 2.3759751 ,  2.42813742,  3.36137916,  1.0209231,  14.00988915 , 2.00005113,
  3.61880335 , 3.67189906 , 3.72519378 , 3.77254542 , 2.81410367,  3.88399979,
  3.9374189  , 3.98766878 , 2.9700941  , 3.01276893 , 4.15408462,  3.09239346,
  2.40307664 , 6.2210062  , 4.37037402 , 3.24867736 , 6.43711451,  4.51345637,
  6.5596337  , 4.60198298 , 4.64825438 , 6.7588135  , 6.81940346,  4.77880148,
  4.82483829 , 2.74626315 , 2.88973586 , 3.62509861 , 3.67910918,  4.71661652,
  2.13238132 , 2.85077623 , 2.90714169 , 3.51649487 , 3.57299114,  3.05412756,
  3.6885325  , 3.74481963 , 3.1954979  , 3.68936504 , 2.91922775,  4.02871722,
  4.08763808 , 4.14652816 , 4.20334656 , 5.0618903  , 5.12610647,  4.3669641,
  4.42392625 , 4.48090089 , 3.87678906 , 4.60165967 , 5.53040448,  4.02841225,
  4.08157001 , 4.83506532 , 7.00518848 , 4.22489996 , 5.92975298,  5.98991908,
  5.10531373 , 7.38116278 , 6.17424833 , 6.23612109 , 7.59298194,  7.65980073,
  5.42228545 , 5.48219084 , 5.54138627 , 5.60064546 , 5.66230025,  5.72196227,
  8.21039688 , 6.88456653 , 6.94854172 , 8.42862708 , 8.49621785,  7.13409953,
  8.64029844 , 8.75644949 , 8.82805989 , 8.90409412 , 6.38629967]
params, covariance_matrix = curve_fit(lin, unp.nominal_values(C_v_plot), unp.nominal_values(T_plot), p0=(1, 1))
uncertainties = np.sqrt(np.diag(covariance_matrix))
for name, value, uncertainty in zip('ab', params, uncertainties):
    print(f'{name} = {value:8.12f} +- {uncertainty:.12f}')

x_plot = np.linspace(10, 29, 2)

plt.errorbar(unp.nominal_values(C_v_plot), unp.nominal_values(T_plot), xerr = C_V_errors, fmt='rx', label='Messwerte')
plt.plot(x_plot, params[0]*x_plot + params[1], 'b-', label=r'Regression', linewidth=1)
plt.xlabel(r'$C_v \, / \, \mathrm{J} \mathrm{Mol}^{-1} \mathrm{K}^{-1}$')
plt.ylabel(r'$T \, / \, \mathrm{K}$')
plt.legend()
plt.tight_layout()
plt.savefig('build/Debye.pdf')