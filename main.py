from __future__ import print_function
import httplib2
import os
import io
import configparser

config_data = configparser.ConfigParser()
config_data.read("config.ini")

aws_s3 = config_data["aws_s3"]
gdrive = config_data["gdrive"]

from googleapiclient import discovery
from googleapiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

import auth

def service_return():    
    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/drive-python-quickstart.json
    SCOPES = gdrive.get("scopes")
    CLIENT_SECRET_FILE = gdrive.get("client_secret_file")
    APPLICATION_NAME = gdrive.get("application_name")

    authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
    credentials = authInst.getCredentials()

    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http)
    return drive_service

def downloadFile(file_id,filepath):
    drive_service = service_return()

    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    
    downloader = MediaIoBaseDownload(fh, request)
    return downloader
    '''done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())'''


def get_fileID(folder_id):
    drive_service = service_return()

    page_token = None
    files = []
    while True:
        results = drive_service.files().list(q=f"'{folder_id}' in parents",spaces='drive',fields='nextPageToken, files(id, name, mimeType)',pageToken=page_token).execute()
        files.extend(results['files'])
        page_token = results.get('nextPageToken')
        if not page_token:
            break

    return files # return file detail

    '''print(files)
    for file in files:
        file_id = file['id']
        file_name = file['name']
        downloadFile(file_id,"GDrive/"+file_name)'''