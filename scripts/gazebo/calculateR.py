
import numpy as np, math
import pylab as plt

r = 100
a = np.linspace(0, 89, 10)

a0 = np.reshape( r*np.cos(a*np.pi/180), (-1,1))
a1 = np.reshape( r*np.sin(a*np.pi/180), (-1,1))

np.savetxt("r.txt", np.hstack([a0, r-a1]), fmt="%.3f")

plt.figure()
plt.plot(a0, r-a1)
plt.show()