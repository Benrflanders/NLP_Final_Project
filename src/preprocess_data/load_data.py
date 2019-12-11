#a file for loading the proper data from the download directory to the processed data directory
import sys
import os, os.path
import shutil
import string

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

from emailInfo import *

#Path information
data_path = os.path.expanduser('~/finalProject/enron_data/maildir/')
output_path = os.path.expanduser('~/finalProject/enron_data_processed/')

#Make output path if it does not exist
if not os.path.exists(output_path):
	os.makedirs(output_path)    

    

def lemmatize_and_normalize_string(email):
    #remove punctuation
    remove = string.punctuation
    remove.replace(".", "") #don't remove periods
    
    
    #Citation: https://machinelearningmastery.com/clean-text-machine-learning-python/
    word_list = word_tokenize(email)
    processed_word_list = []
    for word in word_list:
        if(not '.' in word):
            word = word.lower()
            word = lemmatizer.lemmatize(word=word)
            processed_word_list.append(word)

    #make sure all words are alphanumeric -> get rid of punctuation
    #word_list_stripped = [word for word in word_list if word.isalpha()]
    word_list_stripped = [word.translate(word.maketrans('','', remove)) for word in processed_word_list] #https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
    
    return ' '.join(word_list_stripped)
    
#make directory structure
def load_and_process_data(lemmatize=False):
    
    data_tracker = {}
    
    for sub_dir in os.listdir(data_path): #for each person
        #print(sub_dir)
        
        #for all emails in the inbox and sent folders
        inbox_dir = os.path.join(data_path, sub_dir, "inbox")
        sent_dir = os.path.join(data_path, sub_dir, "sent")
        deleted_dir = os.path.join(data_path, sub_dir, "deleted_items")
        _sent_mail_dir = os.path.join(data_path, sub_dir, "_sent_mail")
        
        dir_list = [inbox_dir, sent_dir, deleted_dir, _sent_mail_dir] #doesn't make sense to use all types of mail, only some
        
        for curr_dir in dir_list: #for each folder type from above in the user directory
            if(os.path.exists(curr_dir)): #
                for file in os.listdir(curr_dir):
                    if(os.path.isfile(os.path.join(inbox_dir,file))):
                        try:
                            file_content = open(os.path.join(inbox_dir,file)).read()
                            emails = re.split('-----Original Message-----', file_content)
                            
                        except:
                            emails = ['NONE']
                        
                        for email in emails:
                            #get that email's to and from users
                            to_list = get_email_to(email)
                            frm = get_email_from(email)
                            
                            for to in to_list: #for each recipient in the list of recipients
                            
                                #id_to = csvEmployeeNameToDirStyleEmployeeName(to)
                                #id_frm = csvEmployeeNameToDirStyleEmployeeName(frm)

                                #get each user's tier
                                tier_to = getEmployeeTier(to)
                                tier_frm = getEmployeeTier(frm)

                                #if both tier_to and tier_frm are greater than 0:
                                if(tier_to > 0 and tier_frm > 0):
                                    fn = str(tier_to) + "_" + str(tier_frm) + ".txt"
                                    
                                    try:
                                        data_tracker[fn] += 1
                                    except:
                                        data_tracker[fn] = 1
                                    
                                    if not os.path.isfile(os.path.join(output_path, fn)):
                                        #create the proper file if it doesn't exist
                                        #os.makedirs(os.path.join(output_path, fn))
                                        f = open(os.path.join(output_path, fn), "w+")

                                    else:
                                        f = open(os.path.join(output_path, fn), "a+")
                                    
                                    print("copied from: " + os.path.join(inbox_dir,file))
                                    
                                    data_to_write = get_email_body_without_metadata(email)
                                    
                                    data_to_write_normalized = ""
                                    sent_list = sent_tokenize(data_to_write)
                                    for sent in sent_list:
                                        data_to_write_normalized = data_to_write_normalized + ". " + lemmatize_and_normalize_string(sent)
                                    
                                    f.write(data_to_write_normalized)
                                    
                                    #sys.exit()
                                #get only the message contents
                                #append to the file for that X to Y file
    print("DATA COPYING RESULTS: ", data_tracker)