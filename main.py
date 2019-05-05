from sequences import Sequences
from debruijingraph import *

if __name__ == "__main__":
    N_THREADS = 5
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

    K = 3
    SEQ.logger.info("build %s-mer graph", K)
    graph_list = getGraphList(N_THREADS, SEQ, K)
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
