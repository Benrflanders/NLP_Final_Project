def classifyBagOfWordsOpinionLexicon():
    #get enron corpus
    word_set = LoadAndTrainModels.applyFeatureSetToWords(enronCorpus().words())
    
    #training_data, testing_data, prob_dist = LoadAndTrainModels.getOpinionTrainingDataWords()
    
    #get the trained sentiment classifier
    classifier = LoadAndTrainModels.getNaiveBayesTrainedClassifier(LoadAndTrainModels.getOpinionTrainingDataWordsAndProbDist)
    
    #classify each relationship type and store the average in a dict
    avg_sentiment = {}
    
    for d in enron_corp.fileids():
        break
        relation_data = enron_corp.words(d) #data for a single relation
        relation_feature_data = LoadAndTrainModels.applyFeatureSetToWords(relation_data) #data for a single relation with a feature set application to it
        print(type(relation_feature_data))
        total_sentiment = 0
        total_sentiment = classifier.classify_many(featuresets=relation_feature_data)
        avg_sentiment[d] = sum(total_sentiment)/len(relation_feature_data)
    
    print("average sentiment for each relation type: ", avg_sentiment)

    print("classifying: good")
    prob_classify_dict = (classifier.prob_classify({"word":"good"}))._prob_dict
    printProbabilitiesFromLogProb(prob_classify_dict)
    
    print("classifying: bad")
    prob_classify_dict = (classifier.prob_classify({"word":"bad"}))._prob_dict
    printProbabilitiesFromLogProb(prob_classify_dict)
          
    print("classifying: envious")
    prob_classify_dict = (classifier.prob_classify({"word":"envious"}))._prob_dict
    printProbabilitiesFromLogProb(prob_classify_dict)