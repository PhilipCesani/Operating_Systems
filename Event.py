class Event():
    def __init__(self, rt, st, type, ID):
        self.originalRT = rt
        self.requestTime = rt
        self.timeRemaining = st
        self.type = type #1:arr,2:dep,3:ts
        self.ID = ID
        self.responseRatio = 0.0
        self.waitTime = 0.0

    def setRequestTime(self, time):
        self.requestTime = time
    def setTimeRemaining(self, time):
        self.timeRemaining = time
    def setType(self, type):
        self.type = type
    def setID(self, ID):
        self.ID = ID
    def setRR(self,rr):
        self.responseRatio = rr
    def setWT(self, wt):
        self.waitTime = wt

    def getRequestTime(self):
        return self.requestTime
    def getTimeRemaining(self):
        return self.timeRemaining
    def getType(self):
        return self.type
    def getID(self):
        return self.ID
    def getResponseRatio(self):
        return self.responseRatio
    def getWaitTime(self):
        return self.waitTime
    def getTurnAroundTime(self):
        return (self.requestTime - self.originalRT)
