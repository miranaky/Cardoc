# 카닥

- 과제 출제 기업 정보
  - 기업명 : 카닥
  - [카닥](https://www.cardoc.co.kr/)
  - [wanted 채용공고 링크](https://www.wanted.co.kr/wd/57545)
  - 기간 : 2021.11.22 ~ 2021.11.29

<br>

## 사용 기술 및 Tools

> - Back-End : <img src="https://img.shields.io/badge/Python 3.9-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django 3.2-092E20?style=for-the-badge&logo=Django&logoColor=white"/>
> - Deploy : <img src="https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=Amazon&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Docker-0052CC?style=for-the-badge&logo=Docker&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github_actions-181717?style=for-the-badge&logo=Github&logoColor=white"/>
> - ETC : <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white"/>

<br>

## API 서버 주소

http://ec2-15-164-95-164.ap-northeast-2.compute.amazonaws.com

<br>

## 🏄‍♀️ 모델링

![Cardoc](https://user-images.githubusercontent.com/5153352/143731044-bbf05ce5-f7da-4941-97cd-4bac578a63af.png)

<br>

## API

[링크-postman document](https://documenter.getpostman.com/view/13670333/UVJbHxpH)

<br>

## 구현 기능

### 1. 서버 구조

배포된 서버의 구조는 다음과 같다.

![server](https://user-images.githubusercontent.com/5153352/143733589-1ecc9773-02e0-4cb3-9b28-02f8a8e88846.jpg)

<br>

클라이언트의 요청이 들어오면 Nginx, Gunicorn, Django 순으로 처리가 된다.
자동차 타이어 정보 저장 요청이 들어오면 자동차 차종ID를 갖고 자동차 정보 조회 API Server에 요청하여 타이어 정보를 얻는다. 이후 Database에 Column별로 저장한다.

### 2. 사용자 생성 및 로그인 API

    # 계정생성
    url : /api/v1/users/
    username, password를 이용하여 계정 생성
    계정 생성하면 200 ok status code 와 jwt token 을 access_token 으로 받음

    # SignIn
    url : /api/v1/users/login/
    username,password 를 이용하여 계정 로그인
    로그인이 되면 200 ok status code 와 jwt token 을 access_token 으로 받음

    계정이 있는 사용자만 아래 API 이용 가능

### 3. 사용자가 소유한 타이어 정보를 저장하는 API

    # 자동차 타이어 정보 저장
    url : /api/v1/tires/
    자동차 차종ID를 이용해서 사용자가 소유한 자동차 정보를 저장.
    한번에 최대 5개의 사용자정보와 자동차 차종ID를 받아서 API를 호출.
    차종별 타이어 정보는 자동차 정보 조회 API 에서 받아온다.
    타이어 정보는 앞/뒤 타이어 별로 폭,편평비,휠 사이즈를 유저 정보와, 유저의 자동차 차종 ID 함께 저장한다.
    한 사용자가 여러대의 자동차를 소유할 수 있기 때문에 한 유저가 여러개의 타이어 정보를 저장할 수 있다.

    Status Code 400 : 유저 정보가 DB에 없거나, 잘못된 차종ID를 작성하는 경우.  (여러 사용자 정보와 차종을 저장하려고 할 때 유저 정보가 없거나 잘못된 차종ID를 작성한다면 요청한 값 모두 저장되지 않는다.)
    Status Code 401 : 로그인 한 사용자만 정보를 저장할 수 있다.
    Status Code 500 : 자동차 정보 조회 API 에서 정보를 찾지 못하는 경우.

### 4. 사용자가 소유한 타이어 정보 조회 API

    # 자동차 타이어 정보 조회
    url : /api/v1/users/str:id/
    사용자 아이디를 통해서 유저에 저장된 타이어 정보를 조회할 수 있다.
    로그인 된 사용자(jwt token 을 갖은 사용자)만 정보를 조회할 수 있다.
    Status Code 401 : 로그인 되어 있지 않은 사용자
    Status Code 404 : 사용자 아이디가 없는 경우

<br>

## 설치 및 실행 방법

### Local 개발 및 테스트용

Docker 실행 혹은 일반 실행 중 선택

1. Docker

```bash
$ git clone https://github.com/miranaky/Cardoc.git && cd Cardoc
$ echo DJANGO_SECRET_KEY=local_secret_key >> .envs
$ echo DJANGO_ALLOWED_HOSTS="localhost testserver" >> .envs
$ docker-compose up --build -d
```

2. 일반 실행

```bash
$ git clone https://github.com/miranaky/Cardoc.git && cd Cardoc
$ pip install -r requirements.txt
$ export DJANGO_SECRET_KEY=local_secret_key
$ export DJANGO_ALLOWED_HOSTS="localhost testserver"
$ python manage.py runserver
```

### 배포 방법

Github에 develop,main 브런치로 push 되면 Github Action을 통하여 테스트 후 AWS EC2에 docker-compose로 자동 배포.

<br>

# Reference

이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 카닥에서 출제한 과제를 기반으로 만들었습니다.
