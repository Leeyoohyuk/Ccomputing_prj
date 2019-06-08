import boto3
from boto3.s3.transfer import TransferConfig
from Bloud import awsconf

S3 = boto3.client(
    's3',
    aws_access_key_id= awsconf.AWS_ACCESS_KEY_ID,
    aws_secret_access_key= awsconf.AWS_SECRET_ACCESS_KEY)
BUCKET = awsconf.AWS_STORAGE_BUCKET_NAME


def list_path(bucket, user, path):
    files = []
    # get list
    objects = S3.list_objects(Bucket=bucket, Prefix='{}/{}'.format(user, path), Delimiter='/')

    # get sub directorys
    common_prefixes = objects.get('CommonPrefixes')
    if common_prefixes:
        for obj in common_prefixes:
            files.append({'type':'directory', 'name':obj.get('Prefix').split('/')[-2]})

    # get files
    contents = objects.get('Contents')
    if contents:
        for obj in contents:
            file = obj.get('Key').split('/')[-1]
            if file != '':
                files.append({'type':'file', 'name':file, 'time':obj.get("LastModified")})
    return {'files':files}

def extension_list(bucket, user):
    files = []
    # get list
    objects = S3.list_objects(Bucket=bucket, Prefix='{}/'.format(user), Delimiter='/')

    # get sub directorys
    common_prefixes = objects.get('CommonPrefixes')
    if common_prefixes:
        for obj in common_prefixes:
            files.append({'type': 'directory', 'name': obj.get('Prefix').split('/')[-2]})

    # get files
    contents = objects.get('Contents')
    if contents:
        for obj in contents:
            file = obj.get('Key').split('/')[-1]
            if file != '':
                files.append({'type': 'file', 'name': file, 'time': obj.get("LastModified")})
    return {'files': files}
 

def upload_file(bucket, user, local_path, key):
    print('업로드 시작 ')
    GB = 1024 ** 3
    config = TransferConfig(multipart_threshold=5 * GB)
    return S3.upload_file(local_path, bucket, user+"/"+key, Config = config)


def download_file(bucket, user, local_path, key):
    return S3.download_file(bucket, user+"/"+key, local_path)


def delete_path(bucket, user, path):
    return S3.delete_object(Bucket=bucket, Key=user+"/"+path)


def make_directory(bucket, user, path):
    return S3.put_object(Bucket=bucket, Key=user+"/"+path)


def move_file(bucket, user, old_path, new_path):
    S3.copy_object(Bucket=bucket, CopySource=bucket+"/"+user+"/"+old_path, Key=user+"/"+new_path)
    S3.delete_object(Bucket=bucket, Key=user+"/"+old_path)
    return


def copy_file(bucket, user, old_path, new_path):
    S3.copy_object(Bucket=bucket, CopySource=bucket+"/"+user+"/"+old_path, Key=user+"/"+new_path)
    return
