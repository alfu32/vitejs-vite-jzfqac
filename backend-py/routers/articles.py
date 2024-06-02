from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from models.article import Article
from database import get_db

router = APIRouter()

class ArticleCreate(BaseModel):
    id: Optional[int] = None
    title: str = ""
    body: str = ""
    photos: str = ""

@router.post("/articles", response_model=ArticleCreate)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(title=article.title, body=article.body, photos=article.photos)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.get("/articles", response_model=List[ArticleCreate])
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    return articles

@router.get("/articles/{id}", response_model=ArticleCreate)
def get_article(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.put("/articles/{id}", response_model=ArticleCreate)
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

@router.delete("/articles/{id}", response_model=ArticleCreate)
def delete_article(id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(db_article)
    db.commit()
    return db_article

class ArticleList(BaseModel):
    __root__: List[ArticleCreate]

@router.post("/articles/save", response_model=List[ArticleCreate])
def save_articles(articles: ArticleList, db: Session = Depends(get_db)):
    saved_articles = []
    for article in articles.__root__:
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
