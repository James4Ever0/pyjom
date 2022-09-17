from seqlearn.perceptron import StructuredPerceptron


# the lengths_train marked each individual sequence's length as a array.

clf.fit(X_train, y_train, lengths_train)