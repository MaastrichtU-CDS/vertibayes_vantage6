## Vertibayes
This is the python wrapper of the vertibayes implementation for Vantage6

This docker container depends a java spring boot project, which uses the n-party-scalar-product protocol for the federated aspect
This container will start the java project at every data station, then communicates the ip-adresses to each of them. After this it will run vertibayes.
Once this is done it will kill the spring projects to ensure the containers close and return the output to the researcher.
For more details on the spring project see: https://gitlab.com/fvandaalen/vertibayes

The images corresponding to this container are:
harbor.carrier-mu.src.surf-hosted.nl/carrier/vertibayes:2.1

It uses the openmarkov response from Vertibayes by default.

Vantage6 request:

```
nodes=<Data-owner nodes>
NETWORK=<Predefined network structure, may be left None>
COMMODITYSERVER=<Organisation selected to play the role of commodity server>
minPercentage=<minimum percentage used for binning scheme, 0.1, 0.25, 0.3 or 0.4>
targetVariable=<the class variable>
folds=<number of folds for crossfold validation, max 10, min 1>
trainStructure=<flag to indicate if structure learning should be applied. This can be on top of a predefined structure>
    
task = self.client.task.create(collaboration=collaboration,
                                           organizations=[commodity_node],
                                           name=NAME, image=IMAGE, description=NAME,
                                           input={'method': 'vertibayes', 'master': True,
                                                  'args': [nodes, INITIAL_NETWORK, targetVariable, minPercentage, folds, trainStructure]})
)
```
An example can also be found in client.py


The predefined network structure must resemble the following:
```
{[
      {
      "parents": [],
      "children": [],
      "uniquevalues":       [
         "0",
         "1"
      ],
      "name": "x1",
      "type": "number",
      "probabilities": []
   },
      {
      "parents": [      {
         "parents": [],
         "children": [],
         "uniquevalues":          [
            "0",
            "1"
         ],
         "name": "x1",
         "type": "number",
         "probabilities": []
      }],
      "children": [],
      "uniquevalues":       [
         "0",
         "1"
      ],
      "name": "x2",
      "type": "number",
      "probabilities": []
   },
      {
      "parents": [      {
         "parents": [         {
            "parents": [],
            "children": [],
            "uniquevalues":             [
               "0",
               "1"
            ],
            "name": "x1",
            "type": "number",
            "probabilities": []
         }],
         "children": [],
         "uniquevalues":          [
            "0",
            "1"
         ],
         "name": "x2",
         "type": "number",
         "probabilities": []
      }],
      "children": [],
      "uniquevalues":       [
         "0",
         "1"
      ],
      "name": "x3",
      "type": "number",
      "probabilities": []
   }
]}

```
