
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.jwt_manager import validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        # Obtener el token de las cookies
        token = request.cookies.get("access_token")
        
        if not token:
            raise HTTPException(status_code=401, detail="No token provided")

        # Validar el token
        try:
            data = validate_token(token)
            if data['email'] != "admin":
                raise HTTPException(status_code=403, detail="Invalid credentials")
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))

'''
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data ['email'] != "admin":
            raise HTTPException(status_code = 403, detail = "Credenciales invalidas")'''
        
