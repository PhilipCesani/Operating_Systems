# /*
# ALGOS
# 1.  First-Come First-Served (FCFS) - non pre
#   -the ready que will update as processes come in and out based on fcfs
# 2.  Shortest Remaining Time First (SRTF) - pre-emptive
#   -the ready que update dynaically as processes come in and update to allow
#   -the srtf prioraty
# 3.  Highest Response Ratio Next (HRRN) - non pre
#   -
# 4.  Round Robin, with different quantum values (RR)
#
# METRICS
# for each lambda value
# The average turnaround time
# The total throughput (number of processes done per unit time)
# The CPU utilization
# The average number of processes in the ready queue
# single plot for each method based on
# */
import random
import math
from sys import argv
from Event import Event
from operator import attrgetter
import matplotlib.pyplot as plt

def genexp(l):
    x = 0
    while(x==0):
        u = random.random()
        x = (-1/l)*math.log(u)
    return(x)

def departIndex(list):
    for i in range(len(list)):
        if (list[i].getType == 2):
            return i


class Sim():
    def __init__(self, algo, lam, qv):
        self.events = []
        self.rq = []
        self.clock = 0.0
        self.algorithm = algo
        self.lam = 10.0 + lam
        self.avgST = .04
        self.qv = qv
        self.cpuIdle = 1 #1 = true, 0 = false
        self.endCondition = 0
        self.arrivalTime = []
        self.processTime = []
        self.pID = 0
        self.turnaroundTimes = []
        self.cpuUseTime = 0.0
        self.startUse = 0.0
        self.stopUse = 0.0
        self.totalQue = 0


    def init(self):
        previousEventTime = 0
        for i in range(10000):
            self.arrivalTime.append((genexp(self.lam)) + previousEventTime)
            previousEventTime = self.arrivalTime[i]
            self.processTime.append(genexp(1/self.avgST))
        self.events.append(Event(0, self.processTime[0], 1, 0))

    def scheduleEvent(self,type,eve):
        if (type == 1):
            self.events.append(eve)
        elif (type == 2):
            eve.setRequestTime(self.clock+eve.getTimeRemaining())
            eve.setType(2)
            self.events.append(eve)
        elif (type == 3):
            eve.setRequestTime(self.clock+self.qv)
            eve.setTimeRemaining(eve.getTimeRemaining()-self.qv)
            eve.setType(3)
            self.events.append(eve)
            #time slice event

    def arrival(self,event):
        if (self.algorithm == 1):
            if (self.cpuIdle == 1):
                self.cpuIdle = 0
                self.startUse = self.clock
                print("cpu starting, event: " + str(event.getID()) + " add to depart")
                self.scheduleEvent(2,event)
            else:
                print("cpu in use, added event: " + str(event.getID()) + " to ready que")
                self.rq.append(event)
                self.totalQue = 1 + self.totalQue
        elif (self.algorithm == 2):
            if (self.cpuIdle == 1):
                self.cpuIdle = 0
                self.startUse = self.clock
                ##print("cpu starting, event add to depart")
                self.scheduleEvent(2,event)
            else:
                ##print("An interupt has occured")
                index = departIndex(self.events)
                self.events[index].setTimeRemaining(self.events[index].getTimeRemaining()-self.clock)
                for i in range(len(self.events)):
                    temp = self.events[i]
                    self.rq.append(temp)
                self.events.pop(index)
                self.rq = self.rq = sorted(self.rq,key=attrgetter('timeRemaining'))
                temp = self.rq[0]
                self.scheduleEvent(2,temp)
                self.rq.pop(0)
                self.totalQue = 1 + self.totalQue
        elif (self.algorithm == 3):
            if (self.cpuIdle == 1):
                self.cpuIdle = 0
                self.startUse = self.clock
                #print("cpu starting, event add to depart")
                self.scheduleEvent(2,event)
            else:
                #print("cpu running, new event added to rq")
                self.totalQue = 1 + self.totalQue
                self.rq.append(event)
        elif (self.algorithm == 4):
            if (self.cpuIdle == 1):
                self.cpuIdle == 0
                self.startUse = self.clock
                if(event.getTimeRemaining() < self.qv):
                    ##print("cpu starting, event add to depart")
                    self.scheduleEvent(2,event)
                else:
                    ##print("cpu starting, event add to ts")
                    self.scheduleEvent(3,event)
            else:
                ##print("cpu running, new event added to rq")
                self.totalQue = 1 + self.totalQue
                self.rq.append(event)

    def depart(self):
        if (self.algorithm == 1):
            if (len(self.rq)==0):
                self.cpuIdle = 1
                self.stopUse = self.clock
                self.cpuUseTime = (self.stopUse - self.startUse) + self.cpuUseTime
                print("cpu idle, nothing in rq")
            else:
                print("cpu in use, depart occuring, scheduled: "+ str(self.rq[0].getID()) +" as next depart")
                temp = self.rq[0]
                self.scheduleEvent(2,temp)
                self.rq.pop(0)
        elif (self.algorithm == 2):
            #for a depart if there is stuff in ready que then
            #sort by shortest time remaining
            if (len(self.rq) == 0):
                self.cpuIdle = 1
                self.stopUse = clock
                self.cpuUseTime = (self.stopUse - self.startUse) + self.cpuUseTime
                #print("cpu idle, nothing in rq")
            else:
                #print("new process, cpu still running, scheduled process depart")
                self.rq = sorted(self.rq,key=attrgetter('timeRemaining'))
                temp = self.rq[0]
                self.scheduleEvent(2,temp)
                self.rq.pop(0)
                self.totalQue = 1 + self.totalQue
        elif (self.algorithm == 3):
            if (len(self.rq) == 0):
                self.cpuIdle = 1
                self.stopUse = clock
                self.cpuUseTime = (self.stopUse - self.startUse) + self.cpuUseTime
                #print("cpu idle, nothing in rq")
            else:
                #print("process from rq, cpu still running, scheduled depart")
                for i in range(len(self.rq)):
                    self.rq[i].setWT(self.rq[i].getRequestTime() - self.clock)
                    self.rq[i].setRR((self.rq[i].getWaitTime() + self.rq[i].getTimeRemaining())/self.rq[i].getTimeRemaining())
                self.rq = sorted(self.rq,key=attrgetter('responseRatio'),reverse=True)
                self.scheduleEvent(2,self.rq[0])
                self.rq.pop(0)
                self.totalQue = 1 + self.totalQue
        elif (self.algorithm == 4):
            if (len(self.rq) == 0):
                self.cpuIdle = 1
                self.stopUse = clock
                self.cpuUseTime = (self.stopUse - self.startUse) + self.cpuUseTime
                ##print("cpu idle, nothing in rq")
            else:
                ##print("process from rq, cpu still running, scheduled depart")
                self.rq[0].setRequestTime(clock)
                event = self.rq[0]
                self.totalQue = 1 + self.totalQue
                if(self.rq.getTimeRemaining() < self.qv):
                    ##print("cpu running, rq event add to depart")
                    self.scheduleEvent(2,event)
                    self.rq.pop(0)
                else:
                    ##print("cpu running, rq event add to ts")
                    self.scheduleEvent(3,event)
                    self.rq.pop(0)

    def timeSlice(self, event):
        if (len(self.rq)==0):
            if(event.getTimeRemaining() < self.qv):
                ##print("cpu running, ts add to depart")
                self.scheduleEvent(2,event)
            else:
                ##print("cpu running, ts add to ts")
                self.scheduleEvent(3,event)
        else:
            if(self.rq[0].getRequestTime() < self.clock):
                if(self.rq[0].getTimeRemaining() < self.qv):
                    #print("cpu running, rq add to depart")
                    self.rq[0].setRequestTime(self.clock)
                    self.scheduleEvent(2,self.rq)
                else:
                    #print("cpu running, rq add to ts")
                    self.rq[0].setRequestTime(self.clock)
                    self.scheduleEvent(3,self.rq)
                self.totalQue = 1 + self.totalQue
                self.rq.append(event)
                self.rq.pop(0)
            else:
                if(event.getTimeRemaining() < self.qv):
                    #print("cpu running, ts add to depart")
                    self.scheduleEvent(2,event)
                else:
                    #print("cpu running, ts add to ts")
                    self.scheduleEvent(3,event)

    def runSim(self):
        while(self.endCondition != 10000):
            eve = self.events[0]
            #print("Event to process: " + str(eve.getID()))
            self.clock = eve.getRequestTime()

            if (eve.getType() == 1):
                self.arrival(eve)
            elif(eve.getType() == 2):
                self.turnaroundTimes.append(eve.getTurnAroundTime())
                self.depart()
                self.endCondition = self.endCondition + 1
                #print("Processes completed: " + str(self.endCondition))
            elif(eve.getType() == 3):
                self.timeSlice(eve)

            self.events.pop(0)
            if (self.pID != 9999):
                self.pID = self.pID + 1
                nextEve = Event((self.arrivalTime[self.pID]), self.processTime[self.pID],1,self.pID)
                self.scheduleEvent(1,nextEve)

            self.events = sorted(self.events,key=attrgetter('requestTime'))

    def metrics(self, turnList, throughList, cpuList, queList):
        turnList.append(sum(self.turnaroundTimes)/10000)
        throughList.append(10000/self.clock)
        cpuList.append((self.cpuUseTime/self.clock)*100)
        queList.append(self.totalQue/self.clock)

################################################################################


turnTimes = []
throughTimes = []
cpuUtilTimes = []
avgQueTimes = []
lamValues = []
#FCFS
for i in range (21):
    print("FCFS" + str(i))
    lamValues.append(10+i)
    sim = Sim(1,i,.01)
    sim.init()
    sim.runSim()
    sim.metrics(turnTimes,throughTimes,cpuUtilTimes,avgQueTimes)

plt.plot(lamValues, turnTimes, label = "Turn Around Average")
plt.plot(lamValues, throughTimes, label = "Through Put (Processes Per Second)")
plt.plot(lamValues, cpuUtilTimes, label = "CPU Util %")
plt.plot(lamValues, avgQueTimes, label = "Average Que Size")

plt.xlabel('Lambda Values')
plt.ylabel('FCFS Values')

plt.legend()
plt.show()


#need to print graphs to file after interation

turnTimes = []
throughTimes = []
cpuUtilTimes = []
avgQueTimes = []
lamValues = []
#SRTF
for i in range (21):
    print("SRTF" + str(i))
    lamValues.append(10+i)
    sim = Sim(1,i,.01)
    sim.init()
    sim.runSim()
    sim.metrics(turnTimes,throughTimes,cpuUtilTimes,avgQueTimes)

plt.plot(lamValues, turnTimes, label = "Turn Around Average")
plt.plot(lamValues, throughTimes, label = "Through Put (Processes Per Second)")
plt.plot(lamValues, cpuUtilTimes, label = "CPU Util %")
plt.plot(lamValues, avgQueTimes, label = "Average Que Size")

plt.xlabel('Lambda Values')
plt.ylabel('SRTF Values')

plt.legend()
plt.show()

turnTimes = []
throughTimes = []
cpuUtilTimes = []
avgQueTimes = []
lamValues = []
#HRRN
for i in range (21):
    print("HRRN" + str(i))
    lamValues.append(10+i)
    sim = Sim(1,i,.01)
    sim.init()
    sim.runSim()
    sim.metrics(turnTimes,throughTimes,cpuUtilTimes,avgQueTimes)

plt.plot(lamValues, turnTimes, label = "Turn Around Average")
plt.plot(lamValues, throughTimes, label = "Through Put (Processes Per Second)")
plt.plot(lamValues, cpuUtilTimes, label = "CPU Util %")
plt.plot(lamValues, avgQueTimes, label = "Average Que Size")

plt.xlabel('Lambda Values')
plt.ylabel('HRRN Values')

plt.legend()
plt.show()


turnTimes = []
throughTimes = []
cpuUtilTimes = []
avgQueTimes = []
lamValues = []
#RR - .01 qv
for i in range (21):
    print("RR - .01 " + str(i))
    lamValues.append(10+i)
    sim = Sim(1,i,.01)
    sim.init()
    sim.runSim()
    sim.metrics(turnTimes,throughTimes,cpuUtilTimes,avgQueTimes)

plt.plot(lamValues, turnTimes, label = "Turn Around Average")
plt.plot(lamValues, throughTimes, label = "Through Put (Processes Per Second)")
plt.plot(lamValues, cpuUtilTimes, label = "CPU Util %")
plt.plot(lamValues, avgQueTimes, label = "Average Que Size")

plt.xlabel('Lambda Values')
plt.ylabel('RR - .01 Values')

plt.legend()
plt.show()

turnTimes = []
throughTimes = []
cpuUtilTimes = []
avgQueTimes = []
lamValues = []
#RR - .2
for i in range (21):
    print("RR - .2 " + str(i))
    lamValues.append(10+i)
    sim = Sim(1,i,.2)
    sim.init()
    sim.runSim()
    sim.metrics(turnTimes,throughTimes,cpuUtilTimes,avgQueTimes)

plt.plot(lamValues, turnTimes, label = "Turn Around Average")
plt.plot(lamValues, throughTimes, label = "Through Put (Processes Per Second)")
plt.plot(lamValues, cpuUtilTimes, label = "CPU Util %")
plt.plot(lamValues, avgQueTimes, label = "Average Que Size")

plt.xlabel('Lambda Values')
plt.ylabel('RR - .2 Values')

plt.legend()
plt.show()
