import boto3
from boto3.s3.transfer import TransferConfig
from Bloud import awsconf

S3 = boto3.client(
    's3',
    aws_access_key_id= awsconf.AWS_ACCESS_KEY_ID,
    aws_secret_access_key= awsconf.AWS_SECRET_ACCESS_KEY)
## Oauth로 로그인을하면 아이디가 ... 만들어지고 ... 이걸 가지고 버킷을 만드는데 원래는 signup에서 하던걸 ...

def list_path(user, path):
    files = []

    # get list
    objects = S3.list_objects(Bucket=user + "-bloud-bucket-test", Prefix='{}'.format(path), Delimiter='/')
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
                files.append({'type':'file', 'name':file, 'time':obj.get("LastModified"), 'volume':obj.get('Size')})

    return {'files':files}

    # if key.size > 1024 * 1024 * 1024:
    #     volume = str(round(key.size / 1024 * 1024 * 1024, 2)) + 'GB'
    # elif key.size > 1024 * 1024:
    #     volume = str(round(key.size/1024*1024, 2)) + 'GB'
    # elif key.size > 1024:
    #     volume = str(round(key.size/1024, 2)) + 'MB'
    # else:
    #     volume = str(round(key.size, 2)) + 'B'
# def extension_list(bucket, user):
#     files = []
#     # get list
#     objects = S3.list_objects(Bucket=bucket, Prefix='{}/'.format(user), Delimiter='/')
#
#     # get sub directorys
#     common_prefixes = objects.get('CommonPrefixes')
#     if common_prefixes:
#         for obj in common_prefixes:
#             files.append({'type': 'directory', 'name': obj.get('Prefix').split('/')[-2]})
#
#     # get files
#     contents = objects.get('Contents')
#     if contents:
#         for obj in contents:
#             file = obj.get('Key').split('/')[-1]
#             if file != '':
#                 files.append({'type': 'file', 'name': file, 'time': obj.get("LastModified")})
#     return {'files': files}
#


def exist_bucket(name):
    s3 = boto3.resource('s3', aws_access_key_id= awsconf.AWS_ACCESS_KEY_ID,
    aws_secret_access_key= awsconf.AWS_SECRET_ACCESS_KEY)
    return (s3.Bucket(name) in s3.buckets.all())


def upload_file(user, local_path, key):
    GB = 1024 ** 3
    config = TransferConfig(multipart_threshold=5 * GB)
    return S3.upload_file(local_path, user + "-bloud-bucket-test", key, Config = config)


def download_file(user, local_path, key):
    return S3.download_file(user + "-bloud-bucket-test", key, local_path)


def delete_path(user, path):
    return S3.delete_object(Bucket=user + "-bloud-bucket-test", Key=path)


def make_directory(user, path):
    return S3.put_object(Bucket=user + "-bloud-bucket-test", Key=path)


def make_bucket(user):
    return S3.create_bucket(Bucket=user + "-bloud-bucket-test", CreateBucketConfiguration={
        'LocationConstraint': 'ap-northeast-2'})


def move_file(user, old_path, new_path):
    S3.copy_object(Bucket=user + "-bloud-bucket-test", CopySource=user + "-bloud-bucket-test/" + old_path, Key=new_path)
    S3.delete_object(Bucket=user + "-bloud-bucket-test", Key=old_path)
    return


def copy_file(user, old_path, new_path):
    S3.copy_object(Bucket= user + "-bloud-bucket-test", CopySource=user + "-bloud-bucket-test/" + old_path, Key=new_path)
    return