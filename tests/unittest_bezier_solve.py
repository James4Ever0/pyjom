import bezier
import numpy as np

skew = 0.2 # skew 
x_start, y_start = 0,0
x_end, y_end = 1,1
nodes1 = np.asfortranarray([
    [x_start, (x_end-x_start)+skew, x_end],
    [y_start, (y_end-y_start)-skew, y_end],
])
curve1 = bezier.Curve(nodes1, degree=2)

# import seaborn
# seaborn.set()

axis = curve1.plot(num_pts=256)
import matplotlib.pyplot as plt
# plt.plot(axis)
plt.show()
# print(axis)