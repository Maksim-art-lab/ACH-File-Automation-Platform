from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.db import get_session
from server.core.models.models import User
from server.core.settings import SettingsJWT
from server.core.utils.token_service import TokenService

ts = TokenService()
settings = SettingsJWT()


class JWTAuth(HTTPBearer):
    def __init__(self, secret_key: str = None, auto_error: bool = True):
        super(JWTAuth, self).__init__(auto_error=auto_error)
        self.secret_key = secret_key

    async def get_current_user(self, token: str, session: AsyncSession) -> User:
        try:
            user = await ts.decode_user_jwt(token=token, session=session, secret_key=self.secret_key)
        except HTTPException:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return user

    async def __call__(self, request: Request, session: AsyncSession = Depends(get_session)) -> User:
        credentials = await super(JWTAuth, self).__call__(request)

        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid credentials scheme.")

        user = await self.get_current_user(credentials.credentials, session)

        return user


jwt_auth = JWTAuth()
jwt_auth_verification = JWTAuth(secret_key=settings.JWT_VERIFICATION_SECRET_KEY)
