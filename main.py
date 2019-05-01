from sequences import Sequences
from debruijingraph import DebruijinGraph
from multiprocessing import Process, Manager
import logging

def getGraphList(seq, k):

    FORMAT = "%(asctime)s: %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Logging initilazied")

    graphs = []
    thread_arr = [None] * N_THREADS
    mgr = Manager()
    shared_dict = mgr.dict()
    shared_dict["df"] = seq.df
    df_size = seq.df.shape[0]
    df_size = 1000
    for i in xrange(N_THREADS):
        start, end = findWorkerThreadIndices(i, df_size)
        thread_arr[i] = Process(target=makeGraphs, args=(i, start, end, k, shared_dict))
        thread_arr[i].start()
        logging.info("starting thread %s", repr(i))
    for i in xrange(N_THREADS):
        thread_arr[i].join()
        logging.info("joining thread %s", repr(i))
    for i in xrange(N_THREADS):
        graphs.extend(shared_dict[i])
    return graphs

def findWorkerThreadIndices(threadNum, dfSize):
    start = (dfSize/N_THREADS) * threadNum
    end = (dfSize/N_THREADS) * threadNum + (dfSize/N_THREADS)
    if threadNum + 1 == N_THREADS:
        end = dfSize - 1
    return start, end

def makeGraphsTemp(threadNum, start, end, k, shared_dict):
    graphList = []
    for i in range(start, end):
        graphList.append("abbas")
    shared_dict[threadNum] = graphList

def makeGraphs(threadNum, start, end, k, shared_dict):
    graphList = []
    for i in range(start, end):
        s = shared_dict["df"]['sequence'].iloc[i]
        graphList.append(DebruijinGraph(s, k))
    shared_dict[threadNum] = graphList 

def getGraphList_noParallel(seq, k):
    df_size = seq.df.shape[0]
    df_size = 10000
    graphs = []
    for i in range(df_size):
        s = seq.df['sequence'].iloc[i]
        graphs.append(DebruijinGraph(s, k))
    return graphs

def getGraphList_noParallel(seq, k):
    df_size = seq.df.shape[0]
    graphs = []
    for i in range(df_size):
        s = seq["df"]['sequence'].iloc[i]
        graphs.append(DebruijinGraph(s, k))
    return graphs

# N_THREADS = 4
# FILENAME = 'Chelonoidis_abingdonii.ASM359739v1.pep.abinitio.fa'
# debroin = Sequences(N_THREADS, FILENAME)
# print(debroin.df.shape[0])

# threeMerGraphList = getGraphList(debroin, 3)
# threeMerGraphList = getGraphList_noParallel(debroin, 3)
# print(len(threeMerGraphList))

s3 = "abccde"
g3 = DebruijinGraph(s3, 4)
g3.printGraph()

g3.find_naive_eulerian_path()
print("finding the eulerian path of {} using a naive greedy algorithm".format(s3))
print(repr(g3.naive_eulerian_path))

s4 = "0011101000"
g4 = DebruijinGraph(s4, 3)
g4.printGraph()

g4.find_naive_eulerian_path()
print("finding the eulerian path of {} using a naive greedy algorithm".format(s4))
print(repr(g4.naive_eulerian_path))


