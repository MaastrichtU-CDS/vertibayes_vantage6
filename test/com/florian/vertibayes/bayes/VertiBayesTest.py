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
        # Manual test to see if the CSV is properly generated
        # The resulting CSV should contain 3 tables, one for each variable
        # x1 has 1 value
        # x2 has 1 value and 1 parent
        # x3 has 2 values and 2 parents
        vertiBayes = VertiBayes()
        vertiBayes.generateOutputCSV(json.loads(self._generateNetworkJSON()))





    def _generateNetworkJSON(self):
        return "{\"nodes\":[{\"parents\":[],\"name\":\"x1\",\"type\":\"numeric\",\"probabilities\":[{\"localValue\":{\"localValue\":null,\"upperLimit\":\"All\",\"lowerLimit\":\"All\",\"range\":true},\"parentValues\":[],\"p\":1}],\"bins\":[{\"upperLimit\":\"All\",\"lowerLimit\":\"All\"}],\"discrete\":true},{\"parents\":[\"x1\"],\"name\":\"x2\",\"type\":\"real\",\"probabilities\":[{\"localValue\":{\"localValue\":null,\"upperLimit\":\"All\",\"lowerLimit\":\"All\",\"range\":true},\"parentValues\":[{\"parent\":\"x1\",\"value\":{\"localValue\":null,\"upperLimit\":\"All\",\"lowerLimit\":\"All\",\"range\":true}}],\"p\":1}],\"bins\":[{\"upperLimit\":\"All\",\"lowerLimit\":\"All\"}],\"discrete\":false},{\"parents\":[\"x2\",\"x1\"],\"name\":\"x3\",\"type\":\"string\",\"probabilities\":[{\"localValue\":{\"localValue\":\"0\",\"upperLimit\":null,\"lowerLimit\":null,\"range\":false},\"parentValues\":[{\"parent\":\"x2\",\"value\":{\"localValue\":null,\"upperLimit\":\"All\",\"lowerLimit\":\"All\",\"range\":true}},{\"parent\":\"x1\",\"value\":{\"localValue\":null,\"upperLimit\":\"All\",\"lowerLimit\":\"All\",\"range\":true}}],\"p\":0.5038996100389961},{\"localValue\":{\"localValue\":\"1\",\"upperLimit\":null,\"lowerLimit\":null,\"range\":false},\"parentValues\":[{\"parent\":\"x2\",\"value\":{\"localValue\":null,\"upperLimit\":\"All\",\"lowerLimit\":\"All\",\"range\":true}},{\"parent\":\"x1\",\"value\":{\"localValue\":null,\"upperLimit\":\"All\",\"lowerLimit\":\"All\",\"range\":true}}],\"p\":0.4961003899610039}],\"bins\":[],\"discrete\":true}],\"target\":\"x3\"}"
