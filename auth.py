from __future__ import print_function
import os
import configparser

config_data = configparser.ConfigParser()
config_data.read("config.ini")

aws_s3 = config_data["aws_s3"]
gdrive = config_data["gdrive"]

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class auth:
    def __init__(self,SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME): # Inititalize the values which will remain constant
        self.SCOPES = gdrive.get("scopes")
        self.CLIENT_SECRET_FILE = gdrive.get("client_secret_file")
        self.APPLICATION_NAME = gdrive.get("application_name")
        
    def getCredentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        cwd_dir = os.getcwd() 
        credential_dir = os.path.join(cwd_dir, '.credentials') # Creating Sub-directory .credentials where api credentials will be stored
        
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                    'google-drive-credentials.json')

        store = Storage(credential_path)
        credentials = store.get() # get credentials from folder
        
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES) 
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials