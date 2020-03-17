# Ccomputing_prj
## Description

모듈은 Storage 역할을 하는 Amazon S3, 사용자에게 인터페이스를 제공하고 사용자의 명령을 수행하는 Web Interface, 유저들의 정보를 담고 있는 DB가 있다.
 S3에서는 파일 저장, 삭제, 다운로드 기능을 제공하며, 파일의 정보를 담고 있다. Web에서는 처음에는 로그인 기능이 있다. Id, Pw를 입력 받아서 로그인을 하면 DB에 있는 정보를 토대로 로그인 정보를 받아들인다. 회원가입을 하면 새로운 사용자를 DB에 추가시키고 원래 화면으로 돌아온다. 로그인이 성공한 상태에서는 파일 목록들을 보여주고 드래그 박스가 존재한다. 드래그 박스 안으로 파일을 드래그 하면 파일 업로드와 같은 기능을 하게 된다. 파일 목록에서 버튼으로 파일 업로드, 파일 삭제, 파일 다운로드 기능을 사용할 수 있다. DB에서는 유저에 대한 정보를 담고 있다.
사용자의 위치를 고려하여 최대한 가까운 데이터센터에 저장소를 만든다.

## Environment

OS - Linux Ubuntu IDE

IDE – Pycharm / VScode

Computing – AWS EC2

Storage –AWS S3

Database – postgreSQL

Language - html/css (FE), Python (BE)

Framework – Django 2.0

## Demo

![tttt](https://user-images.githubusercontent.com/38336997/64960260-f150a400-d8cd-11e9-817b-57f7d4ee3544.JPG)

[유튜브 데모 영상 링크](https://www.youtube.com/watch?v=WfI26buirWY&list=PLxCNGfkJ9D2rn8U2OJilnNhCBKbMVpEM3)
