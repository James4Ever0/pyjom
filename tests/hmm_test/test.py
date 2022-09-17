import numpy as np
from hmmlearn import hmm
np.random.seed(42)
model = hmm.GaussianHMM(n_components=3, covariance_type="full")
# model.startprob_ = np.array([0.6, 0.3, 0.1])
# model.transmat_ = np.array([[0.7, 0.2, 0.1],
#                             [0.3, 0.5, 0.2],
#                             [0.3, 0.3, 0.4]])
# model.means_ = np.array([[0.0, 0.0], [3.0, -3.0], [5.0, 10.0]])
# model.covars_ = np.tile(np.identity(2), (3, 1, 1))
# not fitteed since we do not manually specify all the parameters.
X, Z = model.sample(100)
print(X) # the observations.
# (100, 2)
print(Z) # the states.
# (100,)
breakpoint()