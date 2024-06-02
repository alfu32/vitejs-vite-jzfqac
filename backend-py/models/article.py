from sqlalchemy import Column, Integer, String, Text
from database import Base

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, default="")
    body = Column(Text, default="")
    photos = Column(Text, default="")
