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
    df_size = seq.df.shape[0]
    df_size = 1000
    for i in xrange(N_THREADS):
        start, end = findWorkerThreadIndices(i, df_size)
        thread_arr[i] = Process(target=makeGraphs, args=(i, start, end, k, seq.df, shared_dict))
        thread_arr[i].start()
        # logging.info("starting thread %s", repr(i))
    for i in xrange(N_THREADS):
        thread_arr[i].join()
        # logging.info("joining thread %s", repr(i))
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

def makeGraphs(threadNum, start, end, k, df, shared_dict):
    graphList = []
    for i in range(start, end):
        s = df['sequence'].iloc[i]
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

# debroin = Sequences(N_THREADS, FILENAME)
# print(debroin.df.shape[0])

# threeMerGraphList = getGraphList(debroin, 3)
# threeMerGraphList = getGraphList_noParallel(debroin, 3)
# print(len(threeMerGraphList))


if __name__ == "__main__":
    N_THREADS = 20
    FILENAME = 'Chelonoidis_abingdonii.ASM359739v1.pep.abinitio.fa'
    SEQ = Sequences(N_THREADS, FILENAME)

    S3 = "abccde"
    G3 = DebruijinGraph(S3, 5)
    SEQ.logger.info("finding the eulerian path of %s using a naive greedy algorithm", S3)
    G3.find_naive_eulerian_path()
    SEQ.logger.info("completed")
    SEQ.logger.info("path is %s", G3.naive_eulerian_path)
    SEQ.logger.info("finding the eulerian path of %s using a smart O(V + E) algorithm", S3)
    G3.find_smart_eulerian_path()
    SEQ.logger.info("completed")
    SEQ.logger.info("path is %s", G3.smart_eulerian_path)

    S4 = "0011101000"
    G4 = DebruijinGraph(S4, 3)
    SEQ.logger.info("finding the eulerian path of %s using a naive greedy algorithm", S4)
    G4.find_naive_eulerian_path()
    SEQ.logger.info("completed")
    SEQ.logger.info("path is %s", G4.naive_eulerian_path)
    SEQ.logger.info("finding the eulerian path of %s using a smart O(V + E) algorithm", S4)
    G4.find_smart_eulerian_path()
    SEQ.logger.info("completed")
    SEQ.logger.info("path is %s", G4.smart_eulerian_path)

    K = 30
    SEQ.logger.info("build %s-mer graph", K)
    graph_list = getGraphList(SEQ, K)
    # MARK: debug 
    # graph_list = []

    for counter, i in enumerate(graph_list):
        cur_seq = i.sequence.lower()
        # SEQ.logger.info("finding the eulerian path of %s using a smart O(V + E) algorithm", cur_seq)
        i.find_smart_eulerian_path()
        # SEQ.logger.info("completed")
        cur_path = i.smart_eulerian_path.lower()
        # SEQ.logger.info("path is %s", cur_path)
        if(cur_path != cur_seq):
            print(counter)
            SEQ.logger.error("seq  in %s", cur_seq)
            SEQ.logger.error("path is %s", cur_path)
            SEQ.logger.error("the sequence and path differ")
            exit(-1)
