from typing import Optional

from pydantic import BaseModel

from server.ach.schemas.get_companies_schema import GetCompanySchema
from server.core.status_enum import StatusEnum

class CsvValidateSchema(BaseModel):
    status: StatusEnum = StatusEnum.success
    errors: Optional[str]
    csv_json: Optional[str]
