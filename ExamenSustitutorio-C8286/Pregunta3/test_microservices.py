import requests

def test_auth_service():
    response = requests.post('http://localhost:5001/login', json={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    assert "token" in response.json()

def test_user_service():
    response = requests.post('http://localhost:5002/users', json={"name": "testuser"})
    assert response.status_code == 201
    response = requests.get('http://localhost:5002/users')
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_notification_service():
    response = requests.post('http://localhost:5003/notify', json={"user": "testuser"})
    assert response.status_code == 200

if __name__ == "__main__":
    test_auth_service()
    test_user_service()
    test_notification_service()
    print("All tests passed!")