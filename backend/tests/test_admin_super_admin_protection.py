"""슈퍼 관리자 보호 테스트 (최소 1명 유지)"""

import pytest
from app.models.admin import Admin
from app.utils.auth import hash_password


# ============================================
# Role 변경 보호 테스트
# ============================================

def test_cannot_demote_last_super_admin(client, db_session):
    """마지막 슈퍼 관리자의 role을 변경할 수 없음"""
    # 슈퍼 관리자 1명 생성
    super_admin = Admin(
        email="super@example.com",
        username="superadmin",
        hashed_password=hash_password("password123"),
        role="super_admin",
        is_active=True
    )
    db_session.add(super_admin)
    db_session.commit()
    db_session.refresh(super_admin)

    # 로그인
    login_response = client.post("/api/admin/auth/login", json={
        "email": "super@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    # role을 admin으로 변경 시도
    response = client.put(
        f"/api/admin/users/{super_admin.id}",
        json={"role": "admin"},
        headers={"Authorization": f"Bearer {token}"}
    )

    # 검증
    assert response.status_code == 400
    assert "최소 1명의 슈퍼 관리자가 필요합니다" in response.json()["message"]


def test_can_demote_super_admin_when_others_exist(client, db_session):
    """다른 슈퍼 관리자가 있으면 role 변경 가능"""
    # 슈퍼 관리자 2명 생성
    super_admin1 = Admin(
        email="super1@example.com",
        username="superadmin1",
        hashed_password=hash_password("password123"),
        role="super_admin",
        is_active=True
    )
    super_admin2 = Admin(
        email="super2@example.com",
        username="superadmin2",
        hashed_password=hash_password("password123"),
        role="super_admin",
        is_active=True
    )
    db_session.add_all([super_admin1, super_admin2])
    db_session.commit()
    db_session.refresh(super_admin1)
    db_session.refresh(super_admin2)

    # 슈퍼 관리자 1로 로그인
    login_response = client.post("/api/admin/auth/login", json={
        "email": "super1@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    # 슈퍼 관리자 2의 role을 admin으로 변경
    response = client.put(
        f"/api/admin/users/{super_admin2.id}",
        json={"role": "admin"},
        headers={"Authorization": f"Bearer {token}"}
    )

    # 검증
    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_inactive_super_admin_not_counted(client, db_session):
    """비활성 슈퍼 관리자는 카운트에서 제외됨"""
    # 활성 슈퍼 관리자 1명
    super_admin_active = Admin(
        email="super_active@example.com",
        username="superadmin_active",
        hashed_password=hash_password("password123"),
        role="super_admin",
        is_active=True
    )
    # 비활성 슈퍼 관리자 1명
    super_admin_inactive = Admin(
        email="super_inactive@example.com",
        username="superadmin_inactive",
        hashed_password=hash_password("password123"),
        role="super_admin",
        is_active=False
    )
    db_session.add_all([super_admin_active, super_admin_inactive])
    db_session.commit()
    db_session.refresh(super_admin_active)

    # 활성 슈퍼 관리자로 로그인
    login_response = client.post("/api/admin/auth/login", json={
        "email": "super_active@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    # 활성 슈퍼 관리자의 role을 admin으로 변경 시도
    response = client.put(
        f"/api/admin/users/{super_admin_active.id}",
        json={"role": "admin"},
        headers={"Authorization": f"Bearer {token}"}
    )

    # 검증 (비활성 관리자는 카운트에서 제외되므로 실패해야 함)
    assert response.status_code == 400
    assert "최소 1명의 슈퍼 관리자가 필요합니다" in response.json()["message"]


def test_can_update_other_fields_of_last_super_admin(client, db_session):
    """마지막 슈퍼 관리자의 다른 필드는 수정 가능"""
    # 슈퍼 관리자 1명 생성
    super_admin = Admin(
        email="super@example.com",
        username="superadmin",
        hashed_password=hash_password("password123"),
        role="super_admin",
        is_active=True
    )
    db_session.add(super_admin)
    db_session.commit()
    db_session.refresh(super_admin)

    # 로그인
    login_response = client.post("/api/admin/auth/login", json={
        "email": "super@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    # 사용자명만 변경
    response = client.put(
        f"/api/admin/users/{super_admin.id}",
        json={"username": "newsuperadmin"},
        headers={"Authorization": f"Bearer {token}"}
    )

    # 검증 (role 변경이 아니므로 성공해야 함)
    assert response.status_code == 200
    assert response.json()["username"] == "newsuperadmin"
    assert response.json()["role"] == "super_admin"


# ============================================
# 삭제 보호 테스트
# ============================================

def test_cannot_delete_last_super_admin(client, db_session):
    """마지막 슈퍼 관리자는 삭제할 수 없음"""
    # 슈퍼 관리자 1명, 일반 관리자 1명 생성
    super_admin = Admin(
        email="super@example.com",
        username="superadmin",
        hashed_password=hash_password("password123"),
        role="super_admin",
        is_active=True
    )
    regular_admin = Admin(
        email="admin@example.com",
        username="admin",
        hashed_password=hash_password("password123"),
        role="admin",
        is_active=True
    )
    db_session.add_all([super_admin, regular_admin])
    db_session.commit()
    db_session.refresh(super_admin)
    db_session.refresh(regular_admin)

    # 슈퍼 관리자로 로그인
    login_response = client.post("/api/admin/auth/login", json={
        "email": "super@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    # 일반 관리자 삭제 (성공해야 함)
    response = client.delete(
        f"/api/admin/users/{regular_admin.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

    # 슈퍼 관리자 삭제 시도 (자기 자신이므로 실패)
    response = client.delete(
        f"/api/admin/users/{super_admin.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400


def test_can_delete_super_admin_when_others_exist(client, db_session):
    """다른 슈퍼 관리자가 있으면 삭제 가능"""
    # 슈퍼 관리자 2명 생성
    super_admin1 = Admin(
        email="super1@example.com",
        username="superadmin1",
        hashed_password=hash_password("password123"),
        role="super_admin",
        is_active=True
    )
    super_admin2 = Admin(
        email="super2@example.com",
        username="superadmin2",
        hashed_password=hash_password("password123"),
        role="super_admin",
        is_active=True
    )
    db_session.add_all([super_admin1, super_admin2])
    db_session.commit()
    db_session.refresh(super_admin1)
    db_session.refresh(super_admin2)

    # 슈퍼 관리자 1로 로그인
    login_response = client.post("/api/admin/auth/login", json={
        "email": "super1@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    # 슈퍼 관리자 2 삭제
    response = client.delete(
        f"/api/admin/users/{super_admin2.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    # 검증
    assert response.status_code == 204

    # DB에서 삭제되었는지 확인
    deleted_admin = db_session.query(Admin).filter(Admin.id == super_admin2.id).first()
    assert deleted_admin is None


def test_cannot_delete_last_super_admin_even_with_inactive(client, db_session):
    """비활성 슈퍼 관리자가 있어도 마지막 활성 슈퍼 관리자는 삭제 불가"""
    # 활성 슈퍼 관리자 1명
    super_admin_active = Admin(
        email="super_active@example.com",
        username="superadmin_active",
        hashed_password=hash_password("password123"),
        role="super_admin",
        is_active=True
    )
    # 비활성 슈퍼 관리자 1명
    super_admin_inactive = Admin(
        email="super_inactive@example.com",
        username="superadmin_inactive",
        hashed_password=hash_password("password123"),
        role="super_admin",
        is_active=False
    )
    # 일반 관리자 1명
    regular_admin = Admin(
        email="admin@example.com",
        username="admin",
        hashed_password=hash_password("password123"),
        role="admin",
        is_active=True
    )
    db_session.add_all([super_admin_active, super_admin_inactive, regular_admin])
    db_session.commit()
    db_session.refresh(super_admin_active)
    db_session.refresh(regular_admin)

    # 활성 슈퍼 관리자로 로그인
    login_response = client.post("/api/admin/auth/login", json={
        "email": "super_active@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    # 일반 관리자 삭제 (성공)
    response = client.delete(
        f"/api/admin/users/{regular_admin.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

    # 활성 슈퍼 관리자 삭제 시도 (자기 자신이므로 실패)
    response = client.delete(
        f"/api/admin/users/{super_admin_active.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert "자기 자신은 삭제할 수 없습니다" in response.json()["message"]
