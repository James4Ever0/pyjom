import bezier
import numpy as np

nodes1 = np.asfortranarray([
    [0.0, 0.5, 1.0],
    [0.0, 0.5, 1.0],
])
curve1 = bezier.Curve(nodes1, degree=2)

# import seaborn
# seaborn.set()

axis = curve1.plot(num_pts=256)
import matplotlib.pyplot as plt
# plt.plot(axis)
plt.show()
# print(axis)