class VertiBayes:

    def generateOutputCSV(self, network):
        # Function to generate a CSV based on the network generated.
        # This generation is needed to provide the controllers at CBS something to work with.
        # This little script should probably be moved to the researcher at some point.
        import csv

        # open the file in the write mode
        f = open('output.csv', 'w', newline='')
        # create the csv writer
        writer = csv.writer(f)
        nodes =  network.get('nodes')
        for node in nodes:
            header = []
            header.append("Variable: " + node.get('name'))
            writer.writerow(header)

            parents = node.get('parents')
            values = self.getNodeValues(node)

            table = []

            for parent in parents:
                row = []
                row.append(parent)
                table.append(row)

            for value in values:
                row = []
                row.append(value)
                table.append(row)

            for probability in node.get('probabilities'):
                for i in range(0, len(parents)):
                    row = table[i]
                    name = row[0]
                    for parentValue in probability.get('parentValues'):
                        if name == parentValue.get('parent'):
                            parentNode = self._findNode(name, nodes)
                            row.append(self.getLocalValue(parentNode,parentValue.get('value')))
                for i in range(len(parents), len(table)):
                    row = table[i]
                    name = row[0]
                    if name == self.getLocalValue(node,probability.get('localValue')):
                        row.append(probability.get('p'))

            for row in table:
               writer.writerow(row)
            emptyline = []

            writer.writerow(emptyline)
            writer.writerow(emptyline)
            writer.writerow(emptyline)

        # close the file.
        f.close()

    def _findNode(self, name, nodes):
        for node in nodes:
            if node.get('name') == name:
                return node

    def getNodeValues(self, node):
        values = []
        for probability in node.get('probabilities'):
                value = self.getLocalValue(node, probability.get('localValue'))
                values.append(value)
        return values

    def getLocalValue(self, node, localValue):
        value = ""
        if node.get('type') == "string":
            value = localValue.get('localValue')
        else:
            value = "(" + localValue.get('lowerLimit') + ";" +localValue.get("upperLimit") + ")"
        return value


def _findSliblings(self, probability, probabilities):
    sliblings = []
    for p in probabilities:
        if (p.get('parentValues') == probability.get('parentValues')):
            sliblings.append(p)
    return sliblings
