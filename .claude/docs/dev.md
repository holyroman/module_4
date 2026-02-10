# 개발 내역 - Login 인증 시스템

> 작성일: 2026-02-10
>
> 기반 문서: `.claude/docs/login_todo.md`, `.claude/plans/enchanted-crafting-toucan.md`

## 개요

JWT 기반 인증 시스템을 구현하여 사용자 회원가입, 로그인, 프로필 관리 기능을 추가했습니다.

- **백엔드**: FastAPI + SQLAlchemy + JWT (bcrypt, python-jose)
- **프론트엔드**: Next.js 14 + TypeScript + Tailwind CSS + Context API

---

## Phase 1: 백엔드 구현

### 1.1 의존성 추가

**파일**: `backend/requirements.txt`

추가된 패키지:
```txt
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
```

설치 명령어:
```bash
cd backend
.venv\Scripts\activate
uv pip install passlib[bcrypt]==1.7.4 python-jose[cryptography]==3.3.0 python-multipart==0.0.6
```

---

### 1.2 환경변수 설정

**파일**: `backend/.env` (신규)

```env
SECRET_KEY=your-secret-key-here-change-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**주의**: SECRET_KEY는 프로덕션 환경에서 반드시 강력한 랜덤 문자열로 변경 필요

---

### 1.3 데이터베이스 모델

#### User 모델
**파일**: `backend/app/models/user.py`

```python
class User(Base):
    __tablename__ = "users"

    id: Integer (Primary Key)
    email: String(255) (Unique, Index)
    username: String(100) (Unique)
    hashed_password: String(255)
    is_active: Boolean (default=True)
    created_at: DateTime (자동 생성)
    updated_at: DateTime (자동 업데이트)
```

**패턴**: `models/example.py` 참고

---

### 1.4 Pydantic 스키마

**파일**: `backend/app/schemas/user.py`

구현된 스키마:
- `UserCreate`: 회원가입 요청 (email, username, password)
- `UserLogin`: 로그인 요청 (email, password)
- `UserResponse`: 사용자 정보 응답 (id, email, username, is_active, created_at)
- `Token`: JWT 토큰 응답 (access_token, token_type)
- `TokenData`: 토큰 페이로드 (email)
- `UserUpdate`: 프로필 수정 요청 (username, email - optional)

**패턴**: `schemas/example.py` 참고

---

### 1.5 인증 유틸리티

**파일**: `backend/app/utils/auth.py`

구현된 함수:
1. **`hash_password(password: str) -> str`**
   - bcrypt를 사용한 비밀번호 해싱

2. **`verify_password(plain_password: str, hashed_password: str) -> bool`**
   - 비밀번호 검증

3. **`create_access_token(data: dict, expires_delta: timedelta | None = None) -> str`**
   - JWT 토큰 생성
   - .env에서 SECRET_KEY, ALGORITHM 로드
   - 기본 만료 시간: 30분

4. **`decode_access_token(token: str) -> TokenData`**
   - JWT 디코딩 및 검증
   - 만료/유효성 체크

**라이브러리**:
- `passlib.context.CryptContext`
- `jose.jwt`, `jose.JWTError`

---

### 1.6 인증 의존성

**파일**: `backend/app/dependencies/auth.py`

구현된 의존성:
1. **`oauth2_scheme`**: OAuth2PasswordBearer

2. **`get_current_user(token, db) -> User`**
   - 토큰에서 사용자 정보 추출
   - DB 조회 후 User 객체 반환
   - 에러: 401 Unauthorized

3. **`get_current_active_user(current_user) -> User`**
   - is_active 체크
   - 에러: 403 Forbidden

---

### 1.7 API 엔드포인트

#### 인증 라우터
**파일**: `backend/app/routers/auth.py`

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|-----------|------|----------|
| POST | `/api/auth/register` | 회원가입 | ❌ |
| POST | `/api/auth/login` | 로그인 | ❌ |
| POST | `/api/auth/logout` | 로그아웃 (stateless) | ❌ |

**회원가입 로직**:
- 이메일 중복 체크 → 400 Bad Request
- 사용자명 중복 체크 → 400 Bad Request
- 비밀번호 해싱
- User 생성 및 저장
- UserResponse 반환 (201 Created)

**로그인 로직**:
- 이메일로 사용자 조회 → 401 Unauthorized
- 비밀번호 검증 → 401 Unauthorized
- is_active 체크 → 403 Forbidden
- JWT 생성 (subject=email)
- Token 반환

---

#### 사용자 라우터
**파일**: `backend/app/routers/users.py`

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|-----------|------|----------|
| GET | `/api/users/me` | 프로필 조회 | ✅ |
| PUT | `/api/users/me` | 프로필 수정 | ✅ |

**프로필 수정 로직**:
- username 변경 시 중복 체크 → 400 Bad Request
- email 변경 시 중복 체크 → 400 Bad Request
- 필드 업데이트
- UserResponse 반환

---

### 1.8 라우터 등록

**파일**: `backend/app/main.py`

```python
from app.routers import examples, auth, users

app.include_router(examples.router)
app.include_router(auth.router)
app.include_router(users.router)
```

---

### 1.9 데이터베이스 마이그레이션

**초기화 명령어**:
```bash
cd backend
del app.db  # 기존 DB 삭제 (개발 환경)
uvicorn app.main:app --reload  # 서버 시작 시 자동 생성
```

User 모델이 `models/__init__.py`에 등록되어 있으므로 `Base.metadata.create_all(bind=engine)`에 의해 자동으로 users 테이블이 생성됩니다.

---

## Phase 2: 프론트엔드 구현

### 2.1 타입 정의

**파일**: `frontend/src/types/user.ts`

```typescript
interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
}

interface UserCreate { email, username, password }
interface UserLogin { email, password }
interface Token { access_token, token_type }
interface UserUpdate { username?, email? }
```

---

### 2.2 토큰 관리

**파일**: `frontend/src/utils/token.ts`

localStorage를 사용한 JWT 토큰 관리:
- `setToken(token: string): void`
- `getToken(): string | null`
- `removeToken(): void`

---

### 2.3 API 함수

**파일**: `frontend/src/api/auth.ts`

구현된 API 함수:
- `register(data: UserCreate): Promise<User>` → POST /api/auth/register
- `login(data: UserLogin): Promise<Token>` → POST /api/auth/login
- `getCurrentUser(token: string): Promise<User>` → GET /api/users/me
- `updateProfile(token: string, data: UserUpdate): Promise<User>` → PUT /api/users/me
- `logout(): void` → 토큰 삭제

**패턴**: `app/page.tsx`의 fetch 패턴 재사용

---

### 2.4 전역 인증 상태 관리

**파일**: `frontend/src/contexts/AuthContext.tsx`

**AuthContext**:
```typescript
{
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (data: UserCreate) => Promise<void>;
  updateUser: (data: UserUpdate) => Promise<void>;
}
```

**AuthProvider**:
- 컴포넌트 마운트 시 토큰 확인 → 사용자 정보 자동 로드
- login: API 호출 → 토큰 저장 → 사용자 정보 조회
- logout: 토큰 삭제 → 상태 초기화
- register: API 호출 → 자동 로그인

**useAuth 훅**: Context 값 반환

---

### 2.5 컴포넌트

#### ProtectedRoute
**파일**: `frontend/src/components/ProtectedRoute.tsx`

로직:
- loading 중: 로딩 표시
- 비인증: 로그인 페이지로 리다이렉트
- 인증: children 렌더링

사용 예:
```tsx
<ProtectedRoute>
  <ProfilePage />
</ProtectedRoute>
```

---

#### Navigation
**파일**: `frontend/src/components/Navigation.tsx`

기능:
- **비로그인 상태**: 로그인, 회원가입 링크 표시
- **로그인 상태**: 사용자명, 프로필, 로그아웃 버튼 표시
- Tailwind CSS로 스타일링

---

### 2.6 페이지

#### 로그인 페이지
**파일**: `frontend/src/app/login/page.tsx`

UI:
- 이메일 입력 (type="email", required)
- 비밀번호 입력 (type="password", required)
- 로그인 버튼
- 회원가입 링크
- 에러 메시지 표시 영역

로직:
- useAuth 훅으로 login 함수 가져오기
- 제출 시 login() 호출
- 성공 시 "/" 리다이렉트
- 실패 시 에러 메시지 표시

---

#### 회원가입 페이지
**파일**: `frontend/src/app/register/page.tsx`

UI:
- 이메일 입력
- 사용자명 입력
- 비밀번호 입력
- 비밀번호 확인 입력
- 회원가입 버튼
- 로그인 링크

클라이언트 검증:
- 비밀번호 최소 8자
- 비밀번호 확인 일치

로직:
- useAuth 훅으로 register 함수 가져오기
- 제출 시 register() 호출
- 성공 시 자동 로그인 및 홈으로 리다이렉트

---

#### 프로필 페이지
**파일**: `frontend/src/app/profile/page.tsx`

UI:
- 사용자 정보 표시 (이메일, 사용자명, 가입일)
- 수정 폼 (username, email)
- 수정 버튼
- 성공 메시지 표시

보호:
- ProtectedRoute로 감싸기
- 비인증 사용자는 로그인 페이지로 리다이렉트

---

### 2.7 Layout 업데이트

**파일**: `frontend/src/app/layout.tsx`

변경사항:
```tsx
import { AuthProvider } from '@/contexts/AuthContext';
import Navigation from '@/components/Navigation';

export default function RootLayout({ children }) {
  return (
    <html lang="ko">
      <body>
        <AuthProvider>
          <Navigation />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
```

---

### 2.8 홈 페이지 업데이트

**파일**: `frontend/src/app/page.tsx`

변경사항:
- useAuth 훅으로 user, isAuthenticated 가져오기
- 로그인 상태 표시
- 로그인 사용자에게 환영 메시지
- 프로필 페이지 링크

---

## 프로젝트 구조

### 백엔드
```
backend/app/
├── dependencies/
│   ├── __init__.py
│   └── auth.py (인증 의존성)
├── models/
│   ├── __init__.py
│   ├── example.py
│   └── user.py (User 모델)
├── routers/
│   ├── __init__.py
│   ├── examples.py
│   ├── auth.py (인증 API)
│   └── users.py (사용자 API)
├── schemas/
│   ├── __init__.py
│   ├── example.py
│   └── user.py (User 스키마)
├── utils/
│   ├── __init__.py
│   └── auth.py (인증 유틸리티)
├── database.py
└── main.py
```

### 프론트엔드
```
frontend/src/
├── api/
│   └── auth.ts (API 함수)
├── app/
│   ├── login/
│   │   └── page.tsx
│   ├── register/
│   │   └── page.tsx
│   ├── profile/
│   │   └── page.tsx
│   ├── layout.tsx (AuthProvider, Navigation)
│   └── page.tsx (홈 페이지)
├── components/
│   ├── Navigation.tsx
│   └── ProtectedRoute.tsx
├── contexts/
│   └── AuthContext.tsx (전역 상태 관리)
├── types/
│   └── user.ts (타입 정의)
└── utils/
    └── token.ts (토큰 관리)
```

---

## API 엔드포인트 요약

### 인증 API (Public)

| 메서드 | 엔드포인트 | 요청 Body | 응답 | 설명 |
|--------|-----------|----------|------|------|
| POST | `/api/auth/register` | UserCreate | UserResponse (201) | 회원가입 |
| POST | `/api/auth/login` | UserLogin | Token | 로그인 |
| POST | `/api/auth/logout` | - | message | 로그아웃 |

### 사용자 API (Protected)

| 메서드 | 엔드포인트 | 요청 Body | 응답 | 설명 |
|--------|-----------|----------|------|------|
| GET | `/api/users/me` | - | UserResponse | 프로필 조회 |
| PUT | `/api/users/me` | UserUpdate | UserResponse | 프로필 수정 |

**인증 방식**: Bearer Token (Authorization: Bearer {access_token})

---

## 실행 방법

### 백엔드 실행

```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

- **주소**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

### 프론트엔드 실행

```bash
cd frontend
npm run dev
```

- **주소**: http://localhost:3000

---

## 테스트 시나리오

### 1. 회원가입 플로우
1. http://localhost:3000/register 접속
2. 이메일, 사용자명, 비밀번호 입력
3. "회원가입" 버튼 클릭
4. ✅ 성공 → 자동 로그인 → 홈으로 리다이렉트
5. ❌ 실패 → 에러 메시지 표시 (이메일/사용자명 중복)

### 2. 로그인 플로우
1. http://localhost:3000/login 접속
2. 이메일, 비밀번호 입력
3. "로그인" 버튼 클릭
4. ✅ 성공 → 홈으로 리다이렉트, 네비게이션에 사용자명 표시
5. ❌ 실패 → 에러 메시지 표시

### 3. 프로필 관리
1. 네비게이션에서 "프로필" 클릭
2. 사용자 정보 확인
3. 사용자명 수정
4. "프로필 수정" 버튼 클릭
5. ✅ 성공 메시지 표시
6. 네비게이션에 변경된 사용자명 표시

### 4. 로그아웃
1. 네비게이션에서 "로그아웃" 클릭
2. 로그인 페이지로 리다이렉트
3. 네비게이션 업데이트 (로그인/회원가입 표시)

### 5. Protected Route
1. 로그아웃 상태에서 http://localhost:3000/profile 직접 접속
2. 자동으로 로그인 페이지로 리다이렉트

### 6. 토큰 영속성
1. 로그인 후 페이지 새로고침
2. 로그인 상태 유지 확인 (localStorage에 토큰 저장)

---

## 보안 고려사항

### 백엔드
1. **비밀번호 해싱**: bcrypt 사용 (saltRounds: 12)
2. **JWT 토큰**:
   - SECRET_KEY 최소 32자
   - 만료 시간 30분
   - 알고리즘: HS256
3. **CORS**: localhost:3000 허용 (프로덕션에서 특정 도메인만 허용)
4. **입력 검증**: Pydantic으로 타입 및 형식 검증
5. **에러 메시지**: "이메일 또는 비밀번호가 올바르지 않습니다" (구체적 정보 노출 방지)

### 프론트엔드
1. **토큰 저장**: localStorage 사용 (XSS 취약 가능성 인지)
2. **XSS 방지**: React의 기본 이스케이프 처리 활용
3. **HTTPS**: 프로덕션에서 반드시 사용 (토큰 평문 전송)
4. **클라이언트 검증**: UX 향상용, 서버 검증이 최종 보안 라인

---

## 향후 개선 사항

### Feature 8: 비밀번호 재설정 (선택사항)
- 이메일 전송 기능 (SMTP 설정)
- 재설정 토큰 생성 및 검증
- 비밀번호 재설정 페이지

### Feature 9: 에러 처리 강화
- 전역 예외 핸들러 (FastAPI)
- Toast/Alert 컴포넌트 (프론트엔드)
- react-hook-form, zod 통합

### Feature 10: 테스트
- pytest로 백엔드 API 테스트
- Playwright/Cypress로 E2E 테스트
- 테스트 커버리지 측정

### 추가 개선
- **Refresh Token**: Access token 자동 갱신
- **소셜 로그인**: OAuth2 (Google, GitHub 등)
- **이메일 인증**: 회원가입 시 이메일 인증 링크
- **비밀번호 변경**: 별도 엔드포인트
- **사용자 역할 관리**: role 필드 추가 (user, admin)
- **Rate Limiting**: 로그인 시도 제한

---

## 참고 문서

- **계획 문서**: `.claude/plans/enchanted-crafting-toucan.md`
- **TODO**: `.claude/docs/login_todo.md`
- **프로젝트 가이드**: `CLAUDE.md`
- **포팅 가이드**: `.claude/docs/Porting_guide.md`

---

## 변경 이력

| 날짜 | 작업 | 담당 |
|------|------|------|
| 2026-02-10 | Phase 1: 백엔드 인증 시스템 구현 | be-agent |
| 2026-02-10 | Phase 2: 프론트엔드 인증 UI 구현 | fe-agent |
