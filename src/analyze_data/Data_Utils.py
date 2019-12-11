import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from Make_Enron_Corpus import enronCorpus

enron_corp = enronCorpus()
tagger = nltk.pos_tag

#get the most common nouns for each relation type
def getMostCommonNouns(enron_corp, num_nouns=10):
    most_common_noun_for_each_file = {}
    
    #for each relation
    for d in enron_corp.fileids():
        #get the text and do a freq dist
        tagged_file = getTaggedFile(enron_corp, d)
        word_tag_lst = []
        for sent in tagged_file:
            for (wrd,tag) in sent:
                word_tag_lst.append((wrd,tag))     
        nouns_fd = nltk.FreqDist([word for (word, tag) in word_tag_lst if tag == 'NOUN' and word != '>'])
        most_common_noun_for_each_file[d] = [noun for (noun, amnt) in nouns_fd.most_common(num_nouns)]
        
    return most_common_noun_for_each_file
        
def getTaggedFile(enron_corp, fileid):
    tagged_sents = []
    
    corp_sents= sent_tokenize(enron_corp.raw(fileid))
    
    for sent in corp_sents:
        text = word_tokenize(sent)
        sent_tagged = tagger(text, tagset='universal')
        tagged_sents.append(sent_tagged)
    
    return tagged_sents
                           
def getBigramsOfCommonNounsAndTheirAdjective(enron_corp):
    bigramDict = {}
    commonNouns = getMostCommonNouns(enron_corp, 0)
    
    
    for d in enron_corp.fileids():
        bigramDict[d] = []
        tagged_file = getTaggedFile(enron_corp, d) #get the tagged sentences
        
        for sent in tagged_file:
            bigram = nltk.bigrams(sent)
            for (a,b) in bigram:
                if((a[1] == 'NOUN' and b[1] == 'ADJ' and (a[1] not in commonNouns[d])) or (b[1] == 'NOUN' and a[1] == 'ADJ' and (b[1] not in commonNouns[d]))):
                   bigramDict[d].append((a,b))
        
    return bigramDict
    
    
               