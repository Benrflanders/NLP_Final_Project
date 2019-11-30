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

#get the body of an email without any metadata from the file's content
def get_email_body_without_metadata(fileContent):
    body = re.findall(r"(.+)", emails[0])
    body_temp = ""
    for item in body:
        if not item.startswith(tuple(metadata_tags)):
            body_temp = body_temp + item

    body = body_temp
    return body

#get to user - @TODO currently assumes only one possible recipient
def get_email_to(fileContent):
    to = re.search(r"To:.(.+)", emails[0])
    to = re.split(" ", to.group())
    if("@" in to[1]):
        to = re.split("[@]", str(to[1]))
    to = to[0]
    return to

#get from user
def get_email_from(fileContent):
    frm = re.search(r"From:.(.+)", emails[0])
    print(frm.group())
    frm = re.split(" ", frm.group())
    if("@" in frm[1]):
        frm = re.split("[@]", str(frm[1]))
        print(frm[0])

    frm = frm[0]
    return frm