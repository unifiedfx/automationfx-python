from automationfx import *
from tempfile import NamedTemporaryFile
import shutil
import csv
import json
import pyqrcode
import io
import base64
from datetime import datetime
import os

from colorama import init
init(True)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MigrateClient:
    filename = None
    rows_dict = None
    headers = None
    output_filename = 'migration_results_{0}.csv'.format(
        int(datetime.now().timestamp()))
    output_headers = ['DeviceName', 'NewName', 'NewModel', 'ActivationCode',
                      'ActivationCodeExpiry', 'Email', 'FirstName', 'LastName', 'Result']

    def read_inputfile(self, input_file):
        self.filename = input_file
        if not os.path.isfile(self.filename):
            print("{0}File Not Found ({1})".format(bcolors.FAIL,self.filename))
            return False
        else:
            with open(self.filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                self.headers = reader.fieldnames
                if not 'status' in self.headers:
                    self.headers.append('status')
                source = list(reader)
                self.rows_dict = json.loads(json.dumps(source))
                return True

    def migrate(self, input_file='example_migration.csv', process_all_records=False):
        result = self.read_inputfile(input_file)
        if result and self.rows_dict is not None and len(self.rows_dict) > 0:
            with open(self.output_filename, 'w', newline='') as outputFile:
                writer = csv.DictWriter(outputFile, fieldnames=self.output_headers)
                writer.writeheader()
            for row in self.rows_dict:
                if process_all_records:
                    self.process_row(row)
                else:
                    if row['status'] is None or not row['status'].startswith("Success"):
                        self.process_row(row)

    def process_row(self, row):
        print('\nProcessing record - ' + str(row))
        response = migrate(row['oldphone'], row['newphone'], row['newmodel'],
                           row['newprotocol'], row['createactivationcode'])
        if 'Message' in response:
            row['status'] = "Failed ({0})".format(response['Message'])
            self.update_inputfile()
            print(bcolors.FAIL + response['Message'])
        elif 'Result' in response:
            print( bcolors.OKGREEN+ "Migration Result: " + response['Result'])
            if row['createactivationcode'] and not response['ActivationCode']:
                print(bcolors.WARNING + "Unable to create activation code, Requires UCM 12.5+ and Device Default 'Onboarding Method' for model should be configured to 'Activation Code'")
            if response['Success']:
                row['status'] = response['Result']
                self.wirte_result(response)
            else:
                row['status'] = "Failed ({0})".format(response['Result'])
            self.update_inputfile()                
        else:
            print(response)
            row['status'] = "Unknown, " + response
            self.update_inputfile()
    
    def wirte_result(self, response):
        with open(self.output_filename, 'a', newline='') as outputFile:
            writer = csv.DictWriter(outputFile, fieldnames=self.output_headers)
            outputrow = {}
            for item in self.output_headers:
                outputrow[item] = response[item]
            writer.writerow(outputrow)

    def update_inputfile(self):
        tempfile = NamedTemporaryFile(delete=False)
        with open(tempfile.name, 'w', newline='') as tempf:
            writer = csv.DictWriter(tempf, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self.rows_dict)
            tempfile.close()
        shutil.move(tempfile.name, self.filename)

    def send_activation_email(self, smtp_client, filePath = None):
        if(filePath is None):
            path = os.getcwd()
            files = []
            for i in os.listdir(path):
                if os.path.isfile(os.path.join(path,i)) and 'migration_results' in i and '.csv' in i:
                    files.append(i)
            files.sort(reverse=True)
            filePath = files[0]
        with open(filePath) as inputFile:
            print( "\n"+ bcolors.OKBLUE +"Sending activation email/s for result file: " + filePath)
            readCSV = csv.DictReader(inputFile, delimiter=',')
            for row in readCSV:
                print("\nSending email: " + str(row))
                encoded = self.generate_base64_qrcode(row['ActivationCode'])
                renderdata = {'fname': row['FirstName'],'lname': row['LastName'], 'code': row['ActivationCode'], 'email': row['Email'], 'expiry': row['ActivationCodeExpiry'], 'qrcode': encoded}
                smtp_client.send_email(row['Email'],renderdata)
                    
    def generate_base64_qrcode(self, data, qrscale = 6):
        c = pyqrcode.create(data)
        s = io.BytesIO()
        c.png(s,scale = qrscale)
        encoded = base64.b64encode(s.getvalue()).decode("ascii")
        return encoded