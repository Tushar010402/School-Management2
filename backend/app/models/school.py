from sqlalchemy import Column, String, Integer, ForeignKey
from app.models.base import BaseModel

class School(BaseModel):
    __tablename__ = "schools"

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)
