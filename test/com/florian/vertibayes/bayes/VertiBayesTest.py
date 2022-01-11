import unittest

from pomegranate.BayesianNetwork import BayesianNetwork

from com.florian.vertibayes.bayes.VertiBayes import VertiBayes

POPUlATION = 1000

class CentralStationTest(unittest.TestCase):
    def test_network(self):
        #Should result in the following network: x1 -> x2 -> x3
        vertiBayes = VertiBayes(POPUlATION, self._generateJSON())
        vertiBayes.defineLocalNetwork()
        vertiBayes.trainNetwork()
        network = vertiBayes.getNetwork()

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
        vertiBayes = VertiBayes(POPUlATION, self._generateJSONMissingVlaues())
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

        vertiBayes = VertiBayes(POPUlATION, self._generateJSONMultipleParents())
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

    def _generateJSON(self):
        #  Python formating fucking sucks... god forbid we actually have newlines
        return "[ { \"parents\": [], \"children\": [], \"uniquevalues\": [ \"0\", \"1\" ], \"name\": \"x1\", \"type\": \"number\", \"probabilities\": [ { \"localValue\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x1\", \"id\": null }, \"parents\": [], \"p\": 0.5 }, { \"localValue\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x1\", \"id\": null }, \"parents\": [], \"p\": 0.5 } ] }, { \"parents\": [ { \"parents\": [], \"children\": [], \"uniquevalues\": [ \"0\", \"1\" ], \"name\": \"x1\", \"type\": \"number\", \"probabilities\": [] }], \"children\": [], \"uniquevalues\": [ \"0\", \"1\" ], \"name\": \"x2\", \"type\": \"number\", \"probabilities\": [ { \"localValue\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x2\", \"id\": null }, \"parents\": [ { \"name\": \"x1\", \"value\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x1\", \"id\": null } }], \"p\": 0.8 }, { \"localValue\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x2\", \"id\": null }, \"parents\": [ { \"name\": \"x1\", \"value\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x1\", \"id\": null } }], \"p\": 0.2 }, { \"localValue\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x2\", \"id\": null }, \"parents\": [ { \"name\": \"x1\", \"value\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x1\", \"id\": null } }], \"p\": 0.2 }, { \"localValue\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x2\", \"id\": null }, \"parents\": [ { \"name\": \"x1\", \"value\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x1\", \"id\": null } }], \"p\": 0.8 } ] }, { \"parents\": [ { \"parents\": [ { \"parents\": [], \"children\": [], \"uniquevalues\": [ \"0\", \"1\" ], \"name\": \"x1\", \"type\": \"number\", \"probabilities\": [] }], \"children\": [], \"uniquevalues\": [ \"0\", \"1\" ], \"name\": \"x2\", \"type\": \"number\", \"probabilities\": [] }], \"children\": [], \"uniquevalues\": [ \"0\", \"1\" ], \"name\": \"x3\", \"type\": \"number\", \"probabilities\": [ { \"localValue\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x3\", \"id\": null }, \"parents\": [ { \"name\": \"x2\", \"value\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x2\", \"id\": null } }], \"p\": 0.8 }, { \"localValue\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x3\", \"id\": null }, \"parents\": [ { \"name\": \"x2\", \"value\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x2\", \"id\": null } }], \"p\": 0.2 }, { \"localValue\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x3\", \"id\": null }, \"parents\": [ { \"name\": \"x2\", \"value\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x2\", \"id\": null } }], \"p\": 0 }, { \"localValue\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x3\", \"id\": null }, \"parents\": [ { \"name\": \"x2\", \"value\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x2\", \"id\": null } }], \"p\": 1 } ] } ]"

    def _generateJSONMissingVlaues(self):
        #  Python formating fucking sucks... god forbid we actually have newlines
        return "[ { \"parents\": [], \"children\": [], \"uniquevalues\": [ \"0\", \"1\" ], \"name\": \"x1\", \"type\": \"number\", \"probabilities\": [ { \"localValue\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x1\", \"id\": null }, \"parents\": [], \"p\": 0.5 }, { \"localValue\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x1\", \"id\": null }, \"parents\": [], \"p\": 0.5 } ] }, { \"parents\": [ { \"parents\": [], \"children\": [], \"uniquevalues\": [ \"0\", \"1\" ], \"name\": \"x1\", \"type\": \"number\", \"probabilities\": [] } ], \"children\": [], \"uniquevalues\": [ \"0\", \"1\" ], \"name\": \"x2\", \"type\": \"number\", \"probabilities\": [ { \"localValue\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x2\", \"id\": null }, \"parents\": [ { \"name\": \"x1\", \"value\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x1\", \"id\": null } } ], \"p\": 0.8 }, { \"localValue\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x2\", \"id\": null }, \"parents\": [ { \"name\": \"x1\", \"value\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x1\", \"id\": null } } ], \"p\": 0.2 }, { \"localValue\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x2\", \"id\": null }, \"parents\": [ { \"name\": \"x1\", \"value\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x1\", \"id\": null } } ], \"p\": 0.2 }, { \"localValue\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x2\", \"id\": null }, \"parents\": [ { \"name\": \"x1\", \"value\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x1\", \"id\": null } } ], \"p\": 0.8 } ] }, { \"parents\": [ { \"parents\": [ { \"parents\": [], \"children\": [], \"uniquevalues\": [ \"0\", \"1\" ], \"name\": \"x1\", \"type\": \"number\", \"probabilities\": [] } ], \"children\": [], \"uniquevalues\": [ \"0\", \"1\" ], \"name\": \"x2\", \"type\": \"number\", \"probabilities\": [] } ], \"children\": [], \"uniquevalues\": [ \"0\", \"1\" ], \"name\": \"x3\", \"type\": \"number\", \"probabilities\": [ { \"localValue\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x3\", \"id\": null }, \"parents\": [ { \"name\": \"x2\", \"value\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x2\", \"id\": null } } ], \"p\": 0.7 }, { \"localValue\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x3\", \"id\": null }, \"parents\": [ { \"name\": \"x2\", \"value\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x2\", \"id\": null } } ], \"p\": 0.15 }, { \"localValue\": { \"type\": \"number\", \"value\": \"?\", \"attributeName\": \"x3\", \"id\": null }, \"parents\": [ { \"name\": \"x2\", \"value\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x2\", \"id\": null } } ], \"p\": 0.1 }, { \"localValue\": { \"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x3\", \"id\": null }, \"parents\": [ { \"name\": \"x2\", \"value\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x2\", \"id\": null } } ], \"p\": 0 }, { \"localValue\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x3\", \"id\": null }, \"parents\": [ { \"name\": \"x2\", \"value\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x2\", \"id\": null } } ], \"p\": 0.99 }, { \"localValue\": { \"type\": \"number\", \"value\": \"?\", \"attributeName\": \"x3\", \"id\": null }, \"parents\": [ { \"name\": \"x2\", \"value\": { \"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x2\", \"id\": null } } ], \"p\": 0.01 } ] } ]"

    def _generateJSONMultipleParents(self):
        return "[{\"parents\": [], \"children\": [], \"uniquevalues\": [\"0\", \"1\"], \"name\": \"x1\", \"type\": \"number\", \"probabilities\": [{\"localValue\": {\"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x1\", \"id\": null}, \"parents\": [], \"p\": 0.5}, {\"localValue\": {\"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x1\", \"id\": null}, \"parents\": [], \"p\": 0.5}]}, {\"parents\": [{\"parents\": [], \"children\": [], \"uniquevalues\": [\"0\", \"1\"], \"name\": \"x1\", \"type\": \"number\", \"probabilities\": []}], \"children\": [], \"uniquevalues\": [\"0\", \"1\"], \"name\": \"x2\", \"type\": \"number\", \"probabilities\": [{\"localValue\": {\"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x2\", \"id\": null}, \"parents\": [{\"name\": \"x1\", \"value\": {\"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x1\", \"id\": null}}], \"p\": 0.8}, {\"localValue\": {\"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x2\", \"id\": null}, \"parents\": [{\"name\": \"x1\", \"value\": {\"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x1\", \"id\": null}}], \"p\": 0.2}, {\"localValue\": {\"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x2\", \"id\": null}, \"parents\": [{\"name\": \"x1\", \"value\": {\"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x1\", \"id\": null}}], \"p\": 0.2}, {\"localValue\": {\"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x2\", \"id\": null}, \"parents\": [{\"name\": \"x1\", \"value\": {\"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x1\", \"id\": null}}], \"p\": 0.8}]}, {\"parents\": [{\"parents\": [{\"parents\": [], \"children\": [], \"uniquevalues\": [\"0\", \"1\"], \"name\": \"x1\", \"type\": \"number\", \"probabilities\": []}], \"children\": [], \"uniquevalues\": [\"0\", \"1\"], \"name\": \"x2\", \"type\": \"number\", \"probabilities\": []}, {\"parents\": [], \"children\": [], \"uniquevalues\": [\"0\", \"1\"], \"name\": \"x1\", \"type\": \"number\", \"probabilities\": []}], \"children\": [], \"uniquevalues\": [\"0\", \"1\"], \"name\": \"x3\", \"type\": \"number\", \"probabilities\": [{\"localValue\": {\"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x3\", \"id\": null}, \"parents\": [{\"name\": \"x2\", \"value\": {\"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x2\", \"id\": null}}], \"p\": 0.8}, {\"localValue\": {\"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x3\", \"id\": null}, \"parents\": [{\"name\": \"x2\", \"value\": {\"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x2\", \"id\": null}}], \"p\": 0.2}, {\"localValue\": {\"type\": \"number\", \"value\": \"0\", \"attributeName\": \"x3\", \"id\": null}, \"parents\": [{\"name\": \"x2\", \"value\": {\"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x2\", \"id\": null}}], \"p\": 0}, {\"localValue\": {\"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x3\", \"id\": null}, \"parents\": [{\"name\": \"x2\", \"value\": {\"type\": \"number\", \"value\": \"1\", \"attributeName\": \"x2\", \"id\": null}}], \"p\": 1}]}]"