import os
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

corpus_dir = os.path.expanduser('~/finalProject/enron_data_processed/')

newcorpus = PlaintextCorpusReader(corpusdir, '.*', encoding='latin-1')
