def classifyWithSentiWordNet():
    #get enron corpus
    enron_corp = enronCorpus()
    swn = LoadAndTrainModels.getSentiWordNetClassifier()
    
    #classify each relationship type and store the average in a dict
    avg_sentiment = {}
    
    
    for d in enron_corp.fileids():
        relation_data = enron_corp.words(d) #data for a single relation
        #relation_feature_data = LoadAndTrainModels.applyFeatureSetToWords(relation_data)
        
        #wrds0 = (str(word) for word in relation_data)
        
        #wrds = swn.senti_synset(wrds0)
        word_count = 0
        total_pos_score = 0
        total_neg_score = 0
        total_obj_score = 0
        
        for wrd in list(relation_data):
            try:
                #print("wrd ok: ", wrd)
                curr_wrd = list(swn.senti_synsets(str(wrd)))[0]
                #print(curr_wrd)
                #curr_wrd0 = curr_wrd)[0]
            
                total_pos_score += curr_wrd.pos_score()
                total_neg_score += curr_wrd.neg_score()
                total_obj_score += curr_wrd.obj_score()
                word_count += 1
            except:
                #print("wrd bad: ", wrd)
                pass
        
        avg_sentiment[d] = [total_pos_score/word_count, total_neg_score/word_count, total_obj_score/word_count]
    
    print(avg_sentiment)