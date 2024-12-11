from sqlalchemy import Column, String
from app.models.base import BaseModel

class Tenant(BaseModel):
    __tablename__ = "tenants"

    name = Column(String, nullable=False, index=True)