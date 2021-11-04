# Assignment2

원티드x위코드 백엔드 프리온보딩 과제2
- 과제 출제 기업 정보
  - 기업명 : 마피아컴퍼니
  - [마피아컴퍼니 사이트](http://www.mapiacompany.com/)
  - [wanted 채용공고 링크](https://www.wanted.co.kr/company/6137)

## Members
|이름   |github                   |담당 기능|
|-------|-------------------------|--------------------|
|김태우 |[jotasic](https://github.com/jotasic)     |    |
|고유영 |[lunayyko](https://github.com/lunayyko)   |    |
|박지원 |[jiwon5304](https://github.com/jiwon5304) |   |
|최신혁 |[shchoi94](https://github.com/shchoi94) |   |
|박세원 |[sw-develop](https://github.com/sw-develop) |   |
|

## 과제 내용
> 아래의 상황을 읽고 요구사항을 구현해주세요!
>
- 마피아컴퍼니 선호 기술스택
    - Python/FastAPI
    - Javascript 사용시 선호 프레임워크 없음
- 사용 필수 데이터 베이스
    - neo4j GraphDB
    - 개발 완료 시 리뷰어가 실행해볼 수 있도록 neo4j 디비를 csv 로 export해서 프로젝트 루트 경로에 포함해주세요.
- API 구성은 Restful API 형태로 구성하시면 됩니다.
    - GraphQL로 구현하면 가산점이 있습니다.
        - Strawberry graphql 라이브러리 추천
        - CUD는 GraphQL Mutation 으로 만들지 않고, Restful로 만들어주세요.

### [필수 포함 사항]

- READ.ME 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - 완료된 시스템이 배포된 서버의 주소
    - Swagger나 Postman을 통한 API 테스트할때 필요한 상세 방법
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현

### [과제 안내]
- 음악 스트리밍 서비스에는 3가지 요소 `뮤지션` `곡` `앨범` 이 존재합니다.
   
- 앨범 페이지, 뮤지션 페이지, 곡 페이지에 인접 정보들 (ex, 곡의 뮤지션, 곡의 앨범) 을 표현할 수 있도록 **CRUD** API를 구성해주세요.
   
- 이 페이지들에 대한 DB를 구성할 때 `곡` - `뮤지션` 연결과  `곡` 

- `앨범` 연결은 내부 운영팀에서 직접 연결 가능하지만, `뮤지션` - `앨범` 정보까지 태깅하기엔 내부 운영 리소스가 부족한 상황으로 가정해보겠습니다. 

- 이 때, `뮤지션` - `곡` 이 연결되어있고  `곡` - `앨범` 이 연결되어있다면  `뮤지션` - `[곡*]` - `앨범` 연결되어있다고 판단할 수 있는데요. 이 특성을 이용해서 `뮤지션` 의 `앨범` 을 보여주는 Read API, 특정 `앨범` 의 뮤지션 목록을 보여주는 Read API를 만들어주세요. 

**각 요구사항을 아래에 명시해두었습니다.**
- 화면별 Read API 요구사항
   -  `곡` 페이지 
       - 해당 `곡`이 속한 `앨범`을 가져오는 API
       - 해당 `곡`을 쓴 `뮤지션` 목록을 가져오는 API 
    - `앨범` 페이지  
      - 해당 `앨범`을 쓴 `뮤지션` 목록 가져오는 API
      - 해당 `앨범`의 `곡` 목록을 가져오는 API
    - `뮤지션` 페이지 
      - 해당 `뮤지션`의 모든 `앨범` API
      - 해당 `뮤지션`의 `곡` 목록 가져오는 API

- **Create, Update, Delete API 요구사항**
    - `곡` 생성 API
    - `앨범` 생성 API
    - `뮤지션` 생성 API
    - `뮤지션` - `곡` 연결/연결해제 API
    - `곡` - `앨범` 연결/연결해제 API
    - `뮤지션` - `앨범` 연결/연결해제 API 는 필요하지 않습니다. (구현 X)
        - `뮤지션` - `곡` 연결과 `곡` - `앨범` 연결이 되어있으면
        GraphDB (neo4j) 에서 `뮤지션` - [*] - `앨범` 연결 여부를 뽑을 수 있습니다. **이 특성을 Read API에서 활용**해주세요.

- Neo4j DB 테이블 요구사항
  - `뮤지션`, `곡`, `앨범`은 각각의 테이블 (musician, song, album)로 구성되어야합니다.
  -  `앨범` 안에는 여러 `곡`이 속해있을 수 있습니다.
  - 한 `곡`에는 여러 `뮤지션`이 참여할 수 있습니다.
  - 한 `곡`은 `앨범` 1개에만 들어가있습니다.
  - `뮤지션`은 여러 앨범을 갖고 있을 수 있습니다.
  -  `뮤지션`, `앨범`, `곡` 데이터는 위 relation을 테스트할 수 있을만큼 임의로 생성해주시면 좋습니다.

- **FastAPI 프레임워크 요구사항**
    - Restful API로 구현하셨을 경우, FastAPI의 OpenAPI로 API 문서화해주세요.


## 사용 기술 및 tools
> - Back-End :  <img src="https://img.shields.io/badge/Python 3.8-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django 3.2-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/neo4j 4.2-0d73ff?style=for-the-badge&logo=neo4j&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/graphql-d31195?style=for-the-badge&logo=Graphql&logoColor=white"/>
> - Deploy : <img src="https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=Amazon&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Docker-0052CC?style=for-the-badge&logo=Docker&logoColor=white"/>
> - ETC :  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/SWAGGER-5B8C04?style=for-the-badge&logo=Swagger&logoColor=white"/>

## 모델링
**😅추후입력**

## API
**😅추후입력**

## 구현 기능
**😅추후입력**

### Docker
- 팀원들의 빠른 개발환경 셋팅을 위해서 로컬 개발용과 배포용 docker-compose 파일을 만들어서 적용하였습니다.
- 개발용 환경을 구축했을 시 장점은 팀원들의 개발환경 셋팅시간을 줄여줘서 구현에 더 집중 할 수 있습니다.
- 배포용 환경을 구축했을 시에는 일일이 셋팅을 한다고하면, 아무래도 서버와 로컬간의 OS 같은 환경에 차이로 인해서 시간를 낭비 할 수도 있으며 특히, 배포시마다 이러한 상황이 반복될 수 있다는 것인데, docker를 통해서 이러한 시간낭비를 줄 일 수 있다는 장점이 있습니다. 

## 배포정보
|구분   |  정보          |비고|
|-------|----------------|----|
|배포플랫폼 | AWS EC2    |    |
|API 주소 |              |    |
|Doc 주소 |              |    |
|

## API TEST 방법
**😅추후입력**

## 설치 및 실행 방법
###  Local 개발 및 테스트용
1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
    ```bash
    git clone https://github.com/Wanted-Preonboarding-Backend-1st-G5/Assignment2
    cd Assignment2
    ```
2. 가상 환경을 만들고 프로젝트에 사용한 python package를 받는다.
   1. Miniconda 사용시
        ```bash
        conda create --name Assignment1-TW-JW-YY python=3.8
        conda actvate Assignment1-TW-JW-YY
        pip install -r requirements.txt
        ```

   2. VirtualEnv 사용시

**😅추후입력**

###  배포용 
1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
    
    ```bash
    git clone https://github.com/Wanted-Preonboarding-Backend-1st-G5/Assignment2
    cd Assignment2
    ```
2. .dockerenv.deploy 파일을 만들어서 안에 다음과 같은 내용을 입력한다. manage.py와 같은 폴더에 생성한다.
    
    ```text
    # .dockerenv.deploy
    ```
3. docker-compose를 통해서 db와 서버를 실행시킨다.
    
    ```bash
    docker-compose -f docker-compose-deploy.yml up
    ```
4. 만약 백그라운드에서 실행하고 싶을 시 `-d` 옵션을 추가한다.
    ```bash
    docker-compose -f docker-compose-deploy.yml up -d
    ```

## 폴더 구조
**😅추후입력**

```bash

```

## TIL정리 (Blog)
- 김태우 :
- 고유영 :
- 박지원 :
- 최신혁 :
- 박세원 :

# Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 마피아컴퍼니에서 출제한 과제를 기반으로 만들었습니다.
