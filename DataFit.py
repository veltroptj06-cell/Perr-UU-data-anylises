#This script used the data extracted from main.py to determine the Temperature

import numpy as np
import matplotlib.pyplot as plt
import scipy.odr as odr

xass = np.array([0.0, 4e-06, 8e-06, 1.2e-05, 1.6e-05, 2.4e-05, 3.2e-05, 4.4e-05, 5.9999999999999995e-05, 7.999999999999999e-05, 0.000104, 0.00013199999999999998, 0.00017199999999999998, 0.00023999999999999998, 0.000308])*1
xerror = np.array([4e-07, 4e-07, 4e-07, 4e-07, 4e-07, 4e-07, 4e-07, 4e-07, 4e-07, 4e-07, 4e-07, 4e-07, 4e-07, 4e-07, 4e-07])*1

yass = [630.8125, 365.3125, 264.5625, 201.9375, 200.375, 139.5, 90.1875, 51.3125, 26.75, 11.6875, 4.1875, 2.0625, 1.0625, 0.75, 0.9375]
yerror = [16.662903220927618, 30.480975111534736, 14.928867798664438, 9.509657919715094, 8.652131240336105, 13.228756555322953, 10.841002894105323, 6.907593195172976, 8.011710179481033, 2.6860461183680373, 2.833256739160784, 1.6381678027601445, 0.5555121510822243, 0.4330127018922193, 0.899218410621135]

blanco = 0

Kb = 1.38e-23
d = 7.5e-7
g = 9.81
c = (np.pi*d*d*d*(1.05-0.997)*g*10*10*10)/(6*Kb)
def f(B, x):
    return yass[0]*np.exp(-c*x/B[0]) + blanco

B_start = [294, 650]

odr_model = odr.Model(f)

odr_data  = odr.RealData(xass,yass,sx=xerror,sy=yerror)

odr_obj   = odr.ODR(odr_data,odr_model,beta0=B_start)

odr_res   = odr_obj.run()

par_best = odr_res.beta
par_sig_ext = odr_res.sd_beta
par_cov = odr_res.cov_beta 
print(" De (INTERNE!) covariantiematrix  = \n", par_cov)
chi2 = odr_res.sum_square
print("\n Chi-squared         = ", chi2)
chi2red = odr_res.res_var
print(" Reduced chi-squared = ", chi2red, "\n")
odr_res.pprint()

xplot = np.linspace(np.min(xass),np.max(xass),num=100)

plt.plot(xplot,f(par_best,xplot),'r-',label="model")
plt.errorbar(xass, yass, yerr=yerror, fmt="ko", label="data")
plt.xlabel("Ticks")
plt.ylabel("Particle count")
plt.xlim(0, max(xass))
plt.ylim(0,max(yass))
plt.legend()
plt.show()
