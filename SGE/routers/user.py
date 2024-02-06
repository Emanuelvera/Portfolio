from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from schemas.user import User

user_router = APIRouter()


#Login
@user_router.post('/login', tags= ["auth"])
def login(user: User):
    if user.email == "admin" and user.password == "admin":
        token : str = create_token(user.dict())
        return JSONResponse(status_code = 200, content = token)