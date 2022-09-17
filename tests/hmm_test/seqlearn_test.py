from seqlearn.perceptron import StructuredPerceptron


# the lengths_train marked each individual sequence's length as an array.

lengths_train = [1,1,2,1]

clf.fit(X_train, y_train, lengths_train)