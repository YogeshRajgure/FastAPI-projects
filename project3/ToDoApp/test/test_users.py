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
    pass
