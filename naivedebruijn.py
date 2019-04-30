def getkmerList(sequence, k):
    merList = []
    for x in range(len(sequence)-k+1):
        merList.append(sequence[x:x+k])
    return merList


def getLeftRightMers(s):
    return s[:len(s)-1], s[1:]


def printWarning(s):
    print("Warning: {}".format(s))


class dirGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()  # directed set of tuples (source, destination)

    def addNode(self, n):
        self.nodes.add(n.lower())

    def addEdge(self, sourceNode, destinationNode):
        if sourceNode not in self.nodes:
            self.nodes.add(sourceNode)
            printWarning("adding edge where source node not in graph. \
                          Adding node: " + sourceNode + " to graph")
        if destinationNode not in self.nodes:
            self.nodes.add(destinationNode)
            printWarning("adding edge where destination node not in graph. \
                          Adding node: " + destinationNode + " to graph")
        self.edges.add((sourceNode.lower(), destinationNode.lower()))

    def printGraph(self):
        for n in self.nodes:
            edgeList = ""
            for s, d in self.edges:
                if s == n:
                    edgeList += d + ", "
            print("node: {} edges: {}".format(n, repr(edgeList)))


def makeDebruijinGraph(sequence, k):
    g = dirGraph()
    mers = getkmerList(sequence, k)
    for m in mers:
        lmer, rmer = getLeftRightMers(m)
        g.addEdge(lmer, rmer)
    return g

if __name__ == "__main__":
    s = "abcdefgcdadem"
    g = makeDebruijinGraph(s, 3)
    g.printGraph()
