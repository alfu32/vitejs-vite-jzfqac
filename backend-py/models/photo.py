from sqlalchemy import Column, Integer, String
from database import Base

class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, default="")
    description = Column(String, default="")
    article_id = Column(Integer, index=True)
