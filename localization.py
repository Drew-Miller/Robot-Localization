#!/usr/bin/env python3
import random
from math import *


worldX = 10
worldY = 10
world = [worldX, worldY]

locations = [[20,20],[20, 80],[80, 80],[80, 20]]

#particles will have all member variables set.
#x,y,z,o
#only the original sub uses the sense function and that
#will get data from real sensors.
#the real sub will not use for x,y,z since we cannot determine
#those. We Will just use particles and base where we think we
# are based on groupings of highly possible particles
class robot:
    def __init__(self):
        self.__x = random.random() * worldX
        self.__y = random.random() * worldY
        self.__orientation = random.random() * 2 * pi
        self.__forward_noise = 0.0
        self.__turn_noise = 0.0
        self.__sense_noise = 0.0


    def __str__(self):
        return "[x={0:0.2f} y={1:0.2f} heading={2:0.2f}]".format(
        self.__x, self.__y, self.__orientation)


    def __repr__(self):
        return str(self)


    def set(self, x, y, o):
        if x < 0 or x > worldX:
            raise ValueError("X coordinate is outside of world Bound")

        if y < 0 or y > worldY:
            raise ValueError("Y coordinate is outside of world Bound")

        if o >= 2 * pi or o <= -2 * pi:
            o = o % (2 * pi)

        if o < 0:
            o = o + 2 * pi

        self.__x = x
        self.__y = y
        self.__orientation = o


    def move(self, turn, distance):
        self.__orientation = self.__orientation + turn
        self.__x = self.__x + cos(self.__orientation) * distance
        self.__y = self.__y + sin(self.__orientation) * distance


    def setNoise(self, fNoise, tNoise, sNoise):
        self.__forward_noise = fNoise
        self.__turn_noise = tNoise
        self.__sense_noise = sNoise


    def senseClean(self):
        return self.calcDistances()

    def doSense(self):
        dist = self.calcDistances()
        for i, d in enumerate(dist):
            d = d + ((random.random() - .5)* 2 * self.__sense_noise)
            dist[i] = d

        self.sense = dist
        return dist


    def calcDistances(self):
        distances = []

        for l in locations:
            dist = sqrt((l[0] - self.__x)**2 + (l[1] -  self.__y)**2)
            distances.append(round(dist, 2))

        return distances


    #takes used for the probability of particles
    #measurement is the vector measured from the
    #original robot. The prob is the probability of the
    #robot existing there


    def measurement_prob(self, measurement):
        # calculates how likely a measurement should be
        prob = 1.0;
        for i in range(len(locations)):
            dist = sqrt((self.__x - locations[i][0]) ** 2 + (self.__y - locations[i][1]) ** 2)
            prob *= Gaussian(dist, self.__sense_noise, measurement[i])

        self.__prob = prob
        return prob

    def prob(self):
        return self.__prob

    def resample(self):
        chance = random.random()
        if chance > self.__prob:
            self.__x = random.random() * worldX
            self.__y = random.random() * worldY
            self.__orientation = random.random() * 2 * pi

def Gaussian(mu, sigma, x):
    # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
    return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))


s = robot()
s.setNoise(.1, .1, .1)
r = robot()
distances = s.calcDistances()

particleNumber = 1000
p = []
for i in range(particleNumber):
    p.append(robot())
    p[i].setNoise(0,0,1)
