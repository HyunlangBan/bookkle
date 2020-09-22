## Introduction
![](https://images.velog.io/images/langssi/post/bddeb890-64e7-4abf-bccd-787b5ddb4ff4/logo.0011.jpg)

* 도서에 대한 리뷰를 작성하거나 작성된 리뷰를 추천할 수 있고, 좋아하는 리뷰어를 팔로우하여 리뷰를 모아볼 수 있는 웹사이트를 기획하고 개발하였습니다.
* 개발기간 : 2020.09.07 ~ 2020.09.21(약 2주)
* 개발인원 : 2 (Frontend: 손혜인, Backend: 반현랑)
* [Front-end Github](https://github.com/hyenees/bookkle)

## Demo
💁🏻‍♀️ 클릭해주세요 

[![bookkle-video](https://images.velog.io/images/langssi/post/5eba2c73-155e-4112-8975-b7b7afa41b3f/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202020-09-22%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.36.44.png)](https://youtu.be/B2Zk-3WA3o0)
## Models
![](https://images.velog.io/images/langssi/post/7d23486b-ad5d-492d-b7cd-0fdf1d033b24/image.png)

## Technologies

* Python
* Django REST Framework
* MySQL
* Git
* AWS EC2, RDS
* Docker

## Features
- USER
  - 이메일 인증을 통한 회원가입, 로그인
  - 유저 팔로우
- REVIEW
  - 리뷰 CRUD
  - 전체 리뷰 리스트
  - 내가 작성한 리뷰 리스트
  - 팔로잉하는 유저들의 리뷰 모아보기
  - 등록한 글귀 랜덤 선택
  - 리뷰 추천(좋아요)
  - Permission
    - IsAuthenticated (로그인된 유저만 허용)
    - IsAuthorOrReadOnly (작성자가 아니면 읽기만 허용)
