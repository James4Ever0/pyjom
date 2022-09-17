from seqlearn.perceptron import StructuredPerceptron # it's like mini neural network.

# the lengths_train marked each individual sequence's length as an array.
X_train = # one-hot encoded? not?

lengths_train = [1,1,2,1] # may i apologize.

clf.fit(X_train, y_train, lengths_train)