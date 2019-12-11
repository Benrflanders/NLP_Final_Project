import random
import nltk

from nltk.classify import NaiveBayesClassifier
from nltk.probability import LaplaceProbDist

def sentiment_feature_sentence(sentence):
    return {'firstNoun': getFirstNoun(sentence),
            'secondNoun': getSecondNoun(sentence),
            'POSBeforeNoun': getPOSBeforeNoun(sentence),
            'POSAfterNoun': getPOSAfterNoun(sentence),
            #'adjCount' : getNumberOfAdjs(sentence),
            'adjBeforeNoun' : getAdjBeforeNoun(sentence),
            'adjAfterNoun' : getAdjAfterNoun(sentence),
            'fistVerb' : getFirstVerb(sentence)
           }

def sentiment_feature_bigram(bigram):
    return {'word_1': bigram[0],'word_2':bigram[1]}

def sentiment_feature_bigram_2(bigram):
    return [bigram[0], bigram[1]]

def sentiment_feature(word):
	return {'word_1': word,
           'word_2' : word}

def sentiment_feature_unigram_1(word):
    return {'word_1':word}
def sentiment_feature_unigram_2(word):
    return {'word_2':word}

def getAdjAfterNoun(sentence):
    nounFound = False
    
    split_sent = [nltk.word_tokenize(sentence)]
    
    for word in split_sent:
        tag = nltk.pos_tag(word, tagset='universal')
        for (word, pos) in tag:
            if pos == 'NOUN':
                nounFound = True
            
            if pos == 'ADJ' and nounFound:
                
                return word

def getAdjBeforeNoun(sentence):
    mostRecentAdj = ""
    
    split_sent = [nltk.word_tokenize(sentence)]
    
    for word in split_sent:
        tag = nltk.pos_tag(word, tagset='universal')
        for (word, pos) in tag:
            if pos == 'NOUN':
                return mostRecentAdj
            
            if pos == 'ADJ':
                mostRecentAdj = word
                
                

def getNumberOfAdjs(sentence):
    
    count = 0
    
    split_sent = [nltk.word_tokenize(sentence)]
    
    for word in split_sent:
        tag = nltk.pos_tag(word, tagset='universal')
        for (word, pos) in tag:
            
            if pos == 'ADJ':
                count = count + 1
    return count
                
def getPOSAfterNoun(sentence):
    
    i_stop = -1
    i = 0
    split_sent = [nltk.word_tokenize(sentence)]
    
    for word in split_sent:
        tag = nltk.pos_tag(word, tagset='universal')
        for (word, pos) in tag:
            
            if(i == i_stop):
                return pos
            
            if pos == 'NOUN':
                i = i + 1
                i_stop = i
            else:
                i= i + 1

def getPOSBeforeNoun(sentence):
    pos_before = ""
    pos_after = ""
    
    i = 0
    split_sent = [nltk.word_tokenize(sentence)]
    
    for word in split_sent:
        tag = nltk.pos_tag(word, tagset='universal')
        for (word, pos) in tag:
            
            if pos == 'NOUN':
                return pos_before
            else:
                pos_before = pos
                i= i + 1
 
    
def getFirstNoun(sentence):
    pos_before = ""
    pos_after = ""
    
    i = 0
    split_sent = [nltk.word_tokenize(sentence)]
    
    for word in split_sent:
        tag = nltk.pos_tag(word, tagset='universal')
        for (word, pos) in tag:
            
            if pos == 'NOUN':
               
                return word
            else:
                i= i + 1
                
def getSecondNoun(sentence):
    pos_before = ""
    pos_after = ""
    firstNounFound = False
    i = 0
    split_sent = [nltk.word_tokenize(sentence)]
    
    for word in split_sent:
        tag = nltk.pos_tag(word, tagset='universal')
        for (word, pos) in tag:
            
            if pos == 'NOUN':
                if firstNounFound == False:
                    firstNounFound = True
                else:
                    return word
            else:
                i= i + 1  
                
def getFirstVerb(sentence):
    split_sent = [nltk.word_tokenize(sentence)]
    
    for word in split_sent:
        tag = nltk.pos_tag(word, tagset='universal')
        for (word, pos) in tag:
            
            if pos == 'VERB':
               
                return word

            

    





def getSentiWordNetClassifier():
    from nltk.corpus import sentiwordnet 
    
    return sentiwordnet
    
    #ositive_words = 
    

def applyFeatureSetToSentence(input_data):
    featuresets = [(sentiment_feature_sentence(sentence)) for sentence in input_data]
    return featuresets 

def applyFeatureSetToTaggedSentence(input_data):
    #featuresets = [(sentiment_feature_sentence(' '.join(sentence))) for sentence in input_data]
    featuresets = []
    for sent in input_data:
        joined_sentence = []
        
        for tagged_word, tag in sent:
            joined_sentence.append(tagged_word)
        featuresets.append(sentiment_feature_sentence(' '.join(joined_sentence)))
    
    return featuresets

def applyFeatureSetToBigrams(input_data):
    featuresets = [(sentiment_feature_bigram(bigram)) for bigram in input_data]
    return featuresets

def applyFeatureSetToTaggedBigrams(input_data, only_nouns_and_adj=False):
    
    if only_nouns_and_adj == True:
        featuresets = []
            
        for ((word_1, tag_1), (word_2, tag_2)) in input_data:
            print(tag_1)
            print(tag_2)
            if((tag_1 == 'NOUN' and tag_2 == 'ADJ') or (tag_1 == 'ADJ' and tag_2 == 'NOUN')):
               featuresets.append(sentiment_feature_bigram((word_1, word_2)))
        
    else:
        featuresets = [(sentiment_feature_bigram((word_1, word_2))) for ((word_1, tag_1), (word_2, tag_2)) in input_data]
    
    return featuresets
    
    
    
def applyFeatureSetToWords(input_data):
    featuresets = [(sentiment_feature(wrd)) for wrd in input_data]
    return featuresets
                   


def getNaiveBayesTrainedClassifier(dataset):
    #train_set, test_set = getOpinionTrainingData() #change this to the currently used corpus approach
    #est = lambda fdist : LaplaceProbDist
    train_set, test_set, prob_dist = dataset()
    from nltk.probability import DictionaryProbDist
    
    dict_probs = {'positive': .1, 'negative': .1}
    label_probdist = DictionaryProbDist(dict_probs)
    
    classifier = nltk.NaiveBayesClassifier(label_probdist=label_probdist, feature_probdist=prob_dist)
    
    classifier = classifier.train(train_set, estimator=LaplaceProbDist)                                      
    print("Classifier accuracy percent: ", (nltk.classify.accuracy(classifier, test_set))*100)
    #print(classifier.show_most_informative_features(10))
    return classifier
