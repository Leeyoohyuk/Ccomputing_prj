from django.conf.urls import url
from django.shortcuts import redirect
from django.urls import path
from web import views, auth_views

urlpatterns = [
    url(r'^accounts/login/$', auth_views.signin, name='signin'),
    url(r'^accounts/signup/$', auth_views.signup, name='signup'),
    url(r'^accounts/delete_account/$', auth_views.delete_account, name='delete_account'),
    url(r'^accounts/delete_account_success/$', auth_views.delete_account_success, name='delete_account_success'),

    # blog
    url(r'^$', views.home, name='home'),
    url(r'^aboutus/$', views.aboutus, name='aboutus'),
    url(r'^waste/$', views.waste_file, name='waste_file'),
    url(r'^text/$', views.text_file, name='text_file'),
    url(r'^img/$', views.img_file, name='img_file'),
    url(r'^media/$', views.media_file, name='media_file'),
    url(r'^file/(?P<path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/)*)$', views.user_file, name='user_file'),
    url(r'^upload/(?P<path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/)*)$', views.file_upload,
        name='file_upload'),
    url(r'^view/(?P<path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/*)*)$', views.file_view, name='file_view'),
    url(r'^create_folder/(?P<path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/)*)$', views.create_folder,
        name='create_folder'),
    url(
        r'^copy/(?P<old_path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/*)*)&(?P<new_path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]]*/*)*)$',
        views.file_copy, name='file_copy'),
    url(
        r'^towaste/(?P<old_path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/*)*)&(?P<new_path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]]*/*)*)$',
        views.file_move, name='throw'),
    url(
        r'^restore/(?P<old_path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/*)*)&(?P<new_path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]]*/*)*)$',
        views.file_move, name='restore'),
    url(r'^delete/(?P<path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/*)*)$', views.file_delete,
        name='file_delete'),
    url(r'^download/(?P<path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/*)*)$', views.file_download,
        name='file_download'),
    url(r'^share/(?P<path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/*)*)$', views.file_share,
        name='file_share'),
]