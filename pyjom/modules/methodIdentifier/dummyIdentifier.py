def dummyId():
    import uuid

    return uuid.uuid4()


class dummyIdentifier:
    def __init__(self, uuid):
        self.uuid = uuid
        self.data = {}

    def typeFix(self, typeFix):
        self.data["typeFix"] = typeFix

    def topicFix(self, topicFix):
        self.data["topicFix"] = topicFix

    def infoFix(self, infoFix):
        self.data["infoFix"] = infoFix

    def producerFix(self, producerFix):
        self.data["producerFix"] = producerFix

    def posterFix(self, posterFix):
        self.data["posterFix"] = posterFix

    def feedbackFix(self, feedbackFix):
        self.data["feedbackFix"] = feedbackFix

    def updatorFix(self, updatorFix):
        self.data["updatorFix"] = updatorFix

    def fetcherFix(self, fetcherFix):
        self.data["fetcherFix"] = fetcherFix

    def processorFix(self, processorFix):
        self.data["processorFix"] = processorFix

    def optimizerFix(self, optimizerFix):
        self.data["optimizerFix"] = optimizerFix

    def reviewerFix(self, reviewerFix):
        self.data["reviewerFix"] = reviewerFix
