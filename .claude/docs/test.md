# 테스트 가이드 - Login 인증 시스템

> 작성일: 2026-02-10
>
> 관련 문서: `.claude/docs/dev.md`, `.claude/plans/enchanted-crafting-toucan.md`

## 테스트 환경

- **백엔드**: http://localhost:8000
- **프론트엔드**: http://localhost:3000
- **API 문서**: http://localhost:8000/docs (Swagger UI)

---

## 사전 준비

### 1. 백엔드 실행

```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

**확인사항**:
- ✅ 서버가 http://localhost:8000 에서 실행 중
- ✅ Swagger UI 접속 가능 (http://localhost:8000/docs)
- ✅ Health check: GET /api/health → `{"status": "ok", ...}`

### 2. 프론트엔드 실행

```bash
cd frontend
npm run dev
```

**확인사항**:
- ✅ 서버가 http://localhost:3000 에서 실행 중
- ✅ 홈 페이지 접속 가능
- ✅ 네비게이션 바 표시

---

## 백엔드 API 테스트 (Swagger UI)

### Test Case 1: 회원가입 (POST /api/auth/register)

**접속**: http://localhost:8000/docs → POST /api/auth/register

**Test 1-1: 정상 회원가입**

요청 Body:
```json
{
  "email": "test@example.com",
  "username": "testuser",
  "password": "password123"
}
```

예상 결과:
- ✅ Status Code: 201 Created
- ✅ 응답:
  ```json
  {
    "id": 1,
    "email": "test@example.com",
    "username": "testuser",
    "is_active": true,
    "created_at": "2026-02-10T..."
  }
  ```

---

**Test 1-2: 이메일 중복**

요청 Body (동일한 이메일):
```json
{
  "email": "test@example.com",
  "username": "testuser2",
  "password": "password123"
}
```

예상 결과:
- ✅ Status Code: 400 Bad Request
- ✅ 응답:
  ```json
  {
    "detail": "이메일이 이미 등록되어 있습니다"
  }
  ```

---

**Test 1-3: 사용자명 중복**

요청 Body (동일한 username):
```json
{
  "email": "test2@example.com",
  "username": "testuser",
  "password": "password123"
}
```

예상 결과:
- ✅ Status Code: 400 Bad Request
- ✅ 응답:
  ```json
  {
    "detail": "사용자명이 이미 사용 중입니다"
  }
  ```

---

**Test 1-4: 유효성 검증 실패**

요청 Body (이메일 형식 오류):
```json
{
  "email": "invalid-email",
  "username": "testuser3",
  "password": "password123"
}
```

예상 결과:
- ✅ Status Code: 422 Unprocessable Entity
- ✅ Pydantic 유효성 검증 에러

---

### Test Case 2: 로그인 (POST /api/auth/login)

**Test 2-1: 정상 로그인**

요청 Body:
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

예상 결과:
- ✅ Status Code: 200 OK
- ✅ 응답:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```
- ✅ `access_token` 복사 (다음 테스트에 사용)

---

**Test 2-2: 잘못된 비밀번호**

요청 Body:
```json
{
  "email": "test@example.com",
  "password": "wrongpassword"
}
```

예상 결과:
- ✅ Status Code: 401 Unauthorized
- ✅ 응답:
  ```json
  {
    "detail": "이메일 또는 비밀번호가 올바르지 않습니다"
  }
  ```

---

**Test 2-3: 존재하지 않는 이메일**

요청 Body:
```json
{
  "email": "nonexistent@example.com",
  "password": "password123"
}
```

예상 결과:
- ✅ Status Code: 401 Unauthorized
- ✅ 응답:
  ```json
  {
    "detail": "이메일 또는 비밀번호가 올바르지 않습니다"
  }
  ```

---

### Test Case 3: 프로필 조회 (GET /api/users/me)

**사전 준비**:
1. Test 2-1에서 받은 `access_token` 복사
2. Swagger UI 우측 상단 "Authorize" 버튼 클릭
3. Value에 토큰 입력 (Bearer 접두사 자동 추가됨)
4. "Authorize" 클릭

**Test 3-1: 인증된 사용자 프로필 조회**

요청: GET /api/users/me (인증 헤더 포함)

예상 결과:
- ✅ Status Code: 200 OK
- ✅ 응답:
  ```json
  {
    "id": 1,
    "email": "test@example.com",
    "username": "testuser",
    "is_active": true,
    "created_at": "2026-02-10T..."
  }
  ```

---

**Test 3-2: 토큰 없이 요청**

요청: GET /api/users/me (인증 헤더 없음)

예상 결과:
- ✅ Status Code: 401 Unauthorized
- ✅ 응답:
  ```json
  {
    "detail": "Not authenticated"
  }
  ```

---

**Test 3-3: 잘못된 토큰**

요청: GET /api/users/me (잘못된 토큰)

Authorization: Bearer invalid_token_here

예상 결과:
- ✅ Status Code: 401 Unauthorized
- ✅ 응답:
  ```json
  {
    "detail": "유효하지 않은 토큰입니다"
  }
  ```

---

### Test Case 4: 프로필 수정 (PUT /api/users/me)

**사전 준비**: Test 3-1과 동일 (인증 필요)

**Test 4-1: 사용자명 수정**

요청 Body:
```json
{
  "username": "newusername"
}
```

예상 결과:
- ✅ Status Code: 200 OK
- ✅ 응답:
  ```json
  {
    "id": 1,
    "email": "test@example.com",
    "username": "newusername",
    "is_active": true,
    "created_at": "2026-02-10T..."
  }
  ```

---

**Test 4-2: 이메일 수정**

요청 Body:
```json
{
  "email": "newemail@example.com"
}
```

예상 결과:
- ✅ Status Code: 200 OK
- ✅ username은 변경 없음, email만 변경

---

**Test 4-3: 중복된 사용자명으로 수정 시도**

1. 먼저 다른 사용자 생성 (POST /api/auth/register):
   ```json
   {
     "email": "user2@example.com",
     "username": "user2",
     "password": "password123"
   }
   ```

2. 첫 번째 사용자로 로그인 후 user2로 변경 시도:
   ```json
   {
     "username": "user2"
   }
   ```

예상 결과:
- ✅ Status Code: 400 Bad Request
- ✅ 응답:
  ```json
  {
    "detail": "사용자명이 이미 사용 중입니다"
  }
  ```

---

### Test Case 5: 로그아웃 (POST /api/auth/logout)

**Test 5-1: 로그아웃**

요청: POST /api/auth/logout

예상 결과:
- ✅ Status Code: 200 OK
- ✅ 응답:
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

**참고**: Stateless JWT이므로 서버에서는 실제로 토큰을 무효화하지 않음. 클라이언트에서 토큰 삭제 필요.

---

## 프론트엔드 UI 테스트

### Test Case 6: 회원가입 플로우

**단계**:
1. http://localhost:3000 접속
2. 네비게이션에서 "회원가입" 클릭
3. 폼 입력:
   - 이메일: `frontend@test.com`
   - 사용자명: `frontenduser`
   - 비밀번호: `testpassword123`
   - 비밀번호 확인: `testpassword123`
4. "회원가입" 버튼 클릭

**예상 결과**:
- ✅ 성공 메시지 또는 로딩 표시
- ✅ 자동 로그인
- ✅ 홈 페이지로 리다이렉트
- ✅ 네비게이션에 "frontenduser" 표시
- ✅ "프로필", "로그아웃" 버튼 표시

---

**Test 6-2: 클라이언트 검증**

1. 비밀번호 8자 미만 입력
2. "회원가입" 버튼 클릭

예상 결과:
- ✅ "비밀번호는 최소 8자 이상이어야 합니다" 에러 메시지

3. 비밀번호와 비밀번호 확인 불일치
4. "회원가입" 버튼 클릭

예상 결과:
- ✅ "비밀번호가 일치하지 않습니다" 에러 메시지

---

**Test 6-3: 중복 이메일**

1. 이미 존재하는 이메일로 회원가입 시도
2. "회원가입" 버튼 클릭

예상 결과:
- ✅ 빨간색 배경 에러 메시지 표시
- ✅ "이메일이 이미 등록되어 있습니다"

---

### Test Case 7: 로그인 플로우

**단계**:
1. 로그아웃 상태에서 네비게이션 "로그인" 클릭
2. 폼 입력:
   - 이메일: `frontend@test.com`
   - 비밀번호: `testpassword123`
3. "로그인" 버튼 클릭

**예상 결과**:
- ✅ 로딩 표시
- ✅ 홈 페이지로 리다이렉트
- ✅ 네비게이션에 사용자명 표시
- ✅ "프로필", "로그아웃" 버튼 표시
- ✅ 환영 메시지: "안녕하세요, frontenduser님!"

---

**Test 7-2: 잘못된 비밀번호**

1. 로그인 페이지에서 잘못된 비밀번호 입력
2. "로그인" 버튼 클릭

예상 결과:
- ✅ 빨간색 배경 에러 메시지
- ✅ "이메일 또는 비밀번호가 올바르지 않습니다"
- ✅ 로그인 페이지 유지

---

### Test Case 8: Protected Route

**Test 8-1: 비인증 상태에서 프로필 접근**

1. 로그아웃 상태 확인
2. 브라우저 주소창에 직접 입력: http://localhost:3000/profile
3. Enter

예상 결과:
- ✅ 자동으로 http://localhost:3000/login 으로 리다이렉트
- ✅ 로딩 화면 잠깐 표시 가능

---

**Test 8-2: 인증 후 프로필 접근**

1. 로그인 완료
2. 네비게이션에서 "프로필" 클릭

예상 결과:
- ✅ 프로필 페이지 정상 표시
- ✅ 사용자 정보 표시:
  - 이메일: frontend@test.com
  - 사용자명: frontenduser
  - 가입일: 2026-02-10...

---

### Test Case 9: 프로필 수정

**단계**:
1. 로그인 후 프로필 페이지 접속
2. 사용자명 수정:
   - 기존: `frontenduser`
   - 신규: `updateduser`
3. "프로필 수정" 버튼 클릭

**예상 결과**:
- ✅ 초록색 배경 성공 메시지
- ✅ "프로필이 성공적으로 업데이트되었습니다"
- ✅ 네비게이션에 "updateduser" 표시
- ✅ 프로필 페이지에 변경된 정보 표시

---

**Test 9-2: 이메일 수정**

1. 이메일 수정:
   - 기존: `frontend@test.com`
   - 신규: `updated@test.com`
2. "프로필 수정" 버튼 클릭

예상 결과:
- ✅ 성공 메시지
- ✅ 프로필 페이지에 변경된 이메일 표시

---

### Test Case 10: 로그아웃

**단계**:
1. 로그인 상태에서 네비게이션 "로그아웃" 버튼 클릭

**예상 결과**:
- ✅ 로그인 페이지로 리다이렉트
- ✅ 네비게이션에 "로그인", "회원가입" 버튼 표시
- ✅ 사용자명 사라짐
- ✅ 홈 페이지 접속 시 "로그인하여 서비스를 이용하세요" 메시지

---

### Test Case 11: 토큰 영속성

**Test 11-1: 페이지 새로고침**

1. 로그인 완료
2. 브라우저에서 F5 (새로고침)

예상 결과:
- ✅ 로그인 상태 유지
- ✅ 네비게이션에 사용자명 계속 표시
- ✅ 프로필 페이지 접근 가능

---

**Test 11-2: 브라우저 재시작**

1. 로그인 완료
2. 브라우저 완전히 종료
3. 브라우저 재시작 후 http://localhost:3000 접속

예상 결과:
- ✅ 로그인 상태 유지 (localStorage에 토큰 저장)
- ✅ 사용자 정보 자동 로드

---

**Test 11-3: localStorage 확인**

1. 로그인 완료
2. 개발자 도구 (F12) → Application → Local Storage → http://localhost:3000
3. `access_token` 키 확인

예상 결과:
- ✅ `access_token` 키 존재
- ✅ 값: JWT 토큰 문자열 (eyJ...)

4. 로그아웃 후 다시 확인

예상 결과:
- ✅ `access_token` 키 삭제됨

---

### Test Case 12: 다중 사용자

**단계**:
1. 첫 번째 사용자로 로그인
2. 네비게이션에 첫 번째 사용자명 표시 확인
3. 로그아웃
4. 두 번째 사용자로 로그인
5. 네비게이션에 두 번째 사용자명 표시 확인

예상 결과:
- ✅ 각 사용자별로 올바른 정보 표시
- ✅ 토큰 교체 정상 작동

---

### Test Case 13: 네트워크 에러 처리

**Test 13-1: 백엔드 서버 중지**

1. 백엔드 서버 중지 (Ctrl+C)
2. 프론트엔드에서 로그인 시도

예상 결과:
- ✅ 에러 메시지 표시
- ✅ "Failed to fetch" 또는 네트워크 에러 메시지

---

**Test 13-2: 백엔드 재시작**

1. 백엔드 서버 재시작
2. 프론트엔드에서 로그인 재시도

예상 결과:
- ✅ 정상 로그인
- ✅ 에러에서 복구

---

## 성능 테스트 (선택사항)

### Test Case 14: 동시 로그인

**도구**: Apache Bench, K6, 또는 Postman

**테스트**:
```bash
# Apache Bench 예제
ab -n 100 -c 10 -p login.json -T application/json http://localhost:8000/api/auth/login
```

**예상 결과**:
- ✅ 모든 요청 성공
- ✅ 평균 응답 시간 < 500ms

---

### Test Case 15: 대용량 사용자 생성

**테스트**:
- 1000명의 사용자 생성
- 각 사용자로 로그인
- 프로필 조회

**예상 결과**:
- ✅ 데이터베이스 정상 작동
- ✅ 토큰 생성/검증 정상
- ✅ 메모리 누수 없음

---

## 보안 테스트 (선택사항)

### Test Case 16: SQL Injection

**테스트**:
```json
{
  "email": "test@example.com' OR '1'='1",
  "password": "password"
}
```

예상 결과:
- ✅ 로그인 실패
- ✅ SQLAlchemy가 자동으로 방어

---

### Test Case 17: XSS

**테스트**:
```json
{
  "email": "xss@test.com",
  "username": "<script>alert('XSS')</script>",
  "password": "password123"
}
```

예상 결과:
- ✅ 회원가입 성공
- ✅ 프론트엔드에서 스크립트 실행 안 됨 (React가 자동 이스케이프)

---

### Test Case 18: 토큰 만료

**테스트**:
1. .env에서 `ACCESS_TOKEN_EXPIRE_MINUTES=1` 설정
2. 로그인
3. 1분 대기
4. 프로필 조회

예상 결과:
- ✅ 401 Unauthorized
- ✅ "토큰이 만료되었습니다" 에러

---

## 테스트 체크리스트

### 백엔드 API
- [ ] Test 1: 회원가입 (정상, 중복, 유효성)
- [ ] Test 2: 로그인 (정상, 오류)
- [ ] Test 3: 프로필 조회 (인증, 비인증)
- [ ] Test 4: 프로필 수정 (정상, 중복)
- [ ] Test 5: 로그아웃

### 프론트엔드 UI
- [ ] Test 6: 회원가입 플로우
- [ ] Test 7: 로그인 플로우
- [ ] Test 8: Protected Route
- [ ] Test 9: 프로필 수정
- [ ] Test 10: 로그아웃
- [ ] Test 11: 토큰 영속성
- [ ] Test 12: 다중 사용자
- [ ] Test 13: 네트워크 에러

### 선택사항
- [ ] Test 14: 성능 테스트
- [ ] Test 15: 대용량 데이터
- [ ] Test 16-18: 보안 테스트

---

## 테스트 결과 기록

### 테스트 실행 정보
- **테스트 일자**: _______
- **테스트 담당자**: _______
- **백엔드 버전**: _______
- **프론트엔드 버전**: _______

### 통과/실패 현황

| Test Case | 상태 | 비고 |
|-----------|------|------|
| Test 1: 회원가입 | ⬜ | |
| Test 2: 로그인 | ⬜ | |
| Test 3: 프로필 조회 | ⬜ | |
| Test 4: 프로필 수정 | ⬜ | |
| Test 5: 로그아웃 | ⬜ | |
| Test 6: 회원가입 플로우 | ⬜ | |
| Test 7: 로그인 플로우 | ⬜ | |
| Test 8: Protected Route | ⬜ | |
| Test 9: 프로필 수정 | ⬜ | |
| Test 10: 로그아웃 | ⬜ | |
| Test 11: 토큰 영속성 | ⬜ | |
| Test 12: 다중 사용자 | ⬜ | |
| Test 13: 네트워크 에러 | ⬜ | |

---

## 발견된 이슈

### Issue 1
- **심각도**: ⬜ Critical / ⬜ High / ⬜ Medium / ⬜ Low
- **설명**:
- **재현 방법**:
- **예상 결과**:
- **실제 결과**:
- **스크린샷**:

### Issue 2
- **심각도**:
- **설명**:
- ...

---

## 자동화 테스트 (향후 구현)

### 백엔드 (pytest)
```python
# backend/tests/test_auth.py
def test_register():
    response = client.post("/api/auth/register", json={...})
    assert response.status_code == 201

def test_login():
    # ...
```

### 프론트엔드 (Playwright/Cypress)
```typescript
// tests/login.spec.ts
test('로그인 플로우', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.fill('input[type="email"]', 'test@example.com');
  await page.fill('input[type="password"]', 'password123');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('http://localhost:3000');
});
```

---

## 참고 문서

- **개발 문서**: `.claude/docs/dev.md`
- **계획 문서**: `.claude/plans/enchanted-crafting-toucan.md`
- **TODO**: `.claude/docs/login_todo.md`
