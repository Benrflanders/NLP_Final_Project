import csv 
import os

username_to_name = os.path.expanduser('~/finalProject/employees-username-and-name.csv')
employee_list_path = os.path.expanduser('~/finalProject/employees_with_titles.csv')
title_to_tier_path = os.path.expanduser('~/finalProject/Title_to_tier.csv')

#input should be an ID style employeeName (ex: 'k..alen' or 'tom.alonso')
def getEmployeeTitle(employeeName):
    
    with open(employee_list_path) as csvfile:
        employeeReader = csv.reader(csvfile, delimiter=',')
        for row in employeeReader:
            if(employeeName == row[0]):
                str_tmp = " "
                return str_tmp.join(row[1:])
    
    return " "

#convert a name from the csv style (firstname.lastname) to directory style name (lastname-firstinitial)
def csvEmployeeEmailToLegalName(csvEmployeeName):
    #get the employee name from the list of employees that maps username to legal name
    with open(username_to_name) as csvfile:
        usernameAndNameReader = csv.reader(csvfile, delimiter=',')
        for row in usernameAndNameReader:
            if(csvEmployeeName == row[0]): #if found the username
                csvEmployeeName = row[1] + '.' + row[2]

                
#convert an employees name to their corresponding directory - DEPRECATED SINCE directory is no longer important
def employeeLegalNameToDirStyle(legalName):
    try:
        out = csvEmployeeName.split('.') #split on .
        
        if(len(out) == 1):
            out = csvEmployeeName.split('_')
        
        #if more than 2 values, join [1:] together
        out_tmp = ""
        if(len(out) > 2):
            out[1] = out_tmp.join(out[1:])
            out[2:]=""
        
        
        firstName = out[0]
        lastName = out[1]
        firstInitial = firstName[0]
    except:
        lastName = "ERROR"
        firstInitial = "E"
    
    return lastName + '-' + firstInitial
    
def getEmployeeTitle_old(employeeName):
    employeeInfo = getEmployeeInfo(employeeName)
    
    title = employeeInfo[1:]
    out = " "
    return out.join(title)
    
#get the employee's tier (see readme for more info)
def getEmployeeTier(employeeID):
    title = getEmployeeTitle(employeeID)
    potential_tiers = [-1]
    #open the csv that maps title to tier
    with open(title_to_tier_path) as csvfile:
        titleToTierReader = csv.reader(csvfile, delimiter=',')
        #find the correct row for the given title -- match the best fit
        for row in titleToTierReader:
            if row[0] == title: #if exactly equal then return
                return(int(row[1]))
            elif(row[0] in title):
                potential_tiers.append(int(row[1]))

    
    return max(potential_tiers)
    