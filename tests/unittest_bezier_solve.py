import bezier
import numpy as np

skew = -0.5  # skew: (-0.5,0.5) otherwise this shit will look ugly.
x_start, y_start = 0, 0
x_end, y_end = 1, 1

x_diff = x_end - x_start
y_diff = y_end - y_start

nodes1 = np.asfortranarray(
    [
        [x_start, x_diff * (0.5 + skew), x_end],
        [y_start, y_diff * (0.5 - skew), y_end],
    ]
)
curve1 = bezier.Curve(nodes1, degree=2)

# import seaborn
# seaborn.set()
test_case = 'evaluate':
if test_case == "plot"
    axis = curve1.plot(num_pts=256)
    import matplotlib.pyplot as plt

    # plt.plot(axis)
    plt.show()
elif test_case == "evaluate":
    print('type q to quit evaluation')
    while True:
        x = input("x> ")
        if x == 'q':
            print("quitting...")
        try:
            x = float(x)
            y = curve1.evaluate(x)
            print('point:',(x,y))
        except:
            print('ERROR: Invalid input value: %s' % x)
    # print(axis)
