import datetime

import jwt
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.crud.user import UserCRUD
from server.core.models.models import User
from server.core.settings import SettingsJWT

settings = SettingsJWT()


class TokenService:
    """Service for processing jwt token"""

    @staticmethod
    async def decode_user_jwt(token: str, session: AsyncSession, secret_key: str = None) -> User:
        try:
            if secret_key:
                payload = jwt.decode(token, secret_key, algorithms=[settings.JWT_ALGORITHM])
            else:
                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Token expired")
        except BaseException:
            raise HTTPException(status_code=401, detail="Authorization failed.")
        user_id = payload["user_id"]

        user = await UserCRUD.retrieve_with_company(user_id, session)

        return user

    @staticmethod
    async def encode_user_jwt(user: User, secret_key: str = None) -> str:
        payload = {"user_id": user.id, "exp": datetime.datetime.now() + datetime.timedelta(minutes=settings.JWT_EXP)}
        if secret_key:
            token = jwt.encode(payload, secret_key, algorithm=settings.JWT_ALGORITHM)
        else:
            token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

        return token

    @staticmethod
    async def decode_user_refresh_jwt(token: str, session: AsyncSession) -> User:
        try:
            payload = jwt.decode(token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Refresh token expired")
        except BaseException:
            raise HTTPException(status_code=401, detail="Authorization failed.")
        user_id = payload["user_id"]
        user = await UserCRUD.retrieve_with_company(user_id, session)

        return user

    @staticmethod
    async def encode_user_refresh_jwt(user: User) -> str:
        payload = {
            "user_id": user.id,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=settings.JWT_REFRESH_EXP),
        }
        token = jwt.encode(payload, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

        return token
