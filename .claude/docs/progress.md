# Progress Log

## [2026-02-05 12:00] 세션 작업 내역

### 변경된 파일

#### BE 스킬 정리
- `.claude/skills/BE-CRUD/SKILL.md`: 프로젝트 구조 반영, references 링크 수정
- `.claude/skills/BE-CRUD/references/*.md`: 4개 파일 간결화, 실제 구조에 맞게 수정
- `.claude/skills/BE-DEBUG/SKILL.md`: 신규 작성
- `.claude/skills/BE-DEBUG/references/*.md`: 4개 파일 신규 생성 (에러 유형별)
- `.claude/skills/BE-refactor/SKILL.md`: 오타 수정, 구조 정리
- `.claude/skills/BE-refactor/references/patterns.md`: 불필요 내용 제거
- `.claude/skills/BE-TEST/SKILL.md`: 간결화, references 분리
- `.claude/skills/BE-TEST/references/*.md`: 3개 파일 신규 생성

#### FE 스킬 정리
- `.claude/skills/FE-CRUD/SKILL.md`: 신규 작성
- `.claude/skills/FE-CRUD/references/*.md`: 4개 파일 신규 생성
- `.claude/skills/FE-page/SKILL.md`: 구조 정리, agent 필드 추가
- `.claude/skills/FE-page/references/*.md`: 3개 파일 신규 생성
- `.claude/skills/FE-api/SKILL.md`: 구조 정리, agent 필드 추가
- `.claude/skills/FE-api/references/*.md`: 3개 파일 신규 생성

#### Agent 파일 수정
- `.claude/agents/be-agent.md`: skills 목록 대소문자 일치, 빈 섹션 작성
- `.claude/agents/fe-agent.md`: skills 목록 수정, 존재하지 않는 스킬 제거

### 작업 요약
- BE 스킬 4개 (CRUD, DEBUG, refactor, TEST) 구조 통일 및 references 분리
- FE 스킬 3개 (CRUD, page, api) 구조 통일 및 references 분리
- be-agent, fe-agent와 스킬 매칭 검증 및 수정
- 모든 스킬 파일 간결화 및 실제 프로젝트 구조 반영

---

## [2026-02-05 12:30] CLAUDE.md 최신화

### 변경된 파일
- `CLAUDE.md`: 에이전트 테이블 최신화, db-agent 제거

### 작업 요약
- db-agent 관련 내용 제거
- be-agent skills: BE-CRUD, BE-refactor, BE-TEST, BE-DEBUG 반영
- fe-agent skills: FE-CRUD, FE-page, FE-api 반영
- 작업 순서 3단계 → 2단계 (BE → FE)

---

## [2026-02-10] JWT 인증 시스템 구현

### 변경된 파일

#### Phase 1: 백엔드 인증 시스템 (be-agent)
- `backend/requirements.txt`: passlib, python-jose, python-multipart 추가
- `backend/.env`: SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES 설정
- `backend/app/models/user.py`: User 모델 생성 (신규)
- `backend/app/models/__init__.py`: User 모델 import
- `backend/app/schemas/user.py`: 6개 스키마 생성 (신규)
- `backend/app/schemas/__init__.py`: User 스키마 import
- `backend/app/utils/auth.py`: 인증 유틸리티 (신규)
- `backend/app/dependencies/auth.py`: 인증 의존성 (신규)
- `backend/app/routers/auth.py`: 인증 API (신규)
- `backend/app/routers/users.py`: 사용자 API (신규)
- `backend/app/main.py`: auth, users 라우터 등록

#### Phase 2: 프론트엔드 인증 UI (fe-agent)
- `frontend/src/types/user.ts`: User 타입 정의 (신규)
- `frontend/src/utils/token.ts`: 토큰 관리 (신규)
- `frontend/src/api/auth.ts`: API 함수 (신규)
- `frontend/src/contexts/AuthContext.tsx`: 전역 상태 관리 (신규)
- `frontend/src/components/ProtectedRoute.tsx`: Protected Route (신규)
- `frontend/src/components/Navigation.tsx`: 네비게이션 (신규)
- `frontend/src/app/login/page.tsx`: 로그인 페이지 (신규)
- `frontend/src/app/register/page.tsx`: 회원가입 페이지 (신규)
- `frontend/src/app/profile/page.tsx`: 프로필 페이지 (신규)
- `frontend/src/app/layout.tsx`: AuthProvider, Navigation 추가
- `frontend/src/app/page.tsx`: 인증 상태 표시 추가

#### 문서
- `.claude/docs/dev.md`: 개발 내역 상세 문서 (신규)
- `.claude/docs/test.md`: 테스트 가이드 (신규)
- `.claude/docs/login_todo.md`: 기능별 TODO (신규)
- `README.md`: 프로젝트 README (신규)
- `test_api.py`: API 테스트 스크립트 (신규)
- `.gitignore`: 루트 gitignore (신규)

### 작업 요약
- JWT 기반 인증 시스템 완전 구현
- bcrypt 비밀번호 해싱
- 회원가입, 로그인, 프로필 관리 API
- 인증 Context, Protected Route
- 로그인/회원가입/프로필 페이지
- Git 레포지토리 생성 및 푸시 (https://github.com/holyroman/module_4)

---

## [2026-02-10] 인증 시스템 보안 설정 변경

### 변경된 파일

#### 비밀번호 해싱 알고리즘 변경 (bcrypt → SHA-256)
- `backend/app/utils/auth.py`: SHA-256 + salt 방식으로 변경
  - `hash_password()`: 랜덤 salt(16 bytes) + SHA-256 해싱
  - `verify_password()`: salt 분리 후 검증
  - 보안 경고 주석 추가

#### SECRET_KEY, ALGORITHM DB 관리
- `backend/app/models/config.py`: Config 모델 생성 (신규)
- `backend/app/models/__init__.py`: Config 모델 import
- `backend/app/schemas/config.py`: ConfigResponse 스키마 (신규)
- `backend/app/schemas/__init__.py`: ConfigResponse import
- `backend/app/utils/init_config.py`: 초기 설정값 생성 함수 (신규)
- `backend/app/utils/auth.py`: DB에서 SECRET_KEY, ALGORITHM 로드
- `backend/app/routers/auth.py`: create_access_token에 db 파라미터 추가
- `backend/app/dependencies/auth.py`: decode_access_token에 db 파라미터 추가
- `backend/app/main.py`: 앱 시작 시 init_config() 호출

### 작업 요약
- 비밀번호 해싱: bcrypt → SHA-256 (salt 포함)
- 설정 관리: .env → DB (Config 테이블)
- SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES DB 저장
- 앱 시작 시 자동으로 초기 설정값 생성

### 주의사항
- ⚠️ SHA-256은 비밀번호 해싱에 권장되지 않음 (프로덕션에서는 bcrypt 사용 권장)
- ⚠️ SECRET_KEY를 DB에 저장하는 것은 보안 위험 (환경변수 권장)
- 기존 DB 초기화 필요 (app.db 삭제 후 재생성)

---

## [2026-02-10] SECRET_KEY 메모리 기반 관리로 변경

### 변경된 파일

#### SECRET_KEY 관리 방식 변경 (DB → 메모리)
- `backend/app/main.py`: 서버 시작 시 SECRET_KEY 메모리 생성
  - `secrets.token_urlsafe(48)` 사용
  - `set_secret_key()` 호출
  - DB 의존성 제거 (SessionLocal, init_config 제거)
- `backend/app/utils/auth.py`: 메모리 기반 SECRET_KEY 관리
  - 전역 변수 `_SECRET_KEY` 추가
  - `set_secret_key()`, `get_secret_key()` 함수 추가
  - 상수 정의: `ALGORITHM = "HS256"`, `ACCESS_TOKEN_EXPIRE_MINUTES = 30`
  - `create_access_token()`, `decode_access_token()`에서 `db` 파라미터 제거
  - `get_config_value()` 함수 삭제
- `backend/app/routers/auth.py`: `create_access_token(data={"sub": user.email})` (db 제거)
- `backend/app/dependencies/auth.py`: `decode_access_token(token)` (db 제거)
- `backend/app/models/__init__.py`: Config import 제거
- `backend/app/schemas/__init__.py`: ConfigResponse import 제거

#### 삭제된 파일
- `backend/app/models/config.py`: Config 모델 삭제
- `backend/app/schemas/config.py`: ConfigResponse 스키마 삭제
- `backend/app/utils/init_config.py`: DB 초기화 유틸리티 삭제

#### 문서
- `.claude/docs/dev.md`: SECRET_KEY 메모리 관리 섹션 추가
- `.claude/docs/test.md`: Test Case 22~27 추가 (6개 테스트)

### 작업 요약
- SECRET_KEY를 DB에서 메모리로 이동
- JWT 생성/검증 시 DB 조회 제거 → 성능 향상
- 코드 단순화: 3개 파일 삭제, 약 100줄 감소
- 개발 편의성: 서버 시작 시 자동 생성

### 주의사항
- ⚠️ 서버 재시작 시 SECRET_KEY 변경으로 기존 토큰 무효화
- 프로덕션 환경에서는 환경 변수로 고정된 SECRET_KEY 사용 권장

---

## [2026-02-10] 환경 변수 기반 SECRET_KEY 지원 추가 (프로덕션 대비)

### 변경된 파일

#### 환경 변수 지원 추가
- `backend/app/main.py`: 환경 변수 우선 로드
  - `python-dotenv`의 `load_dotenv()` 추가
  - `os.getenv("SECRET_KEY")` 우선 조회
  - 없으면 자동 생성 (개발 환경)
  - 적절한 로그 메시지 출력 ([INFO]/[WARNING])

#### 새로 생성된 파일
- `backend/.env`: 프로덕션용 SECRET_KEY 설정 파일
  - SECRET_KEY: 86자 랜덤 문자열
  - ALGORITHM: HS256
  - ACCESS_TOKEN_EXPIRE_MINUTES: 30
- `backend/.env.example`: 개발자용 템플릿 파일
  - 플레이스홀더 값으로 실제 SECRET_KEY 노출 방지

#### 문서
- `.claude/docs/dev.md`: 환경 변수 지원 구현 완료 표시, 변경 이력 추가
- `.claude/docs/test.md`: Test Case 28 추가 (5개 세부 테스트), Issue 1 해결 표시

### 작업 요약
- 환경 변수 기반 SECRET_KEY 관리 추가
- .env 파일 우선 로드, 없으면 자동 생성
- 프로덕션 환경 지원 완료
- 서버 재시작해도 JWT 토큰 유지 (고정된 SECRET_KEY 사용 시)

### 기대 효과
- ✅ 개발 환경: .env 없이도 자동 생성으로 편리
- ✅ 프로덕션 환경: .env에 고정 SECRET_KEY 설정으로 토큰 영속성 보장
- ✅ 보안: .env 파일이 .gitignore에 포함되어 git에 커밋되지 않음

---

## [2026-02-10] 에러 처리 강화 및 테스트 자동화

### 변경된 파일

#### 백엔드: 전역 예외 핸들러 구현
- `backend/app/schemas/error.py`: 에러 응답 스키마 (신규)
  - `ErrorDetail`: 에러 상세 정보
  - `ErrorResponse`: 통일된 에러 응답
- `backend/app/utils/exceptions.py`: 커스텀 예외 클래스 (신규)
  - `BadRequestException` (400)
  - `NotFoundException` (404)
  - `UnauthorizedException` (401)
  - `ForbiddenException` (403)
- `backend/app/main.py`: 전역 예외 핸들러 3개 추가
  - HTTP 예외 핸들러
  - Pydantic 검증 에러 핸들러
  - 일반 예외 핸들러
- `backend/app/routers/auth.py`: 커스텀 예외로 변경
- `backend/app/routers/users.py`: 커스텀 예외로 변경
- `backend/app/dependencies/auth.py`: 커스텀 예외로 변경
- `backend/app/schemas/__init__.py`: ErrorResponse export
- `backend/test_error_handlers.py`: 예외 핸들러 테스트 스크립트 (신규)
- `backend/app/utils/ERROR_HANDLING.md`: 사용 가이드 (신규)

#### 프론트엔드: Toast 알림 시스템 구현
- `frontend/src/types/toast.ts`: Toast 타입 정의 (신규)
- `frontend/src/contexts/ToastContext.tsx`: Toast 상태 관리 (신규)
- `frontend/src/components/Toast.tsx`: Toast 컴포넌트 (신규)
- `frontend/src/components/ToastContainer.tsx`: Toast 컨테이너 (신규)
- `frontend/src/utils/api-error.ts`: API 에러 처리 유틸리티 (신규)
- `frontend/tailwind.config.ts`: slide-in 애니메이션 추가
- `frontend/src/app/layout.tsx`: ToastProvider 추가
- `frontend/src/app/login/page.tsx`: Toast 알림 통합
- `frontend/src/app/register/page.tsx`: Toast 알림 통합
- `frontend/src/app/profile/page.tsx`: Toast 알림 통합
- `frontend/src/api/auth.ts`: 에러 처리 개선
- `frontend/src/contexts/AuthContext.tsx`: getErrorMessage import

#### 백엔드: pytest 테스트 자동화
- `backend/pytest.ini`: pytest 설정 (신규)
- `backend/tests/__init__.py`: 테스트 패키지 (신규)
- `backend/tests/conftest.py`: 공통 픽스처 (신규)
- `backend/tests/test_auth.py`: 인증 API 테스트 11개 (신규)
- `backend/tests/test_users.py`: 사용자 API 테스트 13개 (신규)
- `backend/tests/test_error_handlers.py`: 예외 핸들러 테스트 14개 (신규)
- `backend/tests/test_health.py`: Health Check 테스트 6개 (신규)
- `backend/tests/README.md`: 테스트 가이드 (신규)
- `backend/requirements.txt`: pytest, pytest-cov 추가
- `backend/.gitignore`: 테스트 관련 파일 제외

### 작업 요약

#### Feature 9: 에러 처리 강화 ✅
- 백엔드: 전역 예외 핸들러로 통일된 에러 응답 제공
- 프론트엔드: Toast 알림으로 사용자 친화적 에러 표시
- 타입별 Toast: 성공(초록), 에러(빨강), 정보(파랑), 경고(노랑)
- 자동 제거 (3초), 애니메이션 효과

#### Feature 10: 테스트 자동화 ✅
- pytest로 42개 테스트 케이스 작성
- 코드 커버리지 87% 달성
- 테스트용 인메모리 DB 사용
- HTML 커버리지 리포트 생성

### 테스트 결과
```
====================== 42 passed in 2.71s ======================
Coverage: 87%
```

### 기대 효과
- ✅ 일관된 에러 처리로 디버깅 용이
- ✅ 사용자 경험 개선 (Toast 알림)
- ✅ 코드 품질 보장 (자동화 테스트)
- ✅ 회귀 방지 (CI/CD 준비)

---

## 다음 스텝
- [x] JWT 인증 시스템 구현
- [x] DB 기반 설정 관리
- [x] SECRET_KEY 메모리 기반 관리로 변경
- [x] 환경 변수 기반 SECRET_KEY 지원 추가 (프로덕션 대비)
- [x] **에러 처리 강화 (Feature 9)**
- [x] **테스트 자동화 (Feature 10)**
- [ ] 비밀번호 재설정 기능 (Feature 8)
- [ ] Refresh Token 구현
- [ ] 소셜 로그인 (OAuth2)
- [ ] CI/CD 파이프라인 구축
- [ ] 프론트엔드 테스트 (Jest, Playwright)
