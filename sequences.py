import pprint
import logging
from multiprocessing import Process, Manager
from Bio import SeqIO
import pandas as pd

PP = pprint.PrettyPrinter(indent=4)


class Sequences:
    def __init__(self, n_threads, filename):
        self.FILENAME = filename
        self.N_THREADS = n_threads
        self.mgr = Manager()
        self.df = None
        self.shared_dict = self.mgr.dict()
        self.thread_arr = [None] * n_threads
        self.initialize_logs()
        self.initialize_dataframes([])
        self.import_file()

    def initialize_logs(self):
        """ Initialize the logging format """
        FORMAT = "%(asctime)s: %(message)s"
        logging.basicConfig(format=FORMAT, level=logging.INFO,
                            datefmt="%H:%M:%S")
        logging.info("Logging initialized")

    def initialize_dataframes(self, row_arr):
        """ Initialize the dataframe from a list"""
        self.df = pd.DataFrame(row_arr)

    def import_file(self):
        """ Parallelly import the file into a pandas dataframe """
        split_arr = self.split_into_chunks()
        logging.info("split into %s", repr(len(split_arr)))
        # call worker threads
        for i in xrange(self.N_THREADS):
            self.thread_arr[i] = Process(target=self.append_parallel,
                                         args=(i, split_arr[i]))
            self.thread_arr[i].start()
            # logging.info("starting thread %s", repr(i))

        # join worker threads
        for i in xrange(self.N_THREADS):
            self.thread_arr[i].join()
            # logging.info("joining thread %s", repr(i))

        # merge the dataframes that the worker threads created
        # in a serial manner
        self.df = pd.concat(self.shared_dict.values(), axis=0, join='outer',
                            ignore_index=True)

    def append_parallel(self, index, arr):
        """
        Parallell worker function that adds to local dict
        and copies to shared dict
        """
        row_arr = []
        for record in arr:
            current_dict = {
                'sequence_id': record.id,
                'sequence': str(record.seq)
            }
            row_arr.append(current_dict)

        self.initialize_dataframes(row_arr)
        self.shared_dict[index] = self.df

    def split_into_chunks(self):
        """ Split the SeqIO generator into N_THREADS chunks """
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
        # not be appended in the above for-loop
        if not split_arr:
            split_arr = [current_arr]
        elif current_arr:
            split_arr[len(split_arr) - 1].extend(current_arr)
        return split_arr

if __name__ == "__main__":
    N_THREADS = 20
    FILENAME = 'Chelonoidis_abingdonii.ASM359739v1.pep.abinitio.fa'
    debroin = DeBruijn(N_THREADS, FILENAME)
    print(debroin.df.shape)
