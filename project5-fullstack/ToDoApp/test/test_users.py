from fastapi import status

from ..main import app
from ..routers.user import get_current_user, get_db
from ..models import Todos
from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_get_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'yogesh'
    assert response.json()['email'] == 'yogeshrajgure.vraj@gmail.com'
    assert response.json()['first_name'] == 'Yogesh'
    assert response.json()['last_name'] == 'Rajgure'
    assert response.json()['phone_number'] == '1111111111'

def test_change_password(test_user):
    response = client.put("/user/change_password", json={"password":"12345", "new_password":"123456"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/change_password", json={"password":"123456", "new_password":"1234567"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Error on password change'

def test_change_phone_number_success(test_user):
    response = client.put("/user/change_phone_number", params={"new_phone_number":"22222222222"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
