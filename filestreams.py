import boto3
from botocore.exceptions import NoCredentialsError
from googleapiclient.http import MediaIoBaseDownload
import io
import logging
import configparser

config_data = configparser.ConfigParser()
config_data.read("config.ini")

aws_s3 = config_data["aws_s3"]
gdrive = config_data["gdrive"]

from main import get_fileID,service_return

# Logging format : {TimeStamp} {Levelname:INFO} {Message}
logging.basicConfig(filename="Logs.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")

drive_service = service_return()

def upload_to_s3(bucket_name, file_stream,object_key):
    ACCESS_SECRET = aws_s3.get("access_secret")
    ACCESS_KEY = aws_s3.get("access_key")
    s3_client = boto3.client(aws_s3.get("name"), region_name=aws_s3.get("region_name"), aws_access_key_id=aws_s3.get("access_key"),
                            aws_secret_access_key=aws_s3.get("access_secret"))
    try:
        # Generate a unique object key based on the file name
        s3_client.upload_fileobj(file_stream, bucket_name, object_key)
        logging.info('File uploaded to Amazon S3 successfully.')
        
    except NoCredentialsError:
        logging.info('Credentials not found. Please configure AWS credentials.')
    except Exception as e:
        print(e)

# Example usage
bucket_name = aws_s3.get("bucket_name")

def upload_file_from_drive(file_id,object_key):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    # Download the file from Google Drive and save it in the file stream
    done = False
    while not done:
        _, done = downloader.next_chunk()

    # Set the file stream position to the beginning for uploading
    fh.seek(0)
    key = object_key
    # Upload the file stream to Amazon S3 using the original file name
    upload_to_s3(bucket_name, fh,key)

# Usage example
files_list = get_fileID(gdrive.get("folder_id"))

for file_name in files_list:
    # assigning key
    key = file_name.get("name")

    # assigning file name
    file_path = file_name.get("name")
        
    # assigning file id 
    file_id = file_name.get("id")
    
    upload_file_from_drive(file_id,key)