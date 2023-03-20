import vantage6.client

IMAGE = 'harbor.carrier-mu.src.surf-hosted.nl/carrier/vertibayes:3.0'
NAME = 'vertibayes from client'

# Example contains nodes of all three types:
# numeric: Integers
# real: real numbers
# string: other

INITIAL_NETWORK = [ {
    "parents" : [ ],
    "name" : "x1",
    "type" : "numeric",
    "probabilities" : [ ],
    "bins" : [ {
      "upperLimit" : "1.5",
      "lowerLimit" : "0.5"
    }, {
      "upperLimit" : "0.5",
      "lowerLimit" : "-1"
    }, {
      "upperLimit" : "?",
      "lowerLimit" : "?"
    } ],
    "discrete" : True
  }, {
    "parents" : [ "x1" ],
    "name" : "x2",
    "type" : "real",
    "probabilities" : [ ],
    "bins" : [ {
      "upperLimit" : "1.5",
      "lowerLimit" : "0.5"
    }, {
      "upperLimit" : "0.5",
      "lowerLimit" : "-1"
    }, {
      "upperLimit" : "?",
      "lowerLimit" : "?"
    } ],
    "discrete" : False
  }, {
    "parents" : [ "x2","x1" ],
    "name" : "x3",
    "type" : "string",
    "probabilities" : [ ],
    "bins" : [ ],
    "discrete" : True
  } ]


class VertibayesClient:

    def __init__(self, client: vantage6.client.Client):
        """

        :param client: Vantage6 client
        """
        self.client = client

    def vertibayes(self, collaboration, commodity_node, nodes, targetVariable, minPercentage, folds, trainStructure):
            return self.client.task.create(collaboration=collaboration,
                                           organizations=[commodity_node],
                                           name=NAME, image=IMAGE, description=NAME,
                                           input={'method': 'vertibayes', 'master': True,
                                                  'args': [nodes, INITIAL_NETWORK, targetVariable, minPercentage, folds, trainStructure]})

    def vertibayesNoInitialNetwork(self, collaboration, commodity_node, nodes, targetVariable, minPercentage, folds, trainStructure):
            return self.client.task.create(collaboration=collaboration,
                                           organizations=[commodity_node],
                                           name=NAME, image=IMAGE, description=NAME,
                                           input={'method': 'vertibayes', 'master': True,
                                                  'args': [nodes, None, targetVariable, minPercentage, folds, trainStructure]})
