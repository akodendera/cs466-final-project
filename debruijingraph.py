# from graphviz import Digraph

class DebruijinGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()  # directed set of tuples (source, destination)

    def addNode(self, n):
        self.nodes.add(n.lower())

    def addEdge(self, sourceNode, destinationNode):
        if sourceNode not in self.nodes:
            self.addNode(sourceNode)
        if destinationNode not in self.nodes:
            self.addNode(destinationNode)
        self.edges.add((sourceNode.lower(), destinationNode.lower()))

    def printGraph(self):
        for n in self.nodes:
            edgeList = ""
            for s, d in self.edges:
                if s == n:
                    edgeList += d + ", "
            print("node: {} edges: {}".format(n, repr(edgeList)))

    def initializeDebruijinGraph(self, sequence, k):
        mers = self.getkmerList(sequence, k)
        for m in mers:
            lmer, rmer = self.getLeftRightMers(m)
            self.addEdge(lmer, rmer)
        
    def getkmerList(self, sequence, k):
        merList = []
        for x in range(len(sequence)-k+1):
            merList.append(sequence[x:x+k])
        return merList

    def getLeftRightMers(self, s):
        return s[:len(s)-1], s[1:]

    def printWarning(self, s):
        print("Warning: {}".format(s))


# if __name__ == "__main__":