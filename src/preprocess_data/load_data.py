#a file for loading the proper data from the download directory to the processed data directory

import os, os.path
import shutil

from emailInfo import *

#Path information
data_path = os.path.expanduser('~/finalProject/enron_data/maildir/')
output_path = os.path.expanduser('~/finalProject/enron_data_processed/')

#Make output path if it does not exist
if not os.path.exists(output_path):
	os.makedirs(output_path)

    
#Copy data from data_path to output_path
for sub_dir in os.listdir(data_path): #for each person
	print(sub_dir)
	#create new directory for each person with emails
	new_output_sub_dir = os.path.join(output_path, sub_dir)
	if not os.path.exists(new_output_sub_dir):
		os.makedirs(new_output_sub_dir)
		
	#copy over any useful data to their new directory
	for txt_dir in os.listdir(os.path.join(data_path,sub_dir)):
		curr_dir = os.path.join(data_path,sub_dir,txt_dir)
		print(curr_dir)
		#if a file copy it over
		if os.path.isfile(curr_dir):
			new_output_file = os.path.join(curr_dir, txt_dir)
			if not os.path.exists(new_output_file):
				try:
					shutil.copy(curr_dir, new_output_file)
				except IOError:
					print "Could not copy " + curr_dir
		elif os.path.isdir(curr_dir):
			for filename in os.listdir(curr_dir):
				file_to_copy = os.path.join(curr_dir, filename)
				if os.path.isfile(file_to_copy) and not os.path.exists(os.path.join(new_output_sub_dir, filename)):
					try:
						shutil.copy(file_to_copy, new_output_sub_dir)
					except IOError:
						print "Could not copy: " + file_to_copy

#make directory structure
def load_and_process_data():
    for sub_dir in os.listdir(data_path): #for each person
        #for all emails in the inbox and sent folders
        inbox_dir = os.path.join(data_path, sub_dir, inbox)
        if(os.path.exists(inbox_dir)):
            for file in inbox_dir:
                file_content = open(os.path.join(inbox_dir+'/'+file))
                #get that email's to and from users
                to = get_email_to(file_content)
                frm = get_email_from(file_content)
                id_to = csvEmployeeNameToDirStyleEmployeeName(to)
                id_frm = csvEmployeeNameToDirStyleEmployeeName(frm)
                
                #get each user's tier
                
                #create the proper file if it doesn't exist
                #get only the message contents
                #append to the file for that X to Y file
            