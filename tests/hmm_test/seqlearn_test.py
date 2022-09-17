from seqlearn.perceptron import StructuredPerceptron



clf = StructuredPerceptron()
clf.fit(X_train, y_train, lengths_train)