# from graphviz import Digraph


class DebruijinGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()  # directed set of tuples (source, destination)
        self.naive_eulerian_path = None
        self.smart_eulerian_path = None

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

    def get_overlap(self, left, right):
        score = 0
        for l, r in zip(reversed(left), right):
            if(l == r):
                score += 1
        return score

    def find_naive_eulerian_path(self):
        """ find the eulerian path using a naive algorithm """
        path = ""
        merged_nodes = set()
        for i in self.nodes:
            merged_nodes.add(i)

        while(len(merged_nodes) != 0):
            current_node = merged_node.pop()
            max_overlap_score = -1
            max_overlap_node = None
            for i in merged_nodes:
                left_overlap = self.get_overlap(i, current_node)
                right_overlap = self.get_overlap(current_node, i)
                left_overlap_score = left_overlap[0]
                right_overlap_score = right_overlap[0]
                if(left_overlap_score < right_overlap_score):
                    max_overlap_score = right_overlap_score
                    max_overlap_node = (i, current_node)
                else:
                    max_overlap_score = left_overlap_score
                    max_overlap_node = (current_node, i)

            merged_nodes.remove(max_overlap_node[0])
            merged_nodes.remove(max_overlap_node[1])
            merged_nodes.add(max_overlap_node[0][:len(max_overlap_node[0]) - max_overlap_score]
                             + max_overlap_node[1][max_overlap_score:])

        self.naive_eulerian_path = path

    def find_smart_eulerian_path(self):
        """ find the eulerian path using a smart algorithm """
        path = ""
        self.smart_eulerian_path = path


if __name__ == "__main__":
    a = "aaaabcdefghijk"
    g = dirGraph()
    g.initializeDebruijinGraph(a, 3)
    g.printGraph()
