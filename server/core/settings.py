import re
from typing import Any, Dict, Optional, Tuple

from pydantic import BaseSettings, PostgresDsn, validator
from pydantic.env_settings import SettingsSourceCallable


class CustomPostgresDsn(PostgresDsn):
    allowed_schemes = {"postgres", "postgresql", "postgresql+asyncpg"}


class SettingsPostgres(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: Optional[CustomPostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return CustomPostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


class SettingsJWT(BaseSettings):
    JWT_REGISTRATION_SECRET_KEY: str
    JWT_VERIFICATION_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXP: int
    JWT_REFRESH_EXP: int

    @validator("JWT_ALGORITHM", pre=True)
    def validate_algorithm(cls, v: str, values: Dict[str, Any]) -> Optional[str]:
        available_algorithms = [
            "HS256",
            "HS384",
            "HS512",
            "ES256",
            "ES384",
            "ES512",
            "RS256",
            "RS384",
            "RS512",
            "PS256",
            "PS384",
            "PS512",
            "EdDSA",
            "ES256K",
        ]
        if v in available_algorithms:
            return v
        raise ValueError("Algorithm can not be found.")

    @validator("JWT_SECRET_KEY", pre=True)
    def validate_secret_key(cls, v: str, values: Dict[str, Any]):
        return v

    @validator("JWT_REGISTRATION_SECRET_KEY", pre=True)
    def validate_registration_secret_key(cls, v: str, values: Dict[str, Any]):
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"


class SettingsAWS(BaseSettings):
    AWS_BUCKET_NAME_FROM: str = ""
    AWS_BUCKET_NAME_TO: str = ""
    AWS_REGION_NAME: str = ""
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_EMAIL_SENDER: str = ""
    HOST_NAME: str = ""
    EVOLVE_EMAIL_ADDRESS: str = ""
    AWS_S3_TRANSACTIONS_BUCKET: str = "test-s3-bucket"
    AWS_S3_CSV_TEMPLATE_GUIDE_BUCKET: str = ""
    CSV_TEMPLATE_KEY: str = ""
    GUIDE_KEY: str = ""
    GUIDE_FOR_TECHNICAL_SPECIALIST_KEY: str = ""
    GUIDE_ARCHITECTURE_DESCRIPTION_KEY: str = ""
    AWS_LAMBDA_LINK: str
    AWS_LAMBDA_LINK_SALES_TREND: str
    AWS_LAMBDA_LINK_TRANSACTION_FEES: str
    AWS_LAMBDA_LINK_SUMMARY: str
    AWS_LAMBDA_LINK_TRANSACTION: str
    AWS_LAMBDA_CALCULATION_API_KEY: str = ""
    DEPLOY_ON_LAMBDA: str = ""
    AWS_BUCKET_SENT_ACH_FILES_TO_EVOLVE: str = ""
    AWS_INITIAL_TRANSACTION_CSV_BUCKET: str = ""
    RETURNS_BUCKET_NAME: str
    TRACE_BUCKET_NAME: str

    class Config:
        # case_sensitive = True
        env_file = ".env"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return env_settings, file_secret_settings, init_settings

    @validator("AWS_EMAIL_SENDER")
    def validate_sender_username(cls, value):
        pattern = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"

        if re.match(pattern, value):
            return value
        raise ValueError("Email does not satisfy requirements.")


class SettingsDynamoDB(BaseSettings):
    METRICS_BY_PERIOD_TABLE_NAME: str
    SUMMARY_TABLE_NAME: str
    TRANSACTIONS_TABLE_NAME: str
    SERVICE_NAME: str

    class Config:
        case_sensitive = True
        env_file = ".env"


class SettingsSFTP(BaseSettings):
    SFTP_HOST: str
    PRIVATE_KEY: str
    SFTP_USER: str
    AWS_SECRET_MANAGER_NAME: str
    AWS_SECRET_MANAGER_KEY_NAME: str
    RETURNS_FOLDER_NAME: str
    TRACE_FOLDER_NAME: str

    class Config:
        case_sensitive = True
        env_file = ".env"


class SettingsEmailService(BaseSettings):
    HOST_NAME: str = ""
    MAIL_USERNAME: str = ""
    MAIL_USERNAME_SERVICE: str = ""
    MAIL_PASSWORD: str
    MAIL_PASSWORD_SERVICE: str
    MAIL_FROM: str = ""
    MAIL_FROM_SERVICE: str = ""
    MAIL_PORT: str = "587"
    EVOLVE_EMAIL_ADDRESS: str = ""
    MAIL_SERVER: str = "smtp.gmail.com"
    CLIENT_ID: str = ""
    CLIENT_SECRET: str = ""
    AWS_BUCKET_OUTLOOK_TOKEN_SERVICE: str = ""
    AWS_OUTLOOK_FILE_NAME: str = ""

    class Config:
        env_file = ".env"


class SettingsInitCsvBySftpService(BaseSettings):
    CONFIRMATION_EMAIL_TIMEOUT: int
    SFTP_IN_BUCKET: str

    class Config:
        env_file = ".env"


class SettingsSQS(BaseSettings):
    MANUAL_INITIATION_QUEUE: str

    class Config:
        case_sensitive = True
        env_file = ".env"


class SettingsServiceSupport(BaseSettings):
    SERVICE_SUPPORT_EMAILS: str

    class Config:
        case_sensitive = True
        env_file = ".env"


class SettingsConstants(BaseSettings):
    MAX_NUMBER_TRANSACTIONS_IN_CSV: int
    EM_8_INVALID_CONFIRMATION_EMAIL_IMAGE: str

    class Config:
        env_file = ".env"


class SettingsUseApiMvpRestricts(BaseSettings):
    USE_API_MVP_RESTRICTS: bool

    class Config:
        env_file = ".env"
