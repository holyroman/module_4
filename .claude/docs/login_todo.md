# Login 기능 개발 계획

## Feature 1: 사용자 모델 및 데이터베이스 설계

### BE
- [ ] User 모델 생성 (`backend/app/models/user.py`)
  - id (Primary Key)
  - email (Unique, Index)
  - username (Unique)
  - hashed_password
  - is_active (Boolean)
  - created_at, updated_at (Timestamp)
- [ ] User 스키마 생성 (`backend/app/schemas/user.py`)
  - UserCreate (회원가입 요청)
  - UserLogin (로그인 요청)
  - UserResponse (응답 데이터)
  - Token (토큰 응답)
- [ ] 데이터베이스 마이그레이션 적용

### FE
- [ ] User 타입 정의 (`frontend/src/types/user.ts`)
- [ ] API 응답 타입 정의

---

## Feature 2: 인증 유틸리티 구현

### BE
- [ ] 비밀번호 해싱 함수 구현 (`backend/app/utils/auth.py`)
  - bcrypt를 사용한 password hashing
  - verify_password 함수
- [ ] JWT 토큰 생성/검증 함수 구현
  - create_access_token
  - decode_access_token
  - SECRET_KEY 및 ALGORITHM 설정
- [ ] 환경변수 설정 (.env)
  - SECRET_KEY
  - ACCESS_TOKEN_EXPIRE_MINUTES

### FE
- [ ] 토큰 저장/조회/삭제 유틸리티 (`frontend/src/utils/token.ts`)
  - localStorage 또는 cookie 활용
  - getToken, setToken, removeToken 함수

---

## Feature 3: 회원가입 API 개발

### BE
- [ ] 회원가입 엔드포인트 구현 (`backend/app/routers/auth.py`)
  - POST /api/auth/register
  - 이메일 중복 체크
  - 비밀번호 해싱 후 저장
  - 성공 시 사용자 정보 반환
- [ ] 입력 검증 로직
  - 이메일 형식 검증
  - 비밀번호 강도 검증 (최소 8자 이상)
  - 필수 필드 체크

### FE
- [ ] 회원가입 페이지 UI (`frontend/src/app/register/page.tsx`)
  - 이메일, 사용자명, 비밀번호, 비밀번호 확인 입력 필드
  - 폼 검증 (클라이언트 사이드)
  - 에러 메시지 표시
- [ ] 회원가입 API 호출 함수 (`frontend/src/api/auth.ts`)
- [ ] 회원가입 성공 시 로그인 페이지로 리다이렉트

---

## Feature 4: 로그인 API 개발

### BE
- [ ] 로그인 엔드포인트 구현 (`backend/app/routers/auth.py`)
  - POST /api/auth/login
  - 이메일/비밀번호 검증
  - JWT access token 발급
  - 토큰과 사용자 정보 반환
- [ ] 로그인 실패 처리
  - 401 Unauthorized (잘못된 인증 정보)
  - 에러 메시지 표준화

### FE
- [ ] 로그인 페이지 UI (`frontend/src/app/login/page.tsx`)
  - 이메일, 비밀번호 입력 필드
  - "로그인 유지" 체크박스 (optional)
  - 회원가입 페이지 링크
- [ ] 로그인 API 호출 함수 (`frontend/src/api/auth.ts`)
- [ ] 로그인 성공 시 토큰 저장 및 홈페이지로 리다이렉트
- [ ] 로그인 실패 시 에러 메시지 표시

---

## Feature 5: 인증 미들웨어 및 Protected Routes

### BE
- [ ] 인증 의존성 함수 구현 (`backend/app/dependencies/auth.py`)
  - get_current_user (토큰에서 사용자 정보 추출)
  - OAuth2PasswordBearer 설정
- [ ] Protected 엔드포인트 예제
  - GET /api/users/me (현재 로그인 사용자 정보 조회)
  - Depends(get_current_user) 적용
- [ ] 401/403 에러 핸들링

### FE
- [ ] 인증 상태 관리 Context (`frontend/src/contexts/AuthContext.tsx`)
  - useAuth 훅 제공
  - user, isAuthenticated, login, logout 상태/함수
- [ ] Protected Route 컴포넌트 (`frontend/src/components/ProtectedRoute.tsx`)
  - 인증되지 않은 사용자는 로그인 페이지로 리다이렉트
- [ ] API 요청 인터셉터 설정
  - 모든 요청에 Authorization 헤더 자동 추가

---

## Feature 6: 로그아웃 기능

### BE
- [ ] 로그아웃 엔드포인트 (optional, stateless JWT의 경우 FE에서만 처리 가능)
  - POST /api/auth/logout
  - 토큰 블랙리스트 관리 (optional, Redis 활용)

### FE
- [ ] 로그아웃 함수 구현
  - 토큰 삭제
  - 인증 상태 초기화
  - 로그인 페이지로 리다이렉트
- [ ] 로그아웃 버튼 UI 추가 (헤더/네비게이션)

---

## Feature 7: 사용자 프로필 조회 및 수정

### BE
- [ ] 프로필 조회 API
  - GET /api/users/me
  - 현재 로그인 사용자 정보 반환
- [ ] 프로필 수정 API
  - PUT /api/users/me
  - username, email 수정 가능
  - 비밀번호 변경은 별도 엔드포인트 고려

### FE
- [ ] 프로필 페이지 UI (`frontend/src/app/profile/page.tsx`)
  - 사용자 정보 표시
  - 정보 수정 폼
- [ ] 프로필 API 호출 함수
- [ ] 수정 성공 시 피드백 표시

---

## Feature 8: 비밀번호 재설정 (선택사항)

### BE
- [ ] 비밀번호 재설정 요청 API
  - POST /api/auth/forgot-password
  - 이메일로 재설정 링크 전송
- [ ] 비밀번호 재설정 확인 API
  - POST /api/auth/reset-password
  - 토큰 검증 후 새 비밀번호 설정

### FE
- [ ] 비밀번호 찾기 페이지
- [ ] 비밀번호 재설정 페이지
- [ ] 이메일 전송 완료 안내 UI

---

## Feature 9: 에러 처리 및 유효성 검증 강화

### BE
- [ ] 전역 예외 핸들러 추가
- [ ] 상세한 에러 메시지 정의
- [ ] 입력 검증 강화 (Pydantic validators)

### FE
- [ ] 전역 에러 핸들러
- [ ] Toast/Alert 컴포넌트로 에러 표시
- [ ] 폼 검증 라이브러리 통합 (react-hook-form, zod 등)

---

## Feature 10: 보안 강화 및 테스트

### BE
- [ ] CORS 설정 검토
- [ ] Rate limiting 추가 (로그인 시도 제한)
- [ ] 토큰 만료 시간 설정
- [ ] API 테스트 작성 (`backend/tests/test_auth.py`)
  - 회원가입 테스트
  - 로그인 테스트
  - 인증 미들웨어 테스트

### FE
- [ ] HTTPS 적용 (프로덕션)
- [ ] XSS 방지 처리
- [ ] 토큰 자동 갱신 로직 (refresh token)
- [ ] E2E 테스트 작성 (Playwright/Cypress)

---

## 개발 순서 권장

1. **Feature 1** → 데이터베이스 기반 구축
2. **Feature 2** → 인증 유틸리티 준비
3. **Feature 3, 4** → 회원가입/로그인 API (BE 우선)
4. **Feature 3, 4** → 회원가입/로그인 UI (FE)
5. **Feature 5** → 인증 미들웨어 및 상태 관리
6. **Feature 6** → 로그아웃
7. **Feature 7** → 프로필 관리
8. **Feature 8, 9, 10** → 고급 기능 및 보안 강화

---

## 참고사항

- JWT 토큰은 stateless 방식으로 구현 (서버에서 세션 저장 X)
- 비밀번호는 bcrypt로 해싱 (saltRounds: 12 권장)
- Access token 만료 시간: 15분~1시간
- Refresh token 구현 시 만료 시간: 7일~30일
- 환경변수는 `.env` 파일로 관리하며 `.gitignore`에 추가
