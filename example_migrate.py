from automationfx import *
import csv

fileLocation = "example_migration.csv" #e.g. r"C:\migration.txt"
with open(fileLocation) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV) ## skipping headers row
    for row in readCSV:
            print('Processing record - ' + str(row))
            #  Old phone name is required, New name or New Model is required. other fields are optional.
            #  Create Activation requires UCM 12.5+ and Device Default 'Onboarding Method' for model should be configured to 'Activation Code'
            response  = migrate(row[0],row[1],row[2],row[3],row[4])
            if 'Message' in response:
                print(response['Message'])
            elif 'Result' in response:
                print(response['Result'])
            else:
                print(response)