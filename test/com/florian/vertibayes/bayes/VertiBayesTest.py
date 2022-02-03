import json
import tempfile
import unittest
import jsonpickle
from pgmpy.readwrite import BIFWriter

from pomegranate.BayesianNetwork import BayesianNetwork

from com.florian.vertibayes.bayes.VertiBayes import VertiBayes

POPUlATION = 1000

class CentralStationTest(unittest.TestCase):
    def test_network(self):
        #Should result in the following network: x1 -> x2 -> x3
        vertiBayes = VertiBayes(POPUlATION, json.loads(self._generateJSON()).get('nodes'))
        vertiBayes.defineLocalNetwork()
        vertiBayes.trainNetwork()
        network = vertiBayes.getNetwork()

        print(vertiBayes.toBif())

        self.assertEquals(len(network.get_cpds()), 3)
        self.assertEquals(network.get_cpds()[0].variable, 'x1')
        self.assertEquals(network.get_cpds()[0].variables, ['x1'])
        self.assertEquals(network.get_cpds()[1].variable, 'x2')
        self.assertEquals(network.get_cpds()[1].variables, ['x2', 'x1'])
        self.assertEquals(network.get_cpds()[2].variable, 'x3')
        self.assertEquals(network.get_cpds()[2].variables, ['x3','x2'])

    def test_networkMissingValues(self):
        # Should result in the following network: x1 -> x2 -> x3
        # Pretty much the same network as without missing values, but slightly different values
        # This test purely exist to check stuff doesn't crash as testing for the exact CPD's is pointless
        # due to the RNG involved
        vertiBayes = VertiBayes(POPUlATION, json.loads(self._generateJSONMissingValues()).get('nodes'))
        vertiBayes.defineLocalNetwork()
        vertiBayes.trainNetwork()
        network = vertiBayes.getNetwork()

        self.assertEquals(len(network.get_cpds()), 3)
        self.assertEquals(network.get_cpds()[0].variable, 'x1')
        self.assertEquals(network.get_cpds()[0].variables, ['x1'])
        self.assertEquals(network.get_cpds()[1].variable, 'x2')
        self.assertEquals(network.get_cpds()[1].variables, ['x2', 'x1'])
        self.assertEquals(network.get_cpds()[2].variable, 'x3')
        self.assertEquals(network.get_cpds()[2].variables, ['x3', 'x2'])

    def test_networkMultipleParents(self):
        # Should result in the following network: x1 -> x2, x1,x2 ->x3

        vertiBayes = VertiBayes(POPUlATION, json.loads(self._generateJSONMultipleParents()).get('nodes'))
        vertiBayes.defineLocalNetwork()
        vertiBayes.trainNetwork()
        network = vertiBayes.getNetwork()

        self.assertEquals(len(network.get_cpds()), 3)
        self.assertEquals(network.get_cpds()[0].variable, 'x1')
        self.assertEquals(network.get_cpds()[0].variables, ['x1'])
        self.assertEquals(network.get_cpds()[1].variable, 'x2')
        self.assertEquals(network.get_cpds()[1].variables, ['x2', 'x1'])
        self.assertEquals(network.get_cpds()[2].variable, 'x3')
        self.assertEquals(network.get_cpds()[2].variables, ['x3', 'x1', 'x2'])

    def test_networBins(self):
        # Should result in the following network: x1 -> x2, x1,x2 ->x3

        vertiBayes = VertiBayes(POPUlATION, json.loads(self._generateJSONBins()).get('nodes'))
        vertiBayes.defineLocalNetwork()
        vertiBayes.trainNetwork()
        network = vertiBayes.getNetwork()

        self.assertEquals(len(network.get_cpds()), 3)
        self.assertEquals(network.get_cpds()[0].variable, 'x1')
        self.assertEquals(network.get_cpds()[0].variables, ['x1'])
        self.assertEquals(network.get_cpds()[1].variable, 'x2')
        self.assertEquals(network.get_cpds()[1].variables, ['x2', 'x1'])
        self.assertEquals(network.get_cpds()[2].variable, 'x3')
        self.assertEquals(network.get_cpds()[2].variables, ['x3', 'x2'])


    def _generateJSON(self):
        #  Python formating fucking sucks... god forbid we actually have newlines
        return "{\"nodes\":[{\"parents\":[],\"name\":\"x1\",\"type\":\"number\",\"probabilities\":[{\"localValue\":\"0\",\"parentValues\":{},\"p\":0.5},{\"localValue\":\"1\",\"parentValues\":{},\"p\":0.5}]},{\"parents\":[\"x1\"],\"name\":\"x2\",\"type\":\"number\",\"probabilities\":[{\"localValue\":\"0\",\"parentValues\":{\"x1\":\"0\"},\"p\":0.8},{\"localValue\":\"1\",\"parentValues\":{\"x1\":\"0\"},\"p\":0.2},{\"localValue\":\"0\",\"parentValues\":{\"x1\":\"1\"},\"p\":0.2},{\"localValue\":\"1\",\"parentValues\":{\"x1\":\"1\"},\"p\":0.8}]},{\"parents\":[\"x2\"],\"name\":\"x3\",\"type\":\"number\",\"probabilities\":[{\"localValue\":\"0\",\"parentValues\":{\"x2\":\"0\"},\"p\":0.8},{\"localValue\":\"1\",\"parentValues\":{\"x2\":\"0\"},\"p\":0.2},{\"localValue\":\"0\",\"parentValues\":{\"x2\":\"1\"},\"p\":0.001},{\"localValue\":\"1\",\"parentValues\":{\"x2\":\"1\"},\"p\":0.999}]}]}"

    def _generateJSONMissingValues(self):
        #  Python formating fucking sucks... god forbid we actually have newlines
        return "{\"nodes\":[{\"parents\":[],\"name\":\"x1\",\"type\":\"number\",\"probabilities\":[{\"localValue\":\"0\",\"parentValues\":{},\"p\":0.5},{\"localValue\":\"1\",\"parentValues\":{},\"p\":0.5}]},{\"parents\":[\"x1\"],\"name\":\"x2\",\"type\":\"number\",\"probabilities\":[{\"localValue\":\"0\",\"parentValues\":{\"x1\":\"0\"},\"p\":0.8},{\"localValue\":\"1\",\"parentValues\":{\"x1\":\"0\"},\"p\":0.2},{\"localValue\":\"0\",\"parentValues\":{\"x1\":\"1\"},\"p\":0.2},{\"localValue\":\"1\",\"parentValues\":{\"x1\":\"1\"},\"p\":0.8}]},{\"parents\":[\"x2\"],\"name\":\"x3\",\"type\":\"number\",\"probabilities\":[{\"localValue\":\"0\",\"parentValues\":{\"x2\":\"0\"},\"p\":0.33},{\"localValue\":\"1\",\"parentValues\":{\"x2\":\"0\"},\"p\":0.33},{\"localValue\":\"0\",\"parentValues\":{\"x2\":\"1\"},\"p\":0.33},{\"localValue\":\"1\",\"parentValues\":{\"x2\":\"1\"},\"p\":0.33},{\"localValue\":\"?\",\"parentValues\":{\"x2\":\"0\"},\"p\":0.33},{\"localValue\":\"?\",\"parentValues\":{\"x2\":\"1\"},\"p\":0.33}]}]}"

    def _generateJSONMultipleParents(self):
        return "{\"nodes\":[{\"parents\":[],\"name\":\"x1\",\"type\":\"number\",\"probabilities\":[{\"localValue\":\"0\",\"parentValues\":{},\"p\":0.5},{\"localValue\":\"1\",\"parentValues\":{},\"p\":0.5}]},{\"parents\":[\"x1\"],\"name\":\"x2\",\"type\":\"number\",\"probabilities\":[{\"localValue\":\"0\",\"parentValues\":{\"x1\":\"0\"},\"p\":0.8},{\"localValue\":\"1\",\"parentValues\":{\"x1\":\"0\"},\"p\":0.2},{\"localValue\":\"0\",\"parentValues\":{\"x1\":\"1\"},\"p\":0.2},{\"localValue\":\"1\",\"parentValues\":{\"x1\":\"1\"},\"p\":0.8}]},{\"parents\":[\"x1\",\"x2\"],\"name\":\"x3\",\"type\":\"number\",\"probabilities\":[{\"localValue\":\"0\",\"parentValues\":{\"x2\":\"0\",\"x1\":\"0\"},\"p\":0.25},{\"localValue\":\"0\",\"parentValues\":{\"x2\":\"0\",\"x1\":\"1\"},\"p\":0.25},{\"localValue\":\"0\",\"parentValues\":{\"x2\":\"1\",\"x1\":\"0\"},\"p\":0.25},{\"localValue\":\"0\",\"parentValues\":{\"x2\":\"1\",\"x1\":\"1\"},\"p\":0.25},{\"localValue\":\"1\",\"parentValues\":{\"x2\":\"0\",\"x1\":\"0\"},\"p\":0.25},{\"localValue\":\"1\",\"parentValues\":{\"x2\":\"0\",\"x1\":\"1\"},\"p\":0.25},{\"localValue\":\"1\",\"parentValues\":{\"x2\":\"1\",\"x1\":\"0\"},\"p\":0.25},{\"localValue\":\"1\",\"parentValues\":{\"x2\":\"1\",\"x1\":\"1\"},\"p\":0.25}]}]}"

    def _generateJSONBins(self):
        return "{\"nodes\":[{\"parents\":[],\"name\":\"x1\",\"type\":\"number\",\"probabilities\":[{\"localValue\":{\"localValue\":null,\"upperLimit\":\"0.5\",\"lowerLimit\":\"-1\",\"range\":true},\"parentValues\":{},\"p\":0.5},{\"localValue\":{\"localValue\":null,\"upperLimit\":\"1.5\",\"lowerLimit\":\"0.5\",\"range\":true},\"parentValues\":{},\"p\":0.5}],\"bins\":[{\"upperLimit\":\"0.5\",\"lowerLimit\":\"-1\"},{\"upperLimit\":\"1.5\",\"lowerLimit\":\"0.5\"}],\"discrete\":false},{\"parents\":[\"x1\"],\"name\":\"x2\",\"type\":\"number\",\"probabilities\":[{\"localValue\":{\"localValue\":null,\"upperLimit\":\"0.5\",\"lowerLimit\":\"-1\",\"range\":true},\"parentValues\":{\"x1\":{\"localValue\":null,\"upperLimit\":\"0.5\",\"lowerLimit\":\"-1\",\"range\":true}},\"p\":0.8},{\"localValue\":{\"localValue\":null,\"upperLimit\":\"1.5\",\"lowerLimit\":\"0.5\",\"range\":true},\"parentValues\":{\"x1\":{\"localValue\":null,\"upperLimit\":\"0.5\",\"lowerLimit\":\"-1\",\"range\":true}},\"p\":0.2},{\"localValue\":{\"localValue\":null,\"upperLimit\":\"0.5\",\"lowerLimit\":\"-1\",\"range\":true},\"parentValues\":{\"x1\":{\"localValue\":null,\"upperLimit\":\"1.5\",\"lowerLimit\":\"0.5\",\"range\":true}},\"p\":0.2},{\"localValue\":{\"localValue\":null,\"upperLimit\":\"1.5\",\"lowerLimit\":\"0.5\",\"range\":true},\"parentValues\":{\"x1\":{\"localValue\":null,\"upperLimit\":\"1.5\",\"lowerLimit\":\"0.5\",\"range\":true}},\"p\":0.8}],\"bins\":[{\"upperLimit\":\"0.5\",\"lowerLimit\":\"-1\"},{\"upperLimit\":\"1.5\",\"lowerLimit\":\"0.5\"}],\"discrete\":false},{\"parents\":[\"x2\"],\"name\":\"x3\",\"type\":\"number\",\"probabilities\":[{\"localValue\":{\"localValue\":null,\"upperLimit\":\"1.5\",\"lowerLimit\":\"0.5\",\"range\":true},\"parentValues\":{\"x2\":{\"localValue\":null,\"upperLimit\":\"0.5\",\"lowerLimit\":\"-1\",\"range\":true}},\"p\":0.2},{\"localValue\":{\"localValue\":null,\"upperLimit\":\"0.5\",\"lowerLimit\":\"-1\",\"range\":true},\"parentValues\":{\"x2\":{\"localValue\":null,\"upperLimit\":\"0.5\",\"lowerLimit\":\"-1\",\"range\":true}},\"p\":0.8},{\"localValue\":{\"localValue\":null,\"upperLimit\":\"1.5\",\"lowerLimit\":\"0.5\",\"range\":true},\"parentValues\":{\"x2\":{\"localValue\":null,\"upperLimit\":\"1.5\",\"lowerLimit\":\"0.5\",\"range\":true}},\"p\":0.999},{\"localValue\":{\"localValue\":null,\"upperLimit\":\"0.5\",\"lowerLimit\":\"-1\",\"range\":true},\"parentValues\":{\"x2\":{\"localValue\":null,\"upperLimit\":\"1.5\",\"lowerLimit\":\"0.5\",\"range\":true}},\"p\":0.001}],\"bins\":[{\"upperLimit\":\"1.5\",\"lowerLimit\":\"0.5\"},{\"upperLimit\":\"0.5\",\"lowerLimit\":\"-1\"}],\"discrete\":false}]}"