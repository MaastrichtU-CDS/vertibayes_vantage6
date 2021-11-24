## Vertibayes
This is the python half of the vertibayes implementation for Vantage6

This docker container depends on two other containers:
1) The java vertibayes container, which uses the n-party-scalar-product protocol for the federated aspect
2) The endpoint-collector container, which is needed to coordinate the node to node communication within vantage6

This container works as follows:

1) Start the java container at all relevant parties. Including a commodity server
2) use the endpoint-collector to share the relevant urls
3) Use the java container to learn the maximum likelihood for a predefined network structur, treating the values as discrete
4) Based on the learned maximum likelihood learned in the previous step, generate synthetic data
5) Learn bayesian network, using the predefined structure, on the synthetic data
6) Return this network

The final bayesian network is learned using the pgmpy library (https://pgmpy.org/index.html)

Vantage6 request:

```
POPULATION =<Synthetic population size>
NODES=<Predefined network structure>
    
task = client.post_task(
    name="vertibayesPython",
    image="docker build -t carrier-harbor2.carrier-mu.surf-hosted.nl/florian-project/vertibayesPython",
    collaboration_id=1,
    input_={'method': 'vertibayes', 'master': True,
            'kwargs': {'population':POPULATION, 'nodes':NODES , 'exclude_orgs': exclude_orgs}},
    organization_ids=[1]
)
```

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