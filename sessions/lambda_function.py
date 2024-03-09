# lambda_function.py

import boto3
import os
import email
import logging
from email.utils import parseaddr
from datetime import datetime

s3 = boto3.client("s3")

logging.getLogger('__main__').setLevel(logging.DEBUG)
logging.getLogger('botocore').setLevel(logging.WARN)

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    destination_folder = os.environ['PROCESSED_EMAILS_FOLDER']
    main_folder = os.environ['MAIN_EMAILS_FOLDER']

    if not event or 'Records' not in event:
        logging.debug("No valid event records found.")
        return None

    for record in event['Records']:
        s3_event = record['s3']
        object_key = s3_event['object']['key']

        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response['Body'].read()

        # Create an email message object using the content of the file
        msg = email.message_from_bytes(file_content)

        # Extract relevant information from the email message
        subject = msg['Subject']
        sender  = parseaddr(msg['From'])[1] 
        recipient = parseaddr(msg['To'])[1] 

        date = datetime.utcnow().strftime('%Y-%m-%d')  # Use current UTC date and time

        # Concatenate the components into a raw file name
        raw_filename = f"{subject}_{recipient}_{sender}"

        # Sanitize the file name
        filename = raw_filename.replace(' ', '-').replace('<', '').replace('>', '').replace('/', '') + ".eml"

        # Add the folder path
        if destination_folder == main_folder:
            logging.error(f"Destination folder '{destination_folder}' is the same as the main folder.")
            return {"status": "error"}        

        # Add the folder path
        s3_key= os.path.join(destination_folder, date, filename)

        # Copy the object
        s3.copy_object(Bucket=bucket_name, 
                        CopySource={'Bucket': bucket_name, 'Key': object_key}, 
                        Key=s3_key)
        logging.debug(f"Converted inbound email to .eml and copied to: {s3_key}")
