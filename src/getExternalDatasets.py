import os
import re, string
import random
import nltk
from nltk.corpus import stopwords

import numpy as np

from Models.LoadAndTrainModels import *


from nltk.stem import WordNetLemmatizer
from nltk.probability import ConditionalFreqDist
from nltk.probability import ConditionalProbDist 
from nltk.probability import LaplaceProbDist
    

def flip_sentiment(sentiment):
    if(sentiment == 'positive'):
        return 'negative'
    elif(sentiment == 'negative'):
        return 'positive'
    
def convertSentimentValue(sentimentValueOld):
    if sentimentValueOld == '0\n':
        return "negative"
    elif sentimentValueOld == '1\n':
        return "positive"
    
    
    
#get a dataset of labeled words: either positive or negative
def getOpinionTrainingDataWordsAndProbDist(bigram_compatible=False):
    from nltk.corpus import opinion_lexicon
    from nltk.stem import WordNetLemmatizer
    from nltk.probability import ConditionalFreqDist
    from nltk.probability import ConditionalProbDist, ELEProbDist #71.50 training accuracy
    from nltk.probability import LaplaceProbDist #71.90% training accuracy
    
    lemmatizer = WordNetLemmatizer()
    
    text = opinion_lexicon

    positive_words = ([(lemmatizer.lemmatize(word=word), 'positive') for word in text.positive()])
    negative_words = ([(lemmatizer.lemmatize(word=word), 'negative') for word in text.negative()])

    labeled_words = positive_words + negative_words
    
    random.shuffle(labeled_words)
    

    
    featuresets = [(sentiment_feature(n), sentiment) for (n, sentiment) in labeled_words]
    
    
    if(bigram_compatible == True):
        
        featuresets = [(sentiment_feature_bigram(['not', n]), flip_sentiment(sentiment)) for (n, sentiment) in labeled_words] + [(sentiment_feature_bigram([n , 'not']), flip_sentiment(sentiment)) for (n, sentiment) in labeled_words]+[(sentiment_feature_unigram_1(n), sentiment) for (n, sentiment) in labeled_words] + [(sentiment_feature_unigram_2(n), sentiment) for (n, sentiment) in labeled_words] 
        
    
    train_amnt = int(len(featuresets)*.8) #80% train data; 20% test data
    train_data = featuresets[:train_amnt]
    test_data = featuresets[train_amnt:]
    assert len(train_data) == train_amnt

    cfdist = ConditionalFreqDist(labeled_words)
    cpdist = ConditionalProbDist(cfdist, LaplaceProbDist, bins=2)
    
    return train_data, test_data, cpdist



def getUCIDataset_words():
    data_path = os.path.join('/home/brf97486/finalProject/labelled_sentence_data_set/sentiment labelled sentences')
    yelp = os.path.join(data_path, 'yelp_labelled.txt')
    imdb = os.path.join(data_path, 'imdb_labelled.txt')
    amazon = os.path.join(data_path, 'amazon_cells_labelled.txt')
    assert os.path.isfile(yelp) 
    assert os.path.isfile(imdb) 
    assert os.path.isfile(amazon) 
    file = open(yelp, 'r')
    file2 = open(imdb, 'r')
    file3 = open(amazon, 'r')
    dataset = []
    for line in file:
        dataset.append(re.split(r'\t+', line))
    for line in file2:
        dataset.append(re.split(r'\t+', line))
    for line in file3:
        dataset.append(re.split(r'\t+', line))
    
    lemmatizer = WordNetLemmatizer()
    
    dataset = [(lemmatizer.lemmatize(strs), value) for (strs, value) in dataset]
    random.shuffle(dataset)
    
    featuresets = [(sentiment_feature(n), sentiment) for (n, sentiment) in dataset]
    
    train_amnt = int(len(featuresets)*.8) #80% train data; 20% test data
    train_data = featuresets[:train_amnt]
    test_data = featuresets[train_amnt:]
    
    cfdist = ConditionalFreqDist(dataset[:train_amnt])
    cpdist = ConditionalProbDist(cfdist, LaplaceProbDist, bins=2)
    
    return train_data, test_data, cpdist

def getUCIDataset_sentences():
    data_path = os.path.join('/home/brf97486/finalProject/labelled_sentence_data_set/sentiment labelled sentences')
    yelp = os.path.join(data_path, 'yelp_labelled.txt')
    imdb = os.path.join(data_path, 'imdb_labelled.txt')
    amazon = os.path.join(data_path, 'amazon_cells_labelled.txt')
    assert os.path.isfile(yelp) 
    assert os.path.isfile(imdb) 
    assert os.path.isfile(amazon) 

    file = open(yelp, 'r')
    file2 = open(imdb, 'r')
    file3 = open(amazon, 'r')
    
    dataset = []
    
    for line in file:
        dataset.append(re.split(r'\t+', line))
    for line in file2:
        dataset.append(re.split(r'\t+', line))
    for line in file3:
        dataset.append(re.split(r'\t+', line))
        
    #dataset = [(strs, int(value)) for (strs, value) in dataset]
    
    lemmatizer = WordNetLemmatizer()
    
    dataset = [(lemmatizer.lemmatize(strs), convertSentimentValue(value)) for (strs, value) in dataset]
    
    
    ds = []
    ds_without_feat = []
    #nltk.bigram(dataset)
    for line in dataset:
        value = line[1] #sentiment value of the entire sentence
        words = nltk.word_tokenize(line[0]) #get each word in the sentence
        
        processed_words = []
        
        #remove stop words (except negation words) and puncutation then lemmatize
        stop_words = set(stopwords.words('english'))
        
        for word in words:
            if(word not in stop_words and word not in string.punctuation):
                if word in stop_words:
                    if word == 'nor' or word == 'no' or word == 'not':
                        processed_words.append('not')
                else:
                    word_lem = lemmatizer.lemmatize(word)
                    processed_words.append(word_lem)
        ds.append((sentiment_feature_sentence(' '.join(processed_words)), value))
        random.shuffle(ds)
        ds_without_feat.append((processed_words, value))
                         
                  
    #featuresets = [(sentiment_feature_sentence(n), sentiment) for (n, sentiment) in dataset]
    
    train_amnt = int(len(ds)*.8) #80% train data; 20% test data
    train_data = ds[:train_amnt]
    test_data = ds[train_amnt:]
    
    features_to_freq_dist_ready = []
    
    for data in ds: #all pices of training data
        for key in data[0]:
            features_to_freq_dist_ready.append((key, data[1]))
    
    cfdist = ConditionalFreqDist(features_to_freq_dist_ready)
    cpdist = ConditionalProbDist(cfdist, LaplaceProbDist, bins=2)
    
    return train_data, test_data, cpdist

def getUCIDataset_bigram():
    
    data_path = os.path.join('/home/brf97486/finalProject/labelled_sentence_data_set/sentiment labelled sentences')
    yelp = os.path.join(data_path, 'yelp_labelled.txt')
    imdb = os.path.join(data_path, 'imdb_labelled.txt')
    amazon = os.path.join(data_path, 'amazon_cells_labelled.txt')
    assert os.path.isfile(yelp) 
    assert os.path.isfile(imdb) 
    assert os.path.isfile(amazon) 
    file = open(yelp, 'r')
    file2 = open(imdb, 'r')
    file3 = open(amazon, 'r')
    dataset = []
    for line in file:
        dataset.append(re.split(r'\t+', line))
    for line in file2:
        dataset.append(re.split(r'\t+', line))
    for line in file3:
        dataset.append(re.split(r'\t+', line))
    
    lemmatizer = WordNetLemmatizer()
    
    ds = []
    ds_without_feat = []
    #nltk.bigram(dataset)
    for line in dataset:
        value = int(line[1]) #sentiment value of the entire sentence
        words = nltk.word_tokenize(line[0]) #get each word in the sentence
        
        processed_words = []
        
        #remove stop words (except negation words) and puncutation then lemmatize
        stop_words = set(stopwords.words('english'))
        
        for word in words:
            if(word not in stop_words and word not in string.punctuation):
                if word in stop_words:
                    if word == 'nor' or word == 'no' or word == 'not':
                        process_words.append('not')
                else:
                    word_lem = lemmatizer.lemmatize(word)
                    processed_words.append(word_lem)
            
            
        bigram = list(nltk.bigrams(processed_words))
        for bi in bigram:
            if(value <= 0):
                val_key = "negative"
            elif(value >= 1):
                val_key = "positive"
            else:
                print("Some of your sentences have a value other than 0 or 1")
            

            ds.append((sentiment_feature_bigram(bi), val_key))
            ds_without_feat.append((bi, val_key))
    
    #train_opinion, test_opinion, prob_opinion = getOpinionTrainingDataWordsAndProbDist(bigram_compatible=True)
    #ds_unigram_and_bigram = train_opinion + test_opinion + ds
    ds_unigram_and_bigram = ds
    random.shuffle(ds_unigram_and_bigram)
    
    #featuresets = [(applyFeatureSetToBigrams(n), sentiment) for (n, sentiment) in dataset]
    
    train_amnt = int(len(ds_unigram_and_bigram)*.8) #80% train data; 20% test data
    train_data = ds_unigram_and_bigram[:train_amnt]
    test_data = ds_unigram_and_bigram[train_amnt:]
    
    cfdist = ConditionalFreqDist(ds_without_feat)
    cpdist = ConditionalProbDist(cfdist, LaplaceProbDist, bins=2)
    
    return train_data, test_data, cpdist