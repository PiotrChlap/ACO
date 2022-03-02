import numpy as np
import random as rand
import matplotlib.pyplot as plt


places = []
tracePheromone = []
cologne = []
distancePlaces = []
bestAnt = None
chanceRandomPlace = 0.3
alfa = 1
beta = 3
numberIterations = 1000
evaporationRate = 0.1

class Ant(object):


    def __init__(self,place):
        self.placesVisited = []
        self.availblePlace = []
        self.availblePlace = places.copy()
        self.placesVisited.append(place.copy())
        self.availblePlace.remove(self.availblePlace[int(place[0])-1])

    def vistPlace(self, place):
        self.placesVisited.append(place)
        self.availblePlace.remove(place)

    def randomPlace(self):
        tmp = rand.randint(0, len(self.availblePlace)-1)
        self.vistPlace(self.availblePlace[tmp])

    def getDistance(self):
        distance = 0
        for x in range(1, len(self.placesVisited)):
            distance += distancePlaces[int(self.placesVisited[x][0])-1][int(self.placesVisited[x-1][0])-1]
        return distance

    def getProbability(self):
        currentPlace = self.placesVisited[-1]
        table = []
        suma = 0
        for nextPlace in self.availblePlace:
            pheromoneX = np.power(tracePheromone[int(currentPlace[0])-1][int(nextPlace[0])-1],alfa)
            if(distancePlaces[int(currentPlace[0])-1][int(nextPlace[0])-1] == 0.0):
                heurestic =1000000000000
            else:
                heurestic = np.power(1/distancePlaces[int(currentPlace[0])-1][int(nextPlace[0])-1],beta)
            table.append(pheromoneX*heurestic)
            suma += table[-1]
        for x in range(len(table)):
            table[x] = table[x]/suma
        return table

    def rouletteSelection(self):
        probability = self.getProbability()
        section = []
        totality = 0
        ruoulette = rand.random()
        for i in range(len(self.availblePlace)):
            section.append([self.availblePlace[i][0],totality, totality+probability[i]])
            totality += probability[i]
            if(section[i][1]<= ruoulette < section[i][2]):
                self.vistPlace(self.availblePlace[i])
                break


def calculateDistance():
    global distancePlaces
    for x in range(len(places)):
        distancePlaces.append([])
        for y in range(len(places)):
            distancePlaces[x].append(np.linalg.norm(places[x][1]-places[y][1]))



def createColegne(size):
    global cologne
    cologne = []
    for x in range(size):
        startPlace = rand.randint(1, int(len(places)))
        cologne.append(Ant(places[startPlace-1]))


def getBestTrace():
    global bestAnt
    if(bestAnt == None):
        tmpBestAnt = cologne[0]
    else:
        tmpBestAnt = bestAnt
    for x in range(1, len(cologne)):
        if(tmpBestAnt.getDistance() > cologne[x].getDistance()):
            tmpBestAnt = cologne[x]
    bestAnt = tmpBestAnt

def updatePheromone():
    global tracePheromone
    for row in range(len(tracePheromone)):
        for column in range(len(tracePheromone)):
            tracePheromone[row][column] *= (1-evaporationRate)
    for ant in cologne:
        distance = ant.getDistance()
        for i in range(len(places)-1):
            #dodawanie feromonu w jedną stronę np z 2 do 5
            tracePheromone[int(ant.placesVisited[i][0]) - 1][int(ant.placesVisited[i + 1][0]) - 1] += (1/distance)
            #dodawanie feromonu w drugą stronę np z 5 do 2
            tracePheromone[int(ant.placesVisited[i + 1][0]) - 1][int(ant.placesVisited[i][0]) - 1] += (1 / distance)







if __name__ == '__main__':
    for i in range(2):
        places = []
        tracePheromone = []
        cologne = []
        distancePlaces = []
        bestAnt = None
        files = open("A-n80-k10.txt", "r")
        for x in files:
            tmp = x.split()
            name =[]
            name.append(tmp[0])
            tmp.remove(tmp[0])
            tmp = [int(i) for i in tmp]
            tmp = np.array(tmp)
            name.append(tmp)
            places.append(name)

        for x in range(len(places)):
            tracePheromone.append([1]*len(places))

        calculateDistance()



        for i in range(numberIterations):
            createColegne(30)
            for oneAnt in cologne:
                for x in range(len(places)-1):
                    if(chanceRandomPlace >= rand.random()):
                        oneAnt.randomPlace()
                    else:
                        oneAnt.rouletteSelection()
            updatePheromone()
            getBestTrace()
        print(bestAnt.getDistance())
        xpoints = []
        ypoints = []
        for x in bestAnt.placesVisited:
            xpoints.append(x[1][0])
            ypoints.append(x[1][1])

        f, ax = plt.subplots(1)
        ax.plot(xpoints, ypoints, color='green', marker='o', linestyle='dashed')

        ax.annotate("Start "+bestAnt.placesVisited[0][0], (xpoints[0], ypoints[0]), (xpoints[0], ypoints[0] +1))

        for i in range(1,len(xpoints)):
            ax.annotate(bestAnt.placesVisited[i][0],(xpoints[i],ypoints[i]), (xpoints[i], ypoints[i] +1))
        plt.show()









