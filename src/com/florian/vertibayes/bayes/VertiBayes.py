import pickle
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
                edges.append((parent, node.get('name')))
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
                                if node.get('discrete'):
                                    individual[node.get('name')] = theta.get('localValue').get('localValue')
                                else:
                                    z = random.uniform(0,1)
                                    lower = theta.get('localValue').get('upperLimit')
                                    upper = theta.get('localValue').get('lowerLimit')
                                    individual[node.get('name')] = float(lower) + z * (float(upper) - float(lower))
                                break
                        else:
                            # node has parents, so check if parent values have been selected yet
                            correctTheta = True
                            for parent in theta.get('parentValues'):
                                if individual.get(parent) == None:
                                    # not all parents are selected, move on
                                    correctTheta = False
                                    break
                                else:
                                    # discrete values
                                    if not theta.get('parentValues')[parent].get('range'):
                                        if individual.get(parent) != theta.get('parentValues')[parent]:
                                            # A parent has the wrong value, move on
                                            correctTheta = False
                                            break
                                    else:
                                        # range values
                                        parentV = individual.get(parent)
                                        if parentV >= float(theta.get('parentValues')[parent].get('upperLimit')) or parentV < float(theta.get('parentValues')[parent].get('lowerLimit')):
                                            correctTheta = False
                                            break
                            if(correctTheta):
                                y += theta.get('p')
                                if (x <= y):
                                    if node.get('discrete'):
                                        individual[node.get('name')] = theta.get('localValue').get('localValue')
                                    else:
                                        z = random.uniform(0, 1)
                                        lower = theta.get('localValue').get('upperLimit')
                                        upper = theta.get('localValue').get('lowerLimit')
                                        individual[node.get('name')] = float(lower) + z * (float(upper) - float(lower))
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


    def generateOutputCSV(self, network: BayesianNetwork):
        # Function to generate a CSV based on the network generated.
        # This generation is needed to provide the controllers at CBS something to work with.
        # This little script should probably be moved to the researcher at some point.
        import csv
        from pgmpy.factors.discrete import TabularCPD

        # open the file in the write mode
        f = open('test.csv', 'w', newline='')
        # create the csv writer
        writer = csv.writer(f)
        # write a cpd to the file
        for cpd in network.get_cpds():
            header = []
            header.append("Variable: "+cpd.variable)
            # add a header for each CPD to indicate which main attribute this belongs to
            writer.writerow(header)
            cpd: TabularCPD = cpd
            string = cpd.__str__()

            # reformat the string they print to a table I can actually stick in a CSV
            # Why does their object consist of seperate tables for the values & states? How am I supposed to know which
            # cell in the table corresponds to which state without checking it against the print? Why is this not one dictionairy?
            reformat = string.replace("-","").replace("+","").replace("|",",").replace(",\n\n,",";").replace("\n,","").replace(",\n","").replace(" ","")
            rows = reformat.split(";")
            table = [];
            for row in rows:
                table.append(row.split(","))

            # print table
            for row in table:
                writer.writerow(row)
            writer.writerow("")

        # close the file
        f.close()

    def visualize(self, network: BayesianNetwork):
        # Simple method to visualize the bayesian network
        # This can be used in conjunction with the CSV with CPD's to give to the controllers
        # This will also need to be transfered to the researcher side at some point, but storing it here for now.
        import networkx as nx
        import matplotlib.pyplot as plt
        nx.draw(network, with_labels=True)
        plt.show()