from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, RootModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import List, Optional

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, default="")
    body = Column(Text, default="")
    photos = Column(Text, default="")

Base.metadata.create_all(bind=engine)

app = FastAPI()

class ArticleCreate(BaseModel):
    id: Optional[int] = None
    title: str = ""
    body: str = ""
    photos: str = ""

class ArticleUpdate(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    body: Optional[str] = None
    photos: Optional[str] = None

class ArticleList(RootModel):
    root: List[ArticleUpdate]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/articles", response_model=ArticleCreate)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(title=article.title, body=article.body, photos=article.photos)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@app.get("/articles", response_model=List[ArticleCreate])
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    return articles

@app.get("/articles/{id}", response_model=ArticleCreate)
def get_article(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@app.put("/articles/{id}", response_model=ArticleCreate)
def update_article(id: int, article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.title is not None:
        db_article.title = article.title
    if article.body is not None:
        db_article.body = article.body
    if article.photos is not None:
        db_article.photos = article.photos
    db.commit()
    db.refresh(db_article)
    return db_article

@app.delete("/articles/{id}", response_model=ArticleCreate)
def delete_article(id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(db_article)
    db.commit()
    return db_article

@app.post("/articles/save", response_model=List[ArticleCreate])
def save_articles(articles: ArticleList, db: Session = Depends(get_db)):
    saved_articles = []
    for article in articles.root:
        if article.id:
            db_article = db.query(Article).filter(Article.id == article.id).first()
            if db_article:
                if article.title is not None:
                    db_article.title = article.title
                if article.body is not None:
                    db_article.body = article.body
                if article.photos is not None:
                    db_article.photos = article.photos
                db.commit()
                db.refresh(db_article)
                saved_articles.append(db_article)
            else:
                new_article = Article(id=article.id, title=article.title or "", body=article.body or "", photos=article.photos or "")
                db.add(new_article)
                db.commit()
                db.refresh(new_article)
                saved_articles.append(new_article)
        else:
            new_article = Article(title=article.title or "", body=article.body or "", photos=article.photos or "")
            db.add(new_article)
            db.commit()
            db.refresh(new_article)
            saved_articles.append(new_article)
    return saved_articles
