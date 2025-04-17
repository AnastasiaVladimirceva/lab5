from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'ghost@mail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {"name": "Sergey Sergeev", "email": "s.sergeev@mail.com"}

    create_resp = client.post("/api/v1/user", json=new_user)
    assert create_resp.status_code == 201
    user_id = create_resp.json()
    assert isinstance(user_id, int) and user_id == 3

    get_resp = client.get("/api/v1/user", params={"email": new_user["email"]})
    assert get_resp.status_code == 200
    assert get_resp.json() == {"id": user_id, **new_user}

def test_create_user_with_invalid_email():
    '''Попытка создать пользователя с уже занятым email'''
    duplicate = {"name": "Somebody", "email": users[0]["email"]}
    resp = client.post("/api/v1/user", json=duplicate)
    assert resp.status_code == 409
    assert resp.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    email_to_delete = users[1]["email"]

    del_resp = client.delete("/api/v1/user", params={"email": email_to_delete})
    assert del_resp.status_code == 204
    assert del_resp.content == b""        # FastAPI при 204 возвращает пустое тело

    get_resp = client.get("/api/v1/user", params={"email": email_to_delete})
    assert get_resp.status_code == 404
    assert get_resp.json() == {"detail": "User not found"}