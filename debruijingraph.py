import networkx as nx
import matplotlib.pyplot as plt
from random import shuffle
from multiprocessing import Process, Manager
import logging
from sequences import Sequences


class DebruijinGraph:
    def __init__(self, sequence, k):
        self.nodes = set()
        self.edgeSet = set()  # directed set of tuples (source, destination)
        self.adjDict = {}
        self.read_size = k
        self.sequence = sequence
        self.initializeDebruijinGraph(sequence, k)
        self.naive_eulerian_path = None
        self.smart_eulerian_path = None

    def addNode(self, node):
        self.nodes.add(node.lower())
        if node.lower() not in self.adjDict:
            self.adjDict[node.lower()] = []

    def addEdge(self, sourceNode, destinationNode):
        self.addNode(sourceNode)
        self.addNode(destinationNode)
        self.edgeSet.add((sourceNode.lower(), destinationNode.lower()))
        self.adjDict[sourceNode.lower()].append(destinationNode.lower())

    def printGraph(self):
        # for n in self.nodes:
        #     edgeList = ""
        #     for s, d in self.edgeSet:
        #         if s == n:
        #             edgeList += d + ", "
        #     print("node: {} edges: {}".format(n, repr(edgeList)))
        print(self.adjDict)

    
    def visualize(self, filename):
        g = nx.MultiDiGraph()
        g.add_nodes_from(self.nodes)
        for n in self.adjDict:
            for e in self.adjDict[n]:
                g.add_edge(n, e)
        nx.draw(g, with_labels=True)
        plt.savefig(filename)

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
        max_score = 0
        # print("checking overlap of " + repr(left) + " and " + repr(right))
        # 10 and 11
        for cur_score in range(1, min(len(left), len(right)) + 1):
            cur_alignment_score = 0
            for cur_align_index in range(cur_score):
                if(left[len(left) - cur_score + cur_align_index] == right[cur_align_index]):
                    # print("increase overlap")
                    cur_alignment_score += 1
                else:
                    # print("no more overlap")
                    break
            if cur_alignment_score != cur_score:
                cur_alignment_score = 0

            max_score = max(max_score, cur_alignment_score)
            # print("current max score is " + repr(max_score))

        # for cur_alignment_index in range(self.read_size - 2):
        #     if(left[len(left) - (self.read_size - 2) + cur_alignment_index] == right[cur_alignment_index]):
        #         # print("increase overlap")
        #         max_score += 1
        #     else:
        #         # print("no more overlap")
        #         break

        # if(max_score < self.read_size - 2):
        #     max_score = 0
        return max_score

    def find_naive_eulerian_path(self):
        """ find the eulerian path using a naive algorithm """
        merged_nodes = []
        for i in self.nodes:
            merged_nodes.append(i)
        for i in self.adjDict:
            for j in self.adjDict[i]:
                merged_nodes.append(j)

        while(len(merged_nodes) != 1):
            shuffle(merged_nodes)
            current_node = merged_nodes.pop()
            # print("starting merge")
            # print(repr(current_node))
            max_overlap_score = -1
            max_overlap_node = None
            for i in merged_nodes:
                left_overlap_score = self.get_overlap(i, current_node)
                right_overlap_score = self.get_overlap(current_node, i)
                if(max_overlap_score < max(left_overlap_score, right_overlap_score)):
                    if(left_overlap_score < right_overlap_score):
                        max_overlap_score = right_overlap_score
                        max_overlap_node = (current_node, i)
                    else:
                        max_overlap_score = left_overlap_score
                        max_overlap_node = (i, current_node)
            # if max_overlap_score < self.read_size - 2:
            if max_overlap_score == -1:
                # print("could not merge any more")
                return

            # print("merging " + repr(max_overlap_node) + " with a score of " + repr(max_overlap_score))
            if(max_overlap_node[0] == current_node):
                merged_nodes.remove(max_overlap_node[1])
            else:
                merged_nodes.remove(max_overlap_node[0])

            merged_nodes.append(max_overlap_node[0] + max_overlap_node[1][max_overlap_score:])
            # print("new node " + repr(max_overlap_node[0] + max_overlap_node[1][max_overlap_score:]))

        result = merged_nodes.pop()
        if(self.is_eulerian(result)):
            self.naive_eulerian_path = result
        else:
            self.naive_eulerian_path = "The naive greedy algorithm failed to find a eulerian path"

    def is_eulerian(self, path):
        kmer_list = self.getkmerList(path, self.read_size)
        for i in kmer_list:
            lmer, rmer = self.getLeftRightMers(i)
            if((lmer,rmer) not in self.edgeSet):
                return False
        return len(path) == len(self.sequence)

    def find_smart_eulerian_path(self):
        """ find the eulerian path using a smart algorithm """
        path_nodes = []
        path_edges = dict()
        for i in self.nodes:
            path_nodes.append(i)
        for i in self.adjDict:
            if(len(self.adjDict[i]) > 0):
                path_edges[i] = self.adjDict[i]

        starting_vertex_candidate = []
        for i in path_nodes:
            outgoing_edges = 0
            incoming_edges = 0

            if(i in path_edges):
                outgoing_edges = len(path_edges[i])
            for j in path_edges:
                for k in path_edges[j]:
                    if(i == k):
                        incoming_edges += 1
            if((outgoing_edges - incoming_edges) > 0 and
                (outgoing_edges - incoming_edges) % 2 != 0):
                for j in path_edges[i]:
                    starting_vertex_candidate.append(i)
        if(not starting_vertex_candidate):
            for i in path_nodes:
                starting_vertex_candidate.append(i)

        current_path = []
        current_vertex = starting_vertex_candidate.pop()
        not_visited = []
        not_visited.append(current_vertex)
        while(not_visited):
            if(current_vertex in path_edges):
                not_visited.append(current_vertex)
                new_vertex = path_edges[current_vertex].pop()
                if(current_vertex in path_edges):
                    if(len(path_edges[current_vertex]) == 0):
                        path_edges.pop(current_vertex)
                current_vertex = new_vertex
            else:
                current_path.append(current_vertex)
                current_vertex = not_visited.pop()

        merged_node = ""
        for i in reversed(current_path):
            merged_node += i[0]
        merged_node += current_path[0][1:]
        self.smart_eulerian_path = merged_node


def getGraphList(N_THREADS, seq, k):
    FORMAT = "%(asctime)s: %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Logging initilazied")

    graphs = []
    thread_arr = [None] * N_THREADS
    mgr = Manager()
    shared_dict = mgr.dict()
    df_size = seq.df.shape[0]
    # df_size = 10000
    for i in range(N_THREADS):
        start, end = findWorkerThreadIndices(i, N_THREADS, df_size)
        logging.info("thread start: %s. thread end: %s", start, end)
        thread_arr[i] = Process(target=makeGraphs, args=(i, start, end, k, seq.df, shared_dict))
        thread_arr[i].start()
        logging.info("starting thread %s", repr(i))
    for i in range(N_THREADS):
        thread_arr[i].join()
        logging.info("joining thread %s", repr(i))
    for i in range(N_THREADS):
        graphs.extend(shared_dict[i])
    return graphs


def findWorkerThreadIndices(threadNum, N_THREADS, dfSize):
    start = (dfSize // N_THREADS) * threadNum
    end = (dfSize // N_THREADS) * threadNum + (dfSize // N_THREADS)
    if threadNum + 1 == N_THREADS:
        end = dfSize
    return start, end


def makeGraphs(threadNum, start, end, k, df, shared_dict):
    graphList = []
    for i in range(start, end):
        s = df.iloc[i]['sequence']
        graphList.append(DebruijinGraph(s, k))
    if(graphList == None):
        logging.info("IS NONE OH NO AHH")
    shared_dict[threadNum] = graphList 


def getGraphList_noParallel(seq, k):
    df_size = seq.df.shape[0]
    # df_size = 10000
    graphs = []
    for i in range(df_size):
        s = seq.df['sequence'].iloc[i]
        graphs.append(DebruijinGraph(s, k))
    return graphs
