#the main entry point for loading and training all models and printing a report
import numpy as np

from Models import LoadAndTrainModels
from Make_Enron_Corpus import enronCorpus
from analyze_data.Data_Utils import *
from getExternalDatasets import *


def printProbabilitiesFromLogProb(prob_classify_dict):
    positive = prob_classify_dict["positive"]
    negative = prob_classify_dict["negative"]

    print("positive negative log: ", positive)
    print("negative negative log: ", negative)
    
    probs = np.exp([positive, negative])/np.exp([positive, negative]).sum()
    print("positive probability: ", probs[0])
    print("negative probability: ", probs[1])
    
def classifySentenceUCIDataset():
    training_data = getUCIDataset()
    #get the trained sentiment classifier
    print("load and train model")
    classifier = LoadAndTrainModels.getNaiveBayesTrainedClassifier(getUCIDataset)
    
    print("building enron corpus")
    enron_corp = enronCorpus()
    
    avg_sentiment = {}
    
    
    file_list = ['4_5.txt',
'4_2.txt',
'5_3.txt',
'5_4.txt',
'1_1.txt',
'4_4.txt',
'1_5.txt',
'1_2.txt',
'2_4.txt',
'4_1.txt',
'3_2.txt',
'3_5.txt',
'1_4.txt',
'5_1.txt',
'2_2.txt',
'2_5.txt']
    
    print("apply features and sentiments")
    for d in enron_corp.fileids():
        #input_data = enron_corp.sentences(d)
        input_data = (enronCorpus().raw()).split('.')
        relation_sentence_feature_data = LoadAndTrainModels.applyFeatureSetToSentence(input_data)
        total_sentiment = 0
        total_sentiment = classifier.classify_many(featuresets=relation_sentence_feature_data)
        avg_sentiment[d] = sum(total_sentiment)/len(relation_sentence_feature_data)
        print(d, " complete...")
        print(avg_sentiment)
        #break
    print("average sentiment for each relation type: ", avg_sentiment)
    

    
def classifyBigramUCIDataset():
    
    print("get bigrams of common nouns and their adjectives")
    b = getBigramsOfCommonNounsAndTheirAdjective(enronCorpus())
    
    print("train classifier")
    #get the trained sentiment classifier
    classifier = LoadAndTrainModels.getNaiveBayesTrainedClassifier(getUCIDataset_bigram)

    #classify each relationship type and store the average in a dict
    avg_sentiment = {}
    
    print("for each file in corpus")
    for d in enron_corp.fileids():
        
        input_data = b[d]
        relation_bigram_feature_data = LoadAndTrainModels.applyFeatureSetToBigrams(input_data) 
        
        if(len(relation_bigram_feature_data) == 0):
            avg_sentiment[d] = 0
        else:
        
            #total_sentiment = 0
            for feature in relation_bigram_feature_data:
                
                prob_classify_dict = classifier.prob_classify(feature)._prob_dict
                avg_sentiment[d].append([prob_classify_dict['positive'], prob_classify_dict['negative']])
                
                
                #avg_sentiment[d] = sum(total_sentiment)/len(relation_bigram_feature_data)
            
    #print("average sentiment for each relation type: ", avg_sentiment)
    
    
    
    print("classifying: very good")
    prob_classify_dict = (classifier.prob_classify({"bigram":"very good"}))._prob_dict
    printProbabilitiesFromLogProb(prob_classify_dict)
    
    print("classifying: not bad")
    prob_classify_dict = (classifier.prob_classify({"word":"not bad"}))._prob_dict
    printProbabilitiesFromLogProb(prob_classify_dict)
          
    print("classifying: very envious")
    prob_classify_dict = (classifier.prob_classify({"word":"very envious"}))._prob_dict
    printProbabilitiesFromLogProb(prob_classify_dict)
    
    
    

    
    

    

        
def main():
    #testing only
    #classifyWithSentiWordNet()
    
    #words as features
    #classifyBagOfWordsOpinionLexicon()
    #classifyBagOfWordsUCIDataset() # <-- terrible accuracy, don't use
    
    #bigram feaature
    #classifyBigramUCIDataset()
    
    #multi-feature training
    classifySentenceUCIDataset()
    
if __name__ == "__main__":
    main()