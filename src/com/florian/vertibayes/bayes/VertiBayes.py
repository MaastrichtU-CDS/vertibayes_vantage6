import json
import random

import numpy
import pandas
from pgmpy.models import BayesianNetwork


class VertiBayes:
    def __init__(self, population, nodes):
        self.__population = population
        self.__network = None
        self.__nodes = json.loads(nodes)

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
        individual = self._generateIndividual()
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
                                individual[node.get('name')] = self._generateValue(theta)
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
                            y += theta.get('p')
                            if (x <= y):
                                individual[node.get('name')] = self._generateValue(theta)
                                break
        return individual

    def _generateValue(self, theta):
        # Convert missing values appropriatly for pgmpy
        if theta.get('localValue').get('value') == '?':
            return numpy.NaN
        else:
            return theta.get('localValue').get('value')