from seqlearn.perceptron import StructuredPerceptron

from seqlearn.datasets import load_conll

clf = StructuredPerceptron()
clf.fit(X_train, y_train, lengths_train)