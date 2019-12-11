import os

import nltk
from nltk.corpus.reader import PlaintextCorpusReader

corpus_dir = os.path.expanduser('~/finalProject/enron_data_processed/')

#returns the enron plaintext corpus
def enronCorpus():
    #get all fileids
    file_id_list = []
    for relation in os.listdir(corpus_dir):
        if(os.path.isfile(os.path.join(corpus_dir, relation))):
            tmp_corpus_file = os.path.join(corpus_dir, relation)
            file_id_list.append(relation)
    #make a corpus    
    corpus = PlaintextCorpusReader(corpus_dir, file_id_list)
    
    return corpus


    