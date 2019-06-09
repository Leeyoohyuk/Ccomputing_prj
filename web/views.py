from django.shortcuts import render, redirect, Http404
from django.contrib.auth.decorators import login_required
from web import s3_interface
from Bloud import settings
from django.http import HttpResponse
import os
from web.serializers import FileSerializer


def home(request):
    return render(request, 'registration/index.html')

def aboutus(request):
    return render(request, 'web/aboutus.html')

# @login_required  # ¿Ï·á
# def file_list(request, path='/'):
#     user = request.user
#     data = s3_interface.list_path(s3_interface.BUCKET, user.username, path)
#     sort_option = request.GET.get('sort','')
#     if sort_option == 'time':
#         data['files'] = sorted(data['files'], key=lambda k: k['time'])
#     elif sort_option == 'name':
#         data['files'] = sorted(data['files'], key=lambda k: k['name'])
#     ret = data
#     ret['path'] = path
#     return render(request, 'web/file_list.html', ret)
# ---------------file list 수정됨 ---------------------------------------

@login_required  # ¿Ï·á
def file_list(request, path):
    user = request.user
    data = s3_interface.list_path(user.username, path)
    ret = data # 리스트 데이터를 ret에 저장하고
    print(ret)
    ret['path'] = path # 패스key와 현재 경로를 추가한다.
    print(ret)
    return render(request, 'web/file_list.html', ret)

#
# def docu_list(request, path ='/'):
#     user = request.user
#     data = s3_interface.list_path(s3_interface.BUCKET, user.username, path)
#     ret = data
#     ret['path'] = path
#     return render(request, 'web/file_list.html', ret)
#
#
# def img_list(request, path ='/'):
#     user = request.user
#     data = s3_interface.list_path(s3_interface.BUCKET, user.username, path)
#     ret = data
#     ret['path'] = path
#     return render(request, 'web/file_list.html', ret)
#
#
# def media_list(request, path ='/'):
#     user = request.user
#     data = s3_interface.list_path(s3_interface.BUCKET, user.username, path)
#     ret = data
#     ret['path'] = path
#     return render(request, 'web/file_list.html', ret)


def waste_list(request, path ='/'):
    user = request.user
    data = s3_interface.list_path(user.username, path)
    ret = data
    ret['path'] = path
    # return render(request, '--- 여기에 새로운 front ', ret)


@login_required # 완료
def file_upload(request, path="/"):
    file = request.FILES.get('file')
    # created = request.FILES.get('')
    files = {'file':file}
    file_serializer = FileSerializer(data=files)

    if file_serializer.is_valid():
        file_serializer.save()
        # upload to s3
        file_path = '.' + file_serializer.data.get('file')
        user = request.user
        data = s3_interface.upload_file(user.username, file_path,
                                        path + file_path.split('/')[-1])
        if os.path.exists(file_path):
            os.remove(file_path)

    return redirect('file_list', path=path)

@login_required  # ¿Ï·á
def create_folder(request, path):
    request.POST.get('dir_name')
    user = request.user
    s3_interface.make_directory(user.username, path)
    return redirect('file_list', path=path)


@login_required  # ¿Ï·á
def file_delete(request, path='/'):
    user = request.user
    s3_interface.delete_path(user.username, path)
    new_path = "/".join(path.split("/")[:-1])
    if new_path != '':
        new_path = new_path + '/'
    return redirect('file_list', path=new_path)


@login_required  # ¿Ï·á
def file_download(request, path):
    file = 'tempfile/' + path.split('/')[-1]
    user = request.user
    s3_interface.download_file(user.username, file, path)
    return redirect('file_list', path=path.replace(path.split('/')[-1], ''))


@login_required
def file_volume(request, path):
    user = request.user
    volume = s3_interface.volume_file(user.username, path)
    return redirect('file_list', path=path.replace(path.split('/')[-1], ''))


@login_required # ¿Ï·á
def file_view(request, path):
    file = 'tempfile/' + path.split('/')[-1]
    r_path = path.split('/')[-1]
    user = request.user
    s3_interface.download_file(user.username, file, path)
    file_path = os.path.join(settings.MEDIA_ROOT, r_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='text/plain')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@login_required  # ¿Ï·á
def file_copy(request, old_path, new_path):
    user = request.user
    s3_interface.copy_file(user.username, old_path, new_path)
    new_path = "/".join(new_path.split("/")[:-1])
    if new_path != '':
        new_path = new_path + '/'
    return redirect('file_list', path=new_path)


@login_required  # ¿Ï·á
def file_move(request, old_path, new_path):
    user = request.user
    s3_interface.move_file(user.username, old_path, new_path)
    new_path = "/".join(new_path.split("/")[:-1])
    if new_path != '':
        new_path = new_path + '/'
    return redirect('file_list', path=new_path)


@login_required  # ¿Ï·á ## new_path를 waste 경로로 설정해서 만든다, 초기에 waste폴더 생성해야함
def file_waste(request, path):
    user = request.user
    new_path = 'waste/' + path
    s3_interface.move_file(user.username, path, new_path)
    new_path = "/".join(new_path.split("/")[:-1])
    if new_path != '':
        new_path = new_path + '/'
    return redirect('waste_list', path=new_path)

@login_required
def oAuth_signup(request, path=''):
    user = request.user
    if s3_interface.exist_bucket(user.username+"-bloud-bucket-test") == False:
        s3_interface.make_bucket(user.username)
        s3_interface.make_directory(user.username, 'waste/')

    return redirect('file_list', path=path)