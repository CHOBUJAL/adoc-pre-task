# 유저관리
### 회원가입 (POST /users/signup)
- MySQL에 유저 정보 저장 (id, email, password_hash, created_at)
- 비밀번호는 해싱 처리 필요(일반 문자열 저장 금지)
### 로그인 (POST /users/login)
- 이메일과 비밀번호 확인 후, 다음을 반환:
- 짧은 만료 기간을 갖는 Access Token (예: 15분~1시간 내 만료)
- 더 긴 만료 기간을 갖는 Refresh Token (예: 7일~14일 내 만료)
- Refresh Token은 MySQL에 저장(또는 유저별로 관리)하여 이후 토큰 재발급 시 검증에 사용
### 토큰 재발급 (POST /users/refresh)
- Refresh Token을 검증 후, 새로운 Access Token 발급
- Refresh Token 또한 갱신할지 여부는 자율적으로 판단 (일반적으로 재발급 시 Refresh Token 유지 또는 재발급)
### 로그아웃 (POST /users/logout)
- Refresh Token 무효화 처리 (DB 상에서 해당 토큰 삭제 혹은 블랙리스트 처리 등)  

# 게시글 관리(CRUD)
### 게시글 생성 (POST /posts)
- Access Token 인증 필요
- MongoDB에 게시글 저장(id, title, content, author_id, created_at)
### 게시글 조회 (GET /posts/{post_id})
- 인증 불필요
- 지정한 post_id의 게시글 반환
### 게시글 리스트 조회 (GET /posts)
- 인증 불필요
- 페이지네이션(?page=1&page_size=10) 및 작성자 필터(?author_id=) 등의 간단한 기능 제공
### 게시글 수정 (PUT /posts/{post_id})
- Access Token 인증 필요
- 해당 게시글 작성자와 토큰 내 user_id가 일치해야 수정 가능
### 게시글 삭제 (DELETE /posts/{post_id})
- Access Token 인증 필요
- 해당 게시글 작성자와 토큰 내 user_id가 일치해야 삭제 가능