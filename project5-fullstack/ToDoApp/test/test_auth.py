from fastapi import status, HTTPException
from jose import jwt
from datetime import datetime, timedelta

from ..main import app
from ..routers.auth import get_current_user, get_db, authenticate_user, create_access_token, get_current_user, SECRET_KEY, ALGORITHM
from ..models import Todos, Users
from .utils import *



app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_authenticater_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, '12345', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    wrong_pass_user = authenticate_user(test_user.username, 'wrong password', db)
    assert wrong_pass_user is False

    non_existing_user = authenticate_user('wrong user', '12345', db)
    assert non_existing_user is False

def test_create_access_token():
    username = 'yogesh'
    user_id = '1'
    role = 'admin'
    expires = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})

    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub':'testuser', 'id':'1', 'role':'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username':'testuser', 'id':'1', 'user_role':'admin'}

@pytest.mark.asyncio
async def test_get_current_user_missing_apyload():
    encode = {'role': 'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "could not validate user"
