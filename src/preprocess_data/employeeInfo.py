import csv 
import os

employee_list_path = os.path.expanduser('~/finalProject/employees_with_titles.csv')
title_to_tier_path = os.path.expanduser('~/finalProject/Title_to_tier.csv')

#input should be a directory style employeeName (lastname-firstInitial)
def getEmployeeInfo(employeeName):
    
    with open(employee_list_path) as csvfile:
        employeeReader = csv.reader(csvfile, delimiter=',')
        for row in employeeReader:
            if(employeeName == csvEmployeeNameToDirStyleEmployeeName(row[0])):
               return row
    
    return " "

#convert a name from the csv style (firstname.lastname) to directory style name (lastname-firstinitial)
def csvEmployeeNameToDirStyleEmployeeName(csvEmployeeName):
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
    
def getEmployeeTitle(employeeName):
    employeeInfo = getEmployeeInfo(employeeName)
    
    title = employeeInfo[1:]
    out = " "
    return out.join(title)
    
#get the employee's tier (see readme for more info)
def getEmployeeTier(employeeName):
    title = getEmployeeTitle(employeeName)
    potential_tiers = [-1]
    #open the csv that maps title to tier
    with open(title_to_tier_path) as csvfile:
        titleToTierReader = csv.reader(csvfile, delimiter=',')
        #find the correct row for the given title -- match the best fit
        for row in titleToTierReader:
            if row[0] == title: #if exactly equal then return
                return(row[1])
            elif(row[0] in title):
                potential_tiers.append(int(row[1]))
                
    
    return max(potential_tiers)
    