import random
import nltk

from nltk.classify import NaiveBayesClassifier


def sentiment_feature(word):
	return {'word': word}


#get a dataset of labeled words: either positive or negative
def getOpinionTrainingData():
    from nltk.corpus import opinion_lexicon

    text = opinion_lexicon

    positive_words = ([(word, 1) for word in text.positive()])
    negative_words = ([(word, -1) for word in text.negative()])

    labeled_words = positive_words + negative_words
    random.shuffle(labeled_words)
    
    featuresets = [(sentiment_feature(n), sentiment) for (n, sentiment) in labeled_words]
    
    train_amnt = int(len(featuresets)*.8) #80% train data; 20% test data
    train_data = featuresets[:train_amnt]
    test_data = featuresets[train_amnt:]
    assert len(train_data) == train_amnt
    
    return train_data, test_data

def getSentiWordNetClassifier():
    from nltk.corpus import sentiwordnet 
    
    return sentiwordnet
    
    #ositive_words = 
    
    

def applyFeatureSetToWords(input_data):
    featuresets = [(sentiment_feature(wrd)) for wrd in input_data]
    return featuresets
                   
    

def getNaiveBayesTrainedClassifier():
    train_set, test_set = getOpinionTrainingData() #change this to the currently used corpus approach
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print("Classifier accuracy percent: ", (nltk.classify.accuracy(classifier, test_set))*100)
    print(classifier.show_most_informative_features(10))
    #lassifier.train(train_set)
    return classifier
    #print(nltk.classify.accuracy(classifier, test_set))
