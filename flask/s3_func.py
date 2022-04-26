import logging
import boto3
from botocore.exceptions import ClientError
import os

# from numpy import source

def create_bucket(bucket_name, region=None):
    try:
        print("Bucket creating:")
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
        print("Bucket created!")
    except ClientError as e:
        logging.error(e)
        return False
    return True

# create_bucket('riya1-source-bucket','us-east-2')
# create_bucket('riya1-dest-bucket','us-east-2')

def list_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')
    return response

# list_buckets()

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print("File uploaded in the bucket")
    except ClientError as e:
        logging.error(e)
        return False
    return response

# upload_file('nature.jpeg','riya1-source-bucket',)



def download_file(file_name, bucket):
    s3 = boto3.resource('s3')
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)
    print("Downloaded")
    return output

# download_file('nature.jpeg','riya1-source-bucket')

def list_files(bucket):
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)
        print(item['Key'])
    return contents

# list_files('riya1-source-bucket')




def delete_bucket(bucket_name):
    s3 = boto3.client('s3')
    try:
        s3.head_bucket(Bucket=bucket_name)
        print("Bucket exists....STart deleteing")
        response = s3.delete_bucket(Bucket=bucket_name)
        print("Deleted")
        print(response)
    except ClientError:
        print("BUcket does not exist")
        return False
    return True

# delete_bucket('riya-dest-bucket')
