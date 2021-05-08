import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from uncertainties import ufloat

T = [70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300]
alpha = [7, 8.5, 9.75, 10.7, 11.5, 12.1, 12.65, 13.15, 13.6, 13.9, 14.25, 14.5, 14.75, 14.95, 15.2, 15.4, 15.6, 15.75, 15.9, 16.1, 16.25, 16.35, 16.5, 16.65]

#Regression mit Polynom 4. Grades
def poly4(x, a, b, c, d, e):
    return a * x**4 + b * x**3 + c * x**2 + d * x + e

params, covariance_matrix = curve_fit(poly4, T, alpha, p0=(1, 1, 1, 1, 1))
uncertainties = np.sqrt(np.diag(covariance_matrix))
for name, value, uncertainty in zip('abcde', params, uncertainties):
    print(f'{name} = {value:8.12f} +- {uncertainty:.12f}')

x_plot = np.linspace(65, 310, 1000)

plt.plot(T, alpha, 'rx')
plt.plot(x_plot, params[0]*x_plot**4 + params[1]*x_plot**3 + params[2]*x_plot**2 + params[3]*x_plot + params[4], 'b-', label=r'Regression', linewidth=1)
plt.xlabel(r'$T \, / \, \mathrm{K}$')
plt.ylabel(r'$\alpha \, / \, 10^{-6} \, \mathrm{grd}^{-1}$')
plt.legend()
plt.tight_layout()
plt.savefig('alpha.pdf')

#Ergebnis:
#a = (-8,2 +- 0,7) * 10^-9
#b = (7,4 +- 0,5) * 10^-6
#c = (-2,5 +- 0,1) * 10^-3
#d = 0,41 +- 0,02
#e = -11,3 +- 0,6