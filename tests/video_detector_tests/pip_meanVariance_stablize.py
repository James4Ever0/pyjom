import json

data = json.loads(open("pip_meanVariance.json",'r').read())


# print(len(data)) # 589
import numpy as np
data = np.array(data)
from pykalman import KalmanFilter

def Kalman1D(observations,damping=0.2):
    # To return the smoothed time series data
    observation_covariance = damping
    initial_value_guess = observations[0]
    transition_matrix = 1
    transition_covariance = 0.1
    initial_value_guess
    kf = KalmanFilter(
            initial_state_mean=initial_value_guess,
            initial_state_covariance=observation_covariance,
            observation_covariance=observation_covariance,
            transition_covariance=transition_covariance,
            transition_matrices=transition_matrix
        )
    pred_state, state_cov = kf.smooth(observations)
    return pred_state

xLeftPoints = data[:,0,1]
xLeftPointsFiltered = Kalman1D(xLeftPoints)
threshold = 20
xLeftPointSignal = 100*(abs(xLeftPointsFiltered - xLeftPoints) < threshold).astype(np.uint8)
print(xLeftPoints)
import matplotlib.pyplot as plt

plt.plot(xLeftPoints)
plt.plot(xLeftPointsFiltered)
plt.show()

