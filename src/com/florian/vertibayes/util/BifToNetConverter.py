import xmltodict

def findStates(name, variables):
    for var in variables['Variable']:
        if var['@name'] == name:
            return len(var["States"]['State'])

def mapBif(bif):
    dict = xmltodict.parse(bif)['ProbModelXML']['ProbNet']
    net = "net{}";
    for var in dict['Variables']['Variable']:
        net += " node " + var['@name'] + " { states = ( "
        if len(var["States"]['State']) == 1:
            net += var["States"]['State']['@name']
        else:
            for state in var["States"]['State']:
                net += "\"" + state['@name'] + "\" "

        net+=");}"

    for pot in dict['Potentials']['Potential']:
        net += "potential ( "
        parents = []
        if len(pot['Variables']['Variable']) == 1:
            net += pot['Variables']['Variable']['@name']
            name =  pot['Variables']['Variable']['@name']
        else:
            name =  pot['Variables']['Variable'][0]['@name']
            count = 0
            for var in pot['Variables']['Variable']:
                if name != var['@name']:
                    parents.append(var['@name'])
                net+=var['@name']
                if count < len(pot['Variables']['Variable'])-1:
                    net += " "
                if count == 0:
                    net += "| "
                count += 1
        net+=    " ) {  data = "

        potentials = pot['Values'].split(" ")
        states = findStates(name, dict['Variables'])
        for i in range(0, len(potentials)):
            if i % states == 0:
                    potentials[i] = "(" + potentials[i]
            if i % states == states-1:
                potentials[i] = potentials[i] + ")"
        for parent in reversed(parents):
            parentStates = findStates(parent, dict['Variables'])
            states = states * parentStates
            for i in range(0, len(potentials)):
                if i % states == 0:
                    potentials[i] = "(" + potentials[i]
                if i % states == states-1:
                    potentials[i] = potentials[i] + ")"
        pot = ""
        for i in range(0, len(potentials)):
            pot+= potentials[i]
            if(i < len(potentials)-1):
                pot += " "
        pot = pot.replace(") (", ")(")
        net += pot
        net+=" ;}"
    return net



