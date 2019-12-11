import os
import re
import random

from employeeInfo import *

metadata_tags = [
    'Date:',
    'From:',
    'To:',
    'Mime-Version:',
    'Content-Type:',
    'Content-Transfer-Encoding:',
    'X-From:',
    'X-To:',
    'X-cc:',
    'X-bcc:',
    'X-Folder:',
    'X-Origin:',
    'X-FileName:',
    'Message-ID:',
    'Subject'
]

processed_data_path = os.path.expanduser('~/finalProject/enron_data_processed/')
raw_data_path = os.path.expanduser('~/finalProject/enron_data/maildir/')

#for some user get some email
def get_random_file():
    for root, dirs, files in os.walk(data_path):
        for name in files:
            if name.endswith((".", ".txt")):
                print(root)
                print(dirs)
                
                if(random.randint(0,10) == 1): #chance that the email will be used or go to the next one to return it
                    return open(os.path.join(root+'/'+name))

#get the body of an email without any metadata from the file's content - metadata ends at the X-FileName tag
def get_email_body_without_metadata(email):
    tmp_body = ""
    found_metadata_end = False
    
    for line in email.splitlines():
        if(found_metadata_end):
            tmp_body += line
            tmp_body += '\n'

        if("X-FileName:" in line):
            found_metadata_end = True

    body = tmp_body
    return body



#get all recipients of an email - RETURNS A LIST of usernames
def get_email_to(email):
    to_output = []
    
    to = re.search(r"To:.(.+)", email)
    
    if(to == None): #if no match is found for a 'to' metadata field
        return "NONE"

    all_recipients = re.split(" ", to.group())
    for recipient in all_recipients:
        #if an email address
        if("@" in recipient):
            tmp_recipient = re.split("[@]", str(recipient))[0] #get just the username
            
            try: #if there are multiple @ in a single email address
                if("@" in tmp_recipient):
                    tmp_recipient = re.split("[@]", str(tmp_recipient))
                    tmp_recipient = tmp_recipient[0]
            except:
                pass 
                
            to_output.append(tmp_recipient) #add the username to the list of recipients to be returned
            
    return to_output


#get from user
def get_email_from(email):
    frm = re.search(r"From:.(.+)", email)
    
    if(frm == None): #if no match is found for a message recipient
        return "NONE"
    
    frm = re.split(" ", frm.group())
    try:
        if("@" in frm[1]):
            frm = re.split("[@]", str(frm[1]))
        frm = frm[0]
    except:
        pass
    
    return frm