import numpy as np
import random as rand

places = []
tracePheromone = []
cologne = []
bestAnt = None

class ant:
    placesVisited = []

    def __init__(self,place):
        self.placesVisited.append(place)

    def vistPlace(self, place):
        self.placesVisited.append(place)

    def getDistance(self):
        distance = 0
        for x in range(1, len(self.placesVisited)):
            distance += np.linalg.norm(self.placesVisited[x][1] - self.placesVisited[x - 1][1])
        return distance


def createColegne(size):
    for x in range(size):
        startPlace = rand.randint(1, int(len(places)))
        cologne.append(ant(places[startPlace-1]))


def getBestTrace():
    if(bestAnt == None):
        tmpBestAnt = cologne[0]
    else:
        tmpBestAnt = bestAnt
    for x in range(1, len(cologne)):
        if(tmpBestAnt.getDistance() > cologne[x]):
            tmpBestAnt = cologne[x]
    global bestAnt
    bestAnt = tmpBestAnt





if __name__ == '__main__':
    files = open("A-n32-k5.txt", "r")
    for x in files:
        tmp = x.split()
        name =[]
        name.append(tmp[0])
        tmp.remove(tmp[0])
        tmp = [int(i) for i in tmp]
        tmp = np.array(tmp)
        name.append(tmp)
        places.append(name)
    print(places)

    for x in range(len(places)):
        tracePheromone.append([1]*len(places))
    print(tracePheromone)





