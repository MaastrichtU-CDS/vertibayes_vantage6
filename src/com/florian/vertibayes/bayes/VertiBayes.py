import random

import numpy
import pandas
from pgmpy.models import BayesianNetwork
from pgmpy.readwrite import BIFReader
from pgmpy.readwrite import BIFWriter



class VertiBayes:
    def __init__(self, population, nodes):
        self.__population = population
        self.__network = None
        self.__nodes = nodes

    def getNetwork(self):
        return self.__network

    def defineLocalNetwork(self):
        edges = []
        for node in self.__nodes:
            for parent in node.get('parents'):
                edges.append((parent.get('name'), node.get('name')))
        self.__network = BayesianNetwork(edges)

    def trainNetwork(self):
        self.__network.fit(self._generateData())

    def _generateData(self):
        data = []
        for i in range(0, self.__population):
            data.append(self._generateIndividual())
        df = pandas.DataFrame.from_dict(data)
        return df

    def _generateIndividual(self):
        individual = {}
        done = False
        while not done:
            done = True
            for node in self.__nodes:
                if individual.get(node.get('name')) == None:
                    done = False
                    # this attribute does not have a value yet
                    x = random.uniform(0, 1)
                    y = 0
                    for theta in node.get('probabilities'):
                        if len(node.get('parents')) == 0:
                            # no parents, just select a random value
                            y += theta.get('p')
                            if (x <= y):
                                individual[node.get('name')] = theta.get('localValue').get('value')
                                break
                        else:
                            # node has parents, so check if parent values have been selected yet
                            correctTheta = True
                            for parent in theta.get('parents'):
                                if individual.get(parent.get('name')) == None:
                                    # not all parents are selected, move on
                                    correctTheta = False
                                    break
                                elif individual.get(parent.get('name')) != parent.get('value').get('value'):
                                    # A parent has the wrong value, move on
                                    correctTheta = False
                                    break
                            if(correctTheta):
                                y += theta.get('p')
                                if (x <= y):
                                    individual[node.get('name')] = theta.get('localValue').get('value')
                                    break
        self._dealWithMissingValues(individual)
        return individual

    def _dealWithMissingValues(self, individual):
        # python treates numpy.NaN as None, so cannot set these values while generation as my loop breaks
        # ergo just convert after generation of an individual
        # This is really dumb, why is numpy.NaN equal to None? Who designs these things
        for key in individual:
            if individual.get(key) == '?':
                individual[key] = numpy.NaN

    def toBif(self):
        x = BIFWriter(self.__network).__str__()
        return x

    def fromBif(self, str):
       return BIFReader(None, str).get_model()