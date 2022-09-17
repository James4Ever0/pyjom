import numpy as np
from hmmlearn import hmm
# np.random.seed(42)

# hmmlearn is simply unsupervised learning.
# for supervised sequence learning use seqlearn instead

model = hmm.GaussianHMM(n_components=3, covariance_type="full")
# model.startprob_ = np.array([0.6, 0.3, 0.1])
# model.transmat_ = np.array([[0.7, 0.2, 0.1],
#                             [0.3, 0.5, 0.2],
#                             [0.3, 0.3, 0.4]])
# model.means_ = np.array([[0.0, 0.0], [3.0, -3.0], [5.0, 10.0]])
# model.covars_ = np.tile(np.identity(2), (3, 1, 1))
# not fitteed since we do not manually specify all the parameters.

X = np.random.random((100,8)) # it can be anything. the Z contains three labels.
# X, Z = model.sample(100)
# print(X) # the observations.
model.fit(X)
# # (100, 2)
Z_predicted = model.predict(X)
# print(Z) # the states.
print(X.shape, Z_predicted.shape)
# # (100,)
breakpoint()