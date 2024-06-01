from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, RootModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

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
    title: str = ""
    body: str = ""
    photos: str = ""

class ArticleUpdate(BaseModel):
    id: int
    title: str = None
    body: str = None
    photos: str = None

class ArticleList(RootModel):
    root: list[ArticleUpdate]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/articles", response_model=str)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(title=article.title, body=article.body, photos=article.photos)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return "Article created"

@app.get("/articles", response_model=list[ArticleCreate])
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    return articles

@app.get("/articles/{id}", response_model=ArticleCreate)
def get_article(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@app.put("/articles/{id}", response_model=str)
def update_article(id: int, article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.title:
        db_article.title = article.title
    if article.body:
        db_article.body = article.body
    if article.photos:
        db_article.photos = article.photos
    db.commit()
    db.refresh(db_article)
    return "Article updated"

@app.delete("/articles/{id}", response_model=str)
def delete_article(id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(db_article)
    db.commit()
    return "Article deleted"

@app.post("/articles/save", response_model=str)
def save_articles(articles: ArticleList, db: Session = Depends(get_db)):
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
            else:
                new_article = Article(id=article.id, title=article.title or "", body=article.body or "", photos=article.photos or "")
                db.add(new_article)
                db.commit()
                db.refresh(new_article)
        else:
            new_article = Article(title=article.title or "", body=article.body or "", photos=article.photos or "")
            db.add(new_article)
            db.commit()
            db.refresh(new_article)
    return "Articles saved"