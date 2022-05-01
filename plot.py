import matplotlib.pyplot as plt
import numpy as np

t,R_P,R_Z,T_P,T_Z,T,U,I,C_p,C_V = np.genfromtxt("datendat-copy.csv", delimiter=",", skip_header=1, unpack=True)

C_V_kurz = C_V[np.where(T<160)]
T_kurz = T[np.where(T<160)]

print(C_V_kurz, T_kurz, T)
#
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
