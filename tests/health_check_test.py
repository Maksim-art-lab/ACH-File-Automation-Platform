from server.core.status_enum import StatusEnum


def test_health_check(test_client):
    response = test_client.get("/api/health-check/")
    assert response.status_code == 200
    assert response.json()["status"] == StatusEnum.success
