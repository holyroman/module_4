# Module 4 - JWT 인증 시스템

> FastAPI + Next.js 풀스택 웹 애플리케이션

JWT 기반 인증 시스템을 갖춘 풀스택 웹 애플리케이션입니다. 회원가입, 로그인, 프로필 관리 기능을 제공합니다.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2.0-000000?logo=next.js)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0.0-3178C6?logo=typescript)](https://www.typescriptlang.org/)

---

## 📋 목차

- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [시작하기](#-시작하기)
- [API 문서](#-api-문서)
- [화면](#-화면)
- [개발 문서](#-개발-문서)

---

## ✨ 주요 기능

### 인증 시스템
- 🔐 **회원가입**: 이메일, 사용자명, 비밀번호로 계정 생성
- 🔑 **로그인**: JWT 토큰 기반 인증
- 👤 **프로필 관리**: 사용자 정보 조회 및 수정
- 🚪 **로그아웃**: 토큰 삭제 및 세션 종료

### 보안
- ✅ bcrypt를 사용한 비밀번호 해싱
- ✅ JWT 토큰 기반 인증 (만료 시간: 30분)
- ✅ Protected Routes (인증 필요 페이지)
- ✅ CORS 설정
- ✅ 입력 검증 (Pydantic)

---

## 🛠 기술 스택

### 백엔드
- **프레임워크**: FastAPI 0.109.0
- **ORM**: SQLAlchemy 2.0.25
- **데이터베이스**: SQLite
- **인증**: JWT (python-jose), bcrypt (passlib)
- **검증**: Pydantic 2.5.3

### 프론트엔드
- **프레임워크**: Next.js 14 (App Router)
- **언어**: TypeScript 5.0
- **스타일링**: Tailwind CSS 3.4
- **상태관리**: React Context API

---

## 📁 프로젝트 구조

```
module_4/
├── backend/                    # FastAPI 백엔드
│   ├── app/
│   │   ├── dependencies/       # 인증 의존성
│   │   │   └── auth.py
│   │   ├── models/             # SQLAlchemy 모델
│   │   │   ├── example.py
│   │   │   └── user.py
│   │   ├── routers/            # API 엔드포인트
│   │   │   ├── auth.py         # 인증 API
│   │   │   ├── users.py        # 사용자 API
│   │   │   └── examples.py
│   │   ├── schemas/            # Pydantic 스키마
│   │   │   ├── example.py
│   │   │   └── user.py
│   │   ├── utils/              # 유틸리티
│   │   │   └── auth.py         # 비밀번호 해싱, JWT
│   │   ├── database.py         # DB 설정
│   │   └── main.py             # FastAPI 앱 진입점
│   ├── .env                    # 환경변수
│   └── requirements.txt        # Python 의존성
│
├── frontend/                   # Next.js 프론트엔드
│   ├── src/
│   │   ├── api/                # API 함수
│   │   │   └── auth.ts
│   │   ├── app/                # Next.js 페이지
│   │   │   ├── login/          # 로그인 페이지
│   │   │   ├── register/       # 회원가입 페이지
│   │   │   ├── profile/        # 프로필 페이지
│   │   │   ├── layout.tsx      # 루트 레이아웃
│   │   │   └── page.tsx        # 홈 페이지
│   │   ├── components/         # React 컴포넌트
│   │   │   ├── Navigation.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── contexts/           # Context API
│   │   │   └── AuthContext.tsx
│   │   ├── types/              # TypeScript 타입
│   │   │   └── user.ts
│   │   └── utils/              # 유틸리티
│   │       └── token.ts        # 토큰 관리
│   └── package.json            # Node 의존성
│
├── .claude/                    # Claude Code 설정
│   ├── docs/                   # 문서
│   │   ├── dev.md              # 개발 내역
│   │   ├── test.md             # 테스트 가이드
│   │   └── login_todo.md       # TODO 리스트
│   ├── agents/                 # 커스텀 에이전트
│   └── skills/                 # 커스텀 스킬
│
├── CLAUDE.md                   # 프로젝트 가이드
├── README.md                   # 이 파일
└── .gitignore
```

---

## 🚀 시작하기

### 사전 요구사항

- Python 3.12+
- Node.js 18+
- uv (Python 패키지 관리자)

### 1. 저장소 클론

```bash
git clone https://github.com/holyroman/module_4.git
cd module_4
```

### 2. 백엔드 설정

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 의존성 설치
uv pip install -r requirements.txt

# 환경변수 설정 (.env 파일 확인)
# SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# 데이터베이스 초기화 (개발 환경)
# app.db 파일이 자동 생성됨

# 서버 실행
uvicorn app.main:app --reload
```

**백엔드 실행 확인**: http://localhost:8000

### 3. 프론트엔드 설정

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

**프론트엔드 실행 확인**: http://localhost:3000

---

## 📚 API 문서

백엔드 실행 후 Swagger UI에서 API 문서를 확인할 수 있습니다.

**Swagger UI**: http://localhost:8000/docs

### 주요 엔드포인트

#### 인증 API (Public)

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| POST | `/api/auth/register` | 회원가입 |
| POST | `/api/auth/login` | 로그인 (JWT 토큰 발급) |
| POST | `/api/auth/logout` | 로그아웃 |

#### 사용자 API (Protected)

| 메서드 | 엔드포인트 | 설명 | 인증 |
|--------|-----------|------|------|
| GET | `/api/users/me` | 프로필 조회 | Bearer Token |
| PUT | `/api/users/me` | 프로필 수정 | Bearer Token |

### API 사용 예제

#### 회원가입
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "username",
    "password": "password123"
  }'
```

#### 로그인
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

#### 프로필 조회
```bash
curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer {access_token}"
```

---

## 🖼 화면

### 홈 페이지
- 로그인 상태 표시
- 로그인/회원가입 링크 (비로그인 시)
- 환영 메시지 및 프로필 링크 (로그인 시)

### 회원가입 페이지
- 이메일, 사용자명, 비밀번호 입력
- 클라이언트 검증 (비밀번호 8자 이상, 확인 일치)
- 회원가입 성공 시 자동 로그인

### 로그인 페이지
- 이메일, 비밀번호 입력
- 로그인 성공 시 홈으로 리다이렉트
- 에러 메시지 표시

### 프로필 페이지
- 사용자 정보 표시 (이메일, 사용자명, 가입일)
- 프로필 수정 폼
- Protected Route로 보호 (인증 필요)

### 네비게이션
- **비로그인**: 로그인, 회원가입 링크
- **로그인**: 사용자명, 프로필, 로그아웃 버튼

---

## 🧪 테스트

### 백엔드 API 테스트

Swagger UI를 사용하여 테스트:
```bash
# 백엔드 실행
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload

# 브라우저에서 접속
# http://localhost:8000/docs
```

### 프론트엔드 UI 테스트

1. 회원가입 플로우 테스트
2. 로그인 플로우 테스트
3. Protected Route 테스트
4. 프로필 수정 테스트
5. 로그아웃 테스트

**상세 테스트 가이드**: `.claude/docs/test.md`

---

## 📖 개발 문서

### 주요 문서

- **[CLAUDE.md](CLAUDE.md)** - 프로젝트 구조 및 개발 가이드
- **[.claude/docs/dev.md](.claude/docs/dev.md)** - 개발 내역 상세 문서
- **[.claude/docs/test.md](.claude/docs/test.md)** - 테스트 가이드 및 시나리오
- **[.claude/docs/login_todo.md](.claude/docs/login_todo.md)** - 기능별 TODO 리스트
- **[.claude/docs/Porting_guide.md](.claude/docs/Porting_guide.md)** - 설치 및 포팅 가이드

### 개발 워크플로우

1. **백엔드 개발** (be-agent)
   - API 엔드포인트 구현
   - 스키마 및 모델 정의
   - 비즈니스 로직 작성

2. **프론트엔드 개발** (fe-agent)
   - 페이지 및 컴포넌트 구현
   - API 연동
   - 스타일링

3. **테스트**
   - API 테스트 (Swagger UI)
   - UI 테스트 (수동)
   - E2E 테스트 (향후 구현)

---

## 🔒 보안 고려사항

### 백엔드
- ✅ bcrypt를 사용한 비밀번호 해싱 (saltRounds: 12)
- ✅ JWT 토큰 (SECRET_KEY 최소 32자, 만료 시간 30분)
- ✅ CORS 설정 (localhost:3000 허용)
- ✅ Pydantic으로 입력 검증
- ✅ 에러 메시지에서 구체적 정보 노출 방지

### 프론트엔드
- ✅ localStorage에 JWT 토큰 저장
- ✅ React의 기본 XSS 방지
- ✅ 클라이언트 검증 (UX 향상용)
- ⚠️ 프로덕션 환경에서는 HTTPS 필수

---

## 🛣️ 향후 개선 사항

### Feature 8: 비밀번호 재설정
- [ ] 이메일 전송 기능 (SMTP 설정)
- [ ] 재설정 토큰 생성 및 검증
- [ ] 비밀번호 재설정 페이지

### Feature 9: 에러 처리 강화
- [ ] 전역 예외 핸들러 (FastAPI)
- [ ] Toast/Alert 컴포넌트 (프론트엔드)
- [ ] react-hook-form, zod 통합

### Feature 10: 테스트
- [ ] pytest로 백엔드 API 테스트
- [ ] Playwright/Cypress로 E2E 테스트
- [ ] 테스트 커버리지 측정

### 추가 기능
- [ ] Refresh Token (Access token 자동 갱신)
- [ ] 소셜 로그인 (OAuth2: Google, GitHub)
- [ ] 이메일 인증 (회원가입 시 인증 링크)
- [ ] 비밀번호 변경 기능
- [ ] 사용자 역할 관리 (user, admin)
- [ ] Rate Limiting (로그인 시도 제한)

---

## 📝 라이선스

This project is licensed under the MIT License.

---

## 👥 기여자

- **Student** - 초기 개발
- **Claude Sonnet 4.5** - AI 개발 지원

---

## 🙋 FAQ

### Q: 백엔드 서버가 시작되지 않아요
**A**:
1. Python 가상환경이 활성화되었는지 확인
2. 의존성이 모두 설치되었는지 확인: `uv pip install -r requirements.txt`
3. .env 파일이 존재하고 SECRET_KEY가 설정되었는지 확인

### Q: 프론트엔드에서 API 호출이 실패해요
**A**:
1. 백엔드 서버가 http://localhost:8000 에서 실행 중인지 확인
2. next.config.js의 rewrites 설정 확인
3. 브라우저 개발자 도구의 Network 탭에서 에러 확인

### Q: 로그인 후 페이지 새로고침하면 로그아웃돼요
**A**:
1. localStorage에 토큰이 저장되는지 확인 (개발자 도구 → Application → Local Storage)
2. AuthContext의 초기화 로직 확인
3. 토큰 만료 시간 확인 (.env의 ACCESS_TOKEN_EXPIRE_MINUTES)

### Q: 데이터베이스를 초기화하고 싶어요
**A**:
```bash
cd backend
del app.db  # Windows
# rm app.db  # macOS/Linux
uvicorn app.main:app --reload  # 서버 시작 시 자동 생성
```

---

## 📞 문의

프로젝트 관련 문의사항이 있으시면 Issues를 통해 알려주세요.

**GitHub Repository**: https://github.com/holyroman/module_4
