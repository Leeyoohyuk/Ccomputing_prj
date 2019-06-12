from django.shortcuts import render, redirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from web import s3_interface
from Bloud import settings
from django.http import HttpResponse
import os
from web.serializers import FileSerializer


def home(request):
    if request.user.is_authenticated:
        return redirect('user_file', path = '')
    return render(request, 'registration/index.html')


def aboutus(request):
    return render(request, 'web/aboutus.html')


@login_required  # ¿Ï·á
def user_file(request, path):
    user = request.user
    data = s3_interface.dir_path(user.username, path)
    ret = data # 리스트 데이터를 ret에 저장하고
    ret['path'] = path # 패스key와 현재 경로를 추가한다.
    return render(request, 'web/user_file.html', ret)


@login_required  # ¿Ï·á
def text_file(request):
    user = request.user
    data = s3_interface.text_list(user.username)
    ret = data  # 리스트 데이터를 ret에 저장하고
    return render(request, 'web/extension_file.html', ret)


@login_required  # ¿Ï·á
def img_file(request):
    user = request.user
    data = s3_interface.img_list(user.username)
    ret = data  # 리스트 데이터를 ret에 저장하고
    return render(request, 'web/extension_file.html', ret)


@login_required  # ¿Ï·á
def media_file(request):
    user = request.user
    data = s3_interface.media_list(user.username)
    ret = data  # 리스트 데이터를 ret에 저장하고
    return render(request, 'web/extension_file.html', ret)


@login_required  # ¿Ï·á
def waste_file(request, path ='waste/'):
    user = request.user
    data = s3_interface.dir_path(user.username, path)
    ret = data  # 리스트 데이터를 ret에 저장하고
    ret['path'] = path  # 패스key와 현재 경로를 추가한다.
    return render(request, 'web/waste_file.html', ret)


@login_required # 완료
def file_upload(request, path="/"):
    file = request.FILES.get('file')
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

    return redirect('user_file', path=path)

@login_required  # ¿Ï·á
def create_folder(request, path):
    request.POST.get('dir_name')
    user = request.user
    s3_interface.make_directory(user.username, path)
    return redirect('user_file', path=path)


@login_required  # ¿Ï·á
def file_delete(request, path='/'):
    user = request.user
    s3_interface.delete_path(user.username, path)
    return redirect('waste_file')


@login_required  # ¿Ï·á
def file_copy(request, old_path, new_path):
    user = request.user
    s3_interface.copy_file(user.username, old_path, new_path)
    new_path = "/".join(new_path.split("/")[:-1])
    if new_path != '':
        new_path = new_path + '/'
    return redirect('user_file', path=new_path)


@login_required  # ¿Ï·á
def file_move(request, old_path, new_path):
    user = request.user
    s3_interface.move_file(user.username, old_path, new_path)
    return redirect('user_file', path='')


@login_required
def file_share(request, path=''):
    user = request.user
    url = (s3_interface.share_file(user.username, path))
    messages.info(request, url, extra_tags='safe')  # 메세지
    return redirect('user_file', path=path.replace(path.split('/')[-1], ''))


@login_required
def oAuth_signup(request, path=''):
    user = request.user
    print('\n\n\n'+user.first_name + str(user.date_joined))
    if s3_interface.exist_bucket(user.username+"-bloud-bucket-test") == False:
        s3_interface.make_bucket(user.username)
        s3_interface.make_directory(user.username, 'waste/')

    return redirect('user_file', path=path)