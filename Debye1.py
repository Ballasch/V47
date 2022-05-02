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
C_V_errors = [0.03119271, 0.03255349, 0.03394991, 0.0362609 , 0.03790259, 0.04021695,
 0.04278006, 0.04527483, 0.04786025, 0.05053832, 0.05349947, 0.05696226,
 0.06016075, 0.06453554, 0.06844944, 0.07251927, 0.07603303, 0.07916955,
 0.08139095, 0.08289583, 0.0846759 , 0.08700354, 0.08910948, 0.09152098,
 0.09370249, 0.09648035, 0.09988936, 0.10338248, 0.10756676, 0.11218379,
 0.11694257, 0.12251193, 0.1296578 , 0.13747074, 0.14525249, 0.15375821,
 0.16387861, 0.17494184, 0.18657949, 0.19737509, 0.20765965, 0.21836906,
 0.22843939, 0.2383254 , 0.24855969, 0.25915487, 0.27136601, 0.28276413,
 0.29456266, 0.30815529, 0.3244376 , 0.34220141, 0.36477027, 0.39115762,
 0.41738975, 0.44514769, 0.47552167, 0.50344912, 0.53059017, 0.55901606,
 0.5875663 , 0.61360129, 0.63803504, 0.66740301, 0.69091358, 0.71515827,
 0.74464549, 0.76900778, 0.8020468 , 0.84635469, 0.89456752, 0.94148317,
 1.00412178, 1.05599175, 1.10166918, 1.14684254, 1.1890677 , 1.23493647,
 1.27270035, 1.32126106, 1.37389875, 1.42038557, 1.4708424 , 1.52829176,
 1.59038787, 1.66930482, 1.74199327, 1.81390848, 1.89458736]
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