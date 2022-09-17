from seqlearn.perceptron import StructuredPerceptron # it's like mini neural network.

# the lengths_train marked each individual sequence's length as an array.
import numpy as np
X_train = np.random.random((5,4)) # one-hot encoded? not? features=4
y_train = np.random.randint(0,5,(5,)) # the freaking label.

lengths_train = [1,1,2,1] # may i apologize. sum=5

clf.fit(X_train, y_train, lengths_train)