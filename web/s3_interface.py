import boto3
from boto3.s3.transfer import TransferConfig
from botocore.config import Config

from Bloud import awsconf

S3 = boto3.client(
    's3',
    region_name='ap-northeast-2',
    aws_access_key_id= awsconf.AWS_ACCESS_KEY_ID,
    aws_secret_access_key= awsconf.AWS_SECRET_ACCESS_KEY,
    config=Config(signature_version='s3v4')
)

S3source = boto3.resource('s3', aws_access_key_id=awsconf.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=awsconf.AWS_SECRET_ACCESS_KEY,
                          )

def dir_path(user, path):
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
    print('dir path end')
    return {'files':files}


def text_list(user):
    my_bucket = S3source.Bucket(user+"-bloud-bucket-test")
    files = my_bucket.objects.all()
    file_list = []
    for file in files:
        print(file.key[:6])
        if file != '' and file.key[:6] != 'waste/' and (file.key.endswith('.docx') or file.key.endswith('.txt') or file.key.endswith('.hwp') or file.key.endswith('.xlsx')):
            file_list.append({'type': 'file', 'name': file.key.split('/')[-1], 'time': file.get("LastModified")})

    return {'files': file_list}


def img_list(user):
    my_bucket = S3source.Bucket(user + "-bloud-bucket-test")
    files = my_bucket.objects.all()
    file_list = []
    for file in files:
        if file != '' and file.key[:6] != 'waste/' and (file.key.endswith('.jpg') or file.key.endswith('.png') or file.key.endswith('.bmp')):
            file_list.append({'type': 'file', 'name': file.key.split('/')[-1] , 'time': file.get("LastModified")})

    return {'files': file_list}


def media_list(user):
    my_bucket = S3source.Bucket(user + "-bloud-bucket-test")
    files = my_bucket.objects.all()
    file_list = []
    for file in files:
        if file != '' and file.key[:6] != 'waste/' and (file.key.endswith('.mp3') or file.key.endswith('.mp4')):
            file_list.append({'type': 'file', 'name': file.key.split('/')[-1], 'time': file.get("LastModified")})

    return {'files': file_list}


def exist_bucket(name):
    return (S3source.Bucket(name) in S3source.buckets.all())


def upload_file(user, local_path, key):
    GB = 1024 ** 3
    config = TransferConfig(multipart_threshold=5 * GB)
    return S3.upload_file(local_path, user + "-bloud-bucket-test", key, Config = config)


def download_file(user, path):
    url = S3.generate_presigned_url('get_object',
                                                Params={'Bucket': user+"-bloud-bucket-test",
                                                        'Key': path},
                                                ExpiresIn=60)
    print(url)
    return url


def delete_path(user, path):
    return S3.delete_object(Bucket=user + "-bloud-bucket-test", Key=path)


def make_directory(user, path):
    return S3.put_object(Bucket=user + "-bloud-bucket-test", Key=path)


def make_bucket(user):
    return S3.create_bucket(Bucket=user + "-bloud-bucket-test", CreateBucketConfiguration={
        'LocationConstraint': 'ap-northeast-2'})


def share_file(user, path):
    url = S3.generate_presigned_url('get_object',
                                                Params={'Bucket': user+ "-bloud-bucket-test",
                                                        'Key': path},
                                                ExpiresIn=120)
    print(url)
    return url


def move_file(user, old_path, new_path):
    S3.copy_object(Bucket=user + "-bloud-bucket-test", CopySource=user + "-bloud-bucket-test/" + old_path, Key=new_path)
    S3.delete_object(Bucket=user + "-bloud-bucket-test", Key=old_path)
    return


def copy_file(user, old_path, new_path):
    S3.copy_object(Bucket= user + "-bloud-bucket-test", CopySource=user + "-bloud-bucket-test/" + old_path, Key=new_path)
    return