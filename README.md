# 비바이노베이션 사전 과제
## 개요
#### 가상환경(의존성 관리 및 환경 설정) : poetry
#### 데이터베이스 마이그레이션(스키마 관리) : alembic
#### Test(단위 테스트 및 커버리지 측정) : pytest
#### Linter(코드 품질 검사 및 포매팅): ruff
#### docker Compose를 활용해 게시판 애플리케이션(백엔드, MySQL, MongoDB)을 컨테이너로 실행

## 서버 실행 방법
#### 로컬 환경에서 docker compose 기반 동작
#### BackEnd, Mysql, MongoDB 모두 하나의 compose에 종속
- 설정 파일은 app/core/settings.py 참조
```
docker compose up -d
(DB 마이그레이션의 경우, 서버가 정상적으로 동작되면 자동 마이그레이션 진행되게 세팅)
```
#### 동작중인 컨테이너 로그 확인
```
docker logs "container_name" -f
```
#### 데이터베이스 수동 마이그레이션
```
docker exec -it adoc-backend alembic upgrade head
```
### Test 진행(pytest)
```
docker exec -it adoc-backend pytest --cov=app --cov-report=term-missing -v
(test 목록은 app/tests 디렉토리에 존재)
```


## API 목록
### API 문서 확인
- 서버가 정상적으로 동작하면 다음 경로에서 API 문서를 확인
  - Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
    - 요청/응답 구조 및 테스트 UI 제공
  - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
    - OpenAPI 스펙(JSON) 다운로드 및 상세 문서 제공
### 1. 유저관리
- User 모델과 RefreshToken 모델 1:1 관계 매핑
- Token 전략
```
login 요청 시, access token 갱신
login 요청 시, refresh token이 만료되었거나 존재하지 않으면 생성 및 업데이트
access token 재발급 요청 시 "access token 유효 and refresh token 유효" 인 경우 재발급
(token 유효시간은 app/core/settings.py를 참조)
logout이면 요청 유저의 refresh token 삭제
```
1. **회원가입** (POST /users/signup)
2. **로그인** (POST /users/login)
3. **토큰 재발급** (POST /users/refresh)
4. **로그아웃** (POST /users/logout)

### 2. 게시글 관리(CRUD)
1. **게시글 생성** (POST /posts)
2. **게시글 조회** (GET /posts/{post_id})
3. **게시글 리스트 조회** (GET /posts)
4. **게시글 수정** (PUT /posts/{post_id})
5. **게시글 삭제** (DELETE /posts/{post_id})