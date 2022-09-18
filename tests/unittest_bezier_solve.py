import bezier
import numpy as np

skew = 0.2
nodes1 = np.asfortranarray([
    [x_start, 0.5+skew, 1.0],
    [y_start, 0.5-skew, 1.0],
])
curve1 = bezier.Curve(nodes1, degree=2)

# import seaborn
# seaborn.set()

axis = curve1.plot(num_pts=256)
import matplotlib.pyplot as plt
# plt.plot(axis)
plt.show()
# print(axis)