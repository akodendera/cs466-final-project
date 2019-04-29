import pprint
from Bio import SeqIO
import pandas as pd
from tabulate import tabulate
import logging
from multiprocessing import Process, Manager
import os
import threading
import time
from math import ceil

pp = pprint.PrettyPrinter(indent=4)


class DeBruijn:
    def __init__(self, n_threads, filename):
        self.FILENAME = filename
        self.N_THREADS = n_threads
        self.mgr = Manager()
        self.shared_dict = self.mgr.dict()
        self.thread_arr = [None] * n_threads
        self.initialize_logs()
        self.initialize_dataframes()
        self.import_file()

    def initialize_logs(self):
        FORMAT = "%(asctime)s: %(message)s"
        logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt="%H:%M:%S")
        logging.info("Logging initilazied")

    def initialize_dataframes(self):
        self.df = pd.DataFrame()

    def import_file(self):
        split_arr = self.split_array()
        logging.info("split into " + repr(len(split_arr)))
        for i in xrange(self.N_THREADS):
            self.thread_arr[i] = Process(target=self.append_parallel, args=(i, split_arr[i], self.shared_dict))
            self.thread_arr[i].start()
            logging.info("starting thread " + repr(i))

        for i in xrange(self.N_THREADS):
            self.thread_arr[i].join()
            logging.info("joining thread " + repr(i))

        for i in xrange(self.N_THREADS):
            self.df = self.df.append(self.shared_dict[i])

    def append_parallel(self, index, arr, parent_shared_dict):
        # MARK: log length
        # logging.info("length of chunk for thread " + repr(index) + " is " + repr(len(arr)))
        progress_counter = 0
        for record in arr:
            self.df = self.df.append({
                'sequence_id': record.id,
                'sequence': str(record.seq)
            }, ignore_index=True)
            # MARK: progress log
            # if(progress_counter % (len(arr) / 10) == 0):
            #     logging.info("thread " + repr(index) + " is " + repr(int(ceil(100 * float(progress_counter) / len(arr)))) + "% done")
            # progress_counter += 1
        parent_shared_dict[index] = self.df

    def split_array(self):
        split_arr = []
        split_arr_index = 0
        current_arr = []

        arr = SeqIO.parse(open(self.FILENAME), 'fasta')
        arr_len = sum(1 for _ in arr)

        arr = SeqIO.parse(open(self.FILENAME), 'fasta')
        for i, v in enumerate(arr):
            if(i != 0 and i % (arr_len / self.N_THREADS) == 0):
                split_arr.append(current_arr)
                current_arr = [v]
                split_arr_index += 1
            else:
                current_arr.append(v)
        # When the number of thread requested is 1 then it will
        # not be appended in a for-loop
        if not split_arr:
            split_arr = [current_arr]
        return split_arr


if __name__ == "__main__":
    N_THREADS = 20
    FILENAME = 'Chelonoidis_abingdonii.ASM359739v1.pep.abinitio.fa'
    debroin = DeBruijn(N_THREADS, FILENAME)
    print(debroin.df.shape)
