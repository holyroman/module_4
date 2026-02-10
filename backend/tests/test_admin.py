"""Admin 시스템 테스트"""
import pytest
from datetime import datetime, timedelta
from app.models.admin import Admin
from app.models.admin_session import AdminSession
from app.utils.auth import hash_password


# ============================================
# Fixtures
# ============================================

@pytest.fixture
def super_admin_data():
    """슈퍼 관리자 테스트 데이터"""
    return {
        "email": "super@admin.com",
        "username": "superadmin",
        "password": "SuperSecret123!",
        "role": "super_admin"
    }


@pytest.fixture
def admin_data():
    """일반 관리자 테스트 데이터"""
    return {
        "email": "admin@example.com",
        "username": "normaladmin",
        "password": "AdminPass123!",
        "role": "admin"
    }


@pytest.fixture
def create_super_admin(db_session, super_admin_data):
    """슈퍼 관리자 생성"""
    admin = Admin(
        email=super_admin_data["email"],
        username=super_admin_data["username"],
        hashed_password=hash_password(super_admin_data["password"]),
        role="super_admin",
        is_active=True
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture
def create_normal_admin(db_session, admin_data):
    """일반 관리자 생성"""
    admin = Admin(
        email=admin_data["email"],
        username=admin_data["username"],
        hashed_password=hash_password(admin_data["password"]),
        role="admin",
        is_active=True
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture
def super_admin_token(client, super_admin_data, create_super_admin):
    """슈퍼 관리자 로그인 후 토큰 반환"""
    response = client.post("/api/admin/auth/login", json={
        "email": super_admin_data["email"],
        "password": super_admin_data["password"]
    })
    return response.json()["access_token"]


@pytest.fixture
def normal_admin_token(client, admin_data, create_normal_admin):
    """일반 관리자 로그인 후 토큰 반환"""
    response = client.post("/api/admin/auth/login", json={
        "email": admin_data["email"],
        "password": admin_data["password"]
    })
    return response.json()["access_token"]


# ============================================
# 1. Admin 로그인 테스트
# ============================================

def test_admin_login_success(client, super_admin_data, create_super_admin):
    """관리자 로그인 성공"""
    response = client.post("/api/admin/auth/login", json={
        "email": super_admin_data["email"],
        "password": super_admin_data["password"]
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "super_admin"
    assert len(data["access_token"]) > 0


def test_admin_login_invalid_email(client):
    """존재하지 않는 이메일로 로그인 실패"""
    response = client.post("/api/admin/auth/login", json={
        "email": "nonexistent@admin.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    data = response.json()
    assert "message" in data
    assert "이메일" in data["message"] or "비밀번호" in data["message"]


def test_admin_login_invalid_password(client, super_admin_data, create_super_admin):
    """잘못된 비밀번호로 로그인 실패"""
    response = client.post("/api/admin/auth/login", json={
        "email": super_admin_data["email"],
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    data = response.json()
    assert "message" in data
    assert "이메일" in data["message"] or "비밀번호" in data["message"]


def test_admin_login_inactive_admin(client, db_session, super_admin_data, create_super_admin):
    """비활성화된 관리자 로그인 실패"""
    # 관리자 비활성화
    admin = db_session.query(Admin).filter(Admin.email == super_admin_data["email"]).first()
    admin.is_active = False
    db_session.commit()

    response = client.post("/api/admin/auth/login", json={
        "email": super_admin_data["email"],
        "password": super_admin_data["password"]
    })

    assert response.status_code == 403
    data = response.json()
    assert "비활성화" in data["message"]


def test_admin_login_creates_session(client, db_session, super_admin_data, create_super_admin):
    """로그인 시 세션이 DB에 저장되는지 확인"""
    response = client.post("/api/admin/auth/login", json={
        "email": super_admin_data["email"],
        "password": super_admin_data["password"]
    })

    assert response.status_code == 200
    token = response.json()["access_token"]

    # 세션 확인
    session = db_session.query(AdminSession).filter(AdminSession.token == token).first()
    assert session is not None
    assert session.admin_id == create_super_admin.id
    assert session.expires_at > datetime.utcnow()


# ============================================
# 2. Admin 로그아웃 테스트
# ============================================

def test_admin_logout_success(client, db_session, super_admin_token):
    """로그아웃 성공 및 세션 삭제 확인"""
    # 로그아웃 전 세션 확인
    session_before = db_session.query(AdminSession).filter(
        AdminSession.token == super_admin_token
    ).first()
    assert session_before is not None

    # 로그아웃
    response = client.post(
        "/api/admin/auth/logout",
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "로그아웃" in data["message"]

    # 세션 삭제 확인
    session_after = db_session.query(AdminSession).filter(
        AdminSession.token == super_admin_token
    ).first()
    assert session_after is None


def test_admin_logout_without_token(client):
    """토큰 없이 로그아웃 시도 실패"""
    response = client.post("/api/admin/auth/logout")
    assert response.status_code == 401


def test_admin_logout_with_invalid_token(client):
    """유효하지 않은 토큰으로 로그아웃 시도 실패"""
    response = client.post(
        "/api/admin/auth/logout",
        headers={"Authorization": "Bearer invalid.token.format"}
    )
    assert response.status_code == 401


# ============================================
# 3. Admin CRUD 테스트 (슈퍼 관리자만 가능)
# ============================================

def test_create_admin_success(client, super_admin_token):
    """관리자 생성 성공 (슈퍼 관리자)"""
    new_admin_data = {
        "email": "new@admin.com",
        "username": "newadmin",
        "password": "NewPass123!",
        "role": "admin"
    }

    response = client.post(
        "/api/admin/users",
        json=new_admin_data,
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == new_admin_data["email"]
    assert data["username"] == new_admin_data["username"]
    assert data["role"] == new_admin_data["role"]
    assert data["is_active"] is True
    assert "id" in data
    assert "hashed_password" not in data


def test_create_admin_duplicate_email(client, super_admin_token, admin_data, create_normal_admin):
    """중복 이메일로 관리자 생성 실패"""
    response = client.post(
        "/api/admin/users",
        json={
            "email": admin_data["email"],  # 이미 존재하는 이메일
            "username": "different_username",
            "password": "Password123!",
            "role": "admin"
        },
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 400
    data = response.json()
    assert "이메일" in data["message"]


def test_create_admin_duplicate_username(client, super_admin_token, admin_data, create_normal_admin):
    """중복 사용자명으로 관리자 생성 실패"""
    response = client.post(
        "/api/admin/users",
        json={
            "email": "different@admin.com",
            "username": admin_data["username"],  # 이미 존재하는 사용자명
            "password": "Password123!",
            "role": "admin"
        },
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 400
    data = response.json()
    assert "사용자명" in data["message"]


def test_list_admins_success(client, super_admin_token, create_normal_admin):
    """관리자 목록 조회 성공"""
    response = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # 슈퍼 관리자 + 일반 관리자


def test_list_admins_with_pagination(client, super_admin_token):
    """페이지네이션을 사용한 관리자 목록 조회"""
    response = client.get(
        "/api/admin/users?skip=0&limit=1",
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 1


def test_get_admin_success(client, super_admin_token, create_normal_admin):
    """관리자 상세 조회 성공"""
    admin_id = create_normal_admin.id

    response = client.get(
        f"/api/admin/users/{admin_id}",
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == admin_id
    assert data["email"] == create_normal_admin.email
    assert data["username"] == create_normal_admin.username


def test_get_admin_not_found(client, super_admin_token):
    """존재하지 않는 관리자 조회 실패"""
    response = client.get(
        "/api/admin/users/99999",
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 404
    data = response.json()
    assert "찾을 수 없습니다" in data["message"]


def test_update_admin_success(client, super_admin_token, create_normal_admin):
    """관리자 정보 수정 성공"""
    admin_id = create_normal_admin.id
    update_data = {
        "username": "updated_admin",
        "role": "super_admin"
    }

    response = client.put(
        f"/api/admin/users/{admin_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == update_data["username"]
    assert data["role"] == update_data["role"]


def test_update_admin_duplicate_email(client, super_admin_token, super_admin_data, create_normal_admin):
    """다른 관리자의 이메일로 수정 시도 실패"""
    admin_id = create_normal_admin.id

    response = client.put(
        f"/api/admin/users/{admin_id}",
        json={"email": super_admin_data["email"]},  # 슈퍼 관리자의 이메일
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 400
    data = response.json()
    assert "이메일" in data["message"]


def test_delete_admin_success(client, super_admin_token, create_normal_admin):
    """관리자 삭제 성공"""
    admin_id = create_normal_admin.id

    response = client.delete(
        f"/api/admin/users/{admin_id}",
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 204


def test_delete_admin_not_found(client, super_admin_token):
    """존재하지 않는 관리자 삭제 시도 실패"""
    response = client.delete(
        "/api/admin/users/99999",
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 404


# ============================================
# 4. 권한 검증 테스트
# ============================================

def test_normal_admin_cannot_create_admin(client, normal_admin_token):
    """일반 관리자는 관리자를 생성할 수 없음"""
    new_admin_data = {
        "email": "new@admin.com",
        "username": "newadmin",
        "password": "NewPass123!",
        "role": "admin"
    }

    response = client.post(
        "/api/admin/users",
        json=new_admin_data,
        headers={"Authorization": f"Bearer {normal_admin_token}"}
    )

    assert response.status_code == 403
    data = response.json()
    assert "슈퍼 관리자" in data["message"]


def test_normal_admin_cannot_list_admins(client, normal_admin_token):
    """일반 관리자는 관리자 목록을 조회할 수 없음"""
    response = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {normal_admin_token}"}
    )

    assert response.status_code == 403
    data = response.json()
    assert "슈퍼 관리자" in data["message"]


def test_normal_admin_cannot_update_admin(client, normal_admin_token, create_super_admin):
    """일반 관리자는 다른 관리자 정보를 수정할 수 없음"""
    admin_id = create_super_admin.id

    response = client.put(
        f"/api/admin/users/{admin_id}",
        json={"username": "hacked"},
        headers={"Authorization": f"Bearer {normal_admin_token}"}
    )

    assert response.status_code == 403
    data = response.json()
    assert "슈퍼 관리자" in data["message"]


def test_normal_admin_cannot_delete_admin(client, normal_admin_token, create_super_admin):
    """일반 관리자는 관리자를 삭제할 수 없음"""
    admin_id = create_super_admin.id

    response = client.delete(
        f"/api/admin/users/{admin_id}",
        headers={"Authorization": f"Bearer {normal_admin_token}"}
    )

    assert response.status_code == 403
    data = response.json()
    assert "슈퍼 관리자" in data["message"]


def test_unauthenticated_cannot_access_admin_endpoints(client):
    """인증되지 않은 사용자는 관리자 엔드포인트에 접근할 수 없음"""
    # 관리자 생성
    response = client.post("/api/admin/users", json={
        "email": "test@admin.com",
        "username": "testadmin",
        "password": "Test123!",
        "role": "admin"
    })
    assert response.status_code == 401

    # 관리자 목록 조회
    response = client.get("/api/admin/users")
    assert response.status_code == 401

    # 로그아웃
    response = client.post("/api/admin/auth/logout")
    assert response.status_code == 401


# ============================================
# 5. 세션 검증 테스트
# ============================================

def test_valid_session_allows_access(client, super_admin_token):
    """유효한 세션은 접근 허용"""
    response = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 200


def test_expired_session_denies_access(client, db_session, super_admin_token):
    """만료된 세션은 접근 거부"""
    # 세션 만료 시간을 과거로 변경
    session = db_session.query(AdminSession).filter(
        AdminSession.token == super_admin_token
    ).first()
    session.expires_at = datetime.utcnow() - timedelta(hours=1)
    db_session.commit()

    response = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 401
    data = response.json()
    assert "세션" in data["message"] or "만료" in data["message"]


def test_deleted_session_denies_access(client, db_session, super_admin_token):
    """삭제된 세션은 접근 거부"""
    # 세션 삭제
    db_session.query(AdminSession).filter(
        AdminSession.token == super_admin_token
    ).delete()
    db_session.commit()

    response = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 401


def test_invalid_token_format_denies_access(client):
    """잘못된 형식의 토큰은 접근 거부"""
    response = client.get(
        "/api/admin/users",
        headers={"Authorization": "Bearer invalid.token.format"}
    )

    assert response.status_code == 401


# ============================================
# 6. 자기 자신 삭제 불가 테스트
# ============================================

def test_super_admin_cannot_delete_self(client, super_admin_token, create_super_admin):
    """슈퍼 관리자는 자기 자신을 삭제할 수 없음"""
    admin_id = create_super_admin.id

    response = client.delete(
        f"/api/admin/users/{admin_id}",
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    assert response.status_code == 400
    data = response.json()
    assert "자기 자신" in data["message"]


def test_admin_remains_after_failed_self_delete(client, db_session, super_admin_token, create_super_admin):
    """자기 자신 삭제 시도 실패 후에도 관리자는 여전히 존재"""
    admin_id = create_super_admin.id

    # 삭제 시도
    client.delete(
        f"/api/admin/users/{admin_id}",
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    # 관리자가 여전히 DB에 존재하는지 확인
    admin = db_session.query(Admin).filter(Admin.id == admin_id).first()
    assert admin is not None
    assert admin.is_active is True


# ============================================
# 7. 추가 엣지 케이스 테스트
# ============================================

def test_inactive_admin_cannot_access_endpoints(client, db_session, super_admin_data, create_super_admin):
    """비활성화된 관리자는 로그인은 되지만 엔드포인트 접근 불가"""
    # 먼저 로그인
    login_response = client.post("/api/admin/auth/login", json={
        "email": super_admin_data["email"],
        "password": super_admin_data["password"]
    })
    token = login_response.json()["access_token"]

    # 관리자 비활성화
    admin = db_session.query(Admin).filter(Admin.email == super_admin_data["email"]).first()
    admin.is_active = False
    db_session.commit()

    # 엔드포인트 접근 시도
    response = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )

    # 현재 구현에 따라 403 또는 401 예상
    assert response.status_code in [401, 403]


def test_create_admin_with_invalid_role(client, super_admin_token):
    """유효하지 않은 role로 관리자 생성 (현재는 검증하지 않지만 테스트 추가)"""
    new_admin_data = {
        "email": "invalid@admin.com",
        "username": "invalidrole",
        "password": "Pass123!",
        "role": "invalid_role"
    }

    response = client.post(
        "/api/admin/users",
        json=new_admin_data,
        headers={"Authorization": f"Bearer {super_admin_token}"}
    )

    # 현재는 어떤 role이든 허용하지만, 향후 검증 추가 시 400 예상
    # 지금은 201 성공
    assert response.status_code == 201


def test_multiple_sessions_per_admin(client, super_admin_data, create_super_admin):
    """한 관리자가 여러 세션을 가질 수 있는지 테스트"""
    import time

    # 첫 번째 로그인
    response1 = client.post("/api/admin/auth/login", json={
        "email": super_admin_data["email"],
        "password": super_admin_data["password"]
    })
    token1 = response1.json()["access_token"]

    # 토큰이 달라지도록 잠시 대기 (JWT exp 값이 변경됨)
    time.sleep(1)

    # 두 번째 로그인
    response2 = client.post("/api/admin/auth/login", json={
        "email": super_admin_data["email"],
        "password": super_admin_data["password"]
    })
    token2 = response2.json()["access_token"]

    # 두 토큰이 다른지 확인
    assert token1 != token2

    # 두 토큰 모두 유효한지 확인
    response1 = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response1.status_code == 200

    response2 = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response2.status_code == 200


def test_logout_only_affects_current_session(client, db_session, super_admin_data, create_super_admin):
    """로그아웃은 현재 세션만 영향을 미침"""
    import time

    # 두 개의 세션 생성
    response1 = client.post("/api/admin/auth/login", json={
        "email": super_admin_data["email"],
        "password": super_admin_data["password"]
    })
    token1 = response1.json()["access_token"]

    # 토큰이 달라지도록 잠시 대기
    time.sleep(1)

    response2 = client.post("/api/admin/auth/login", json={
        "email": super_admin_data["email"],
        "password": super_admin_data["password"]
    })
    token2 = response2.json()["access_token"]

    # 첫 번째 세션 로그아웃
    client.post(
        "/api/admin/auth/logout",
        headers={"Authorization": f"Bearer {token1}"}
    )

    # 첫 번째 토큰은 무효
    response = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response.status_code == 401

    # 두 번째 토큰은 여전히 유효
    response = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 200
