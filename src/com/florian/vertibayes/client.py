import vantage6.client

IMAGE = 'carrrier-harbor.carrier-mu.src.surf-hosted.nl/carrier/vertibayes'
NAME = 'vertibayes from client'

INITIAL_NETWORK = [
    {
        "parents": [],
        "name": "x1",
        "type": "number"
    }, {
        "parents": ["x1"],
        "name": "x2",
        "type": "number"
    }, {
        "parents": ["x2"],
        "name": "x3",
        "type": "number"
    }
]


class VertibayesClient:

    def __init__(self, client: vantage6.client.Client):
        """

        :param client: Vantage6 client
        """
        self.client = client

    def vertibayes(self, collaboration, commodity_node, nodes, population):
        return self.client.task.create(collaboration=collaboration,
                                       organizations=[commodity_node],
                                       name=NAME, image=IMAGE, description=NAME,
                                       input={'method': 'vertibayes', 'master': True,
                                              'args': [nodes, INITIAL_NETWORK, population]})
