"""Health Check 및 기본 엔드포인트 테스트"""
import pytest


def test_health_check(client):
    """Health Check 엔드포인트 테스트"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data
    assert "FastAPI" in data["message"]


def test_health_check_multiple_calls(client):
    """Health Check 엔드포인트 여러 번 호출"""
    for _ in range(5):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_root_path_not_found(client):
    """루트 경로는 정의되지 않음"""
    response = client.get("/")
    assert response.status_code == 404


def test_api_root_not_found(client):
    """/api 루트 경로는 정의되지 않음"""
    response = client.get("/api")
    assert response.status_code == 404


def test_docs_endpoint_exists(client):
    """API 문서 엔드포인트 존재 확인"""
    response = client.get("/docs")
    # docs는 HTML 반환하므로 200 또는 리다이렉트
    assert response.status_code in [200, 307]


def test_openapi_json_exists(client):
    """OpenAPI 스키마 JSON 엔드포인트 존재 확인"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "Module 5 API"
