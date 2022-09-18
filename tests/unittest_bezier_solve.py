import bezier

nodes1 = np.asfortranarray([
    [0.0, 0.5, 1.0],
    [0.0, 1.0, 0.0],
])
curve1 = bezier.Curve(nodes1, degree=2)

curve1.locate()

import matplotlib.pyplot as plt
plt.plot(curve1)
plt.show()