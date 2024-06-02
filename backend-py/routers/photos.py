from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from models.photo import Photo
from database import get_db

router = APIRouter()

class PhotoCreate(BaseModel):
    id: Optional[int] = None
    url: str = ""
    description: str = ""
    article_id: Optional[int] = None

@router.post("/photos", response_model=PhotoCreate)
def create_photo(photo: PhotoCreate, db: Session = Depends(get_db)):
    db_photo = Photo(url=photo.url, description=photo.description, article_id=photo.article_id)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

@router.get("/photos", response_model=List[PhotoCreate])
def get_photos(db: Session = Depends(get_db)):
    photos = db.query(Photo).all()
    return photos

@router.get("/photos/{id}", response_model=PhotoCreate)
def get_photo(id: int, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id == id).first()
    if photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo

@router.put("/photos/{id}", response_model=PhotoCreate)
def update_photo(id: int, photo: PhotoCreate, db: Session = Depends(get_db)):
    db_photo = db.query(Photo).filter(Photo.id == id).first()
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    if photo.url is not None:
        db_photo.url = photo.url
    if photo.description is not None:
        db_photo.description = photo.description
    if photo.article_id is not None:
        db_photo.article_id = photo.article_id
    db.commit()
    db.refresh(db_photo)
    return db_photo

@router.delete("/photos/{id}", response_model=PhotoCreate)
def delete_photo(id: int, db: Session = Depends(get_db)):
    db_photo = db.query(Photo).filter(Photo.id == id).first()
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    db.delete(db_photo)
    db.commit()
    return db_photo

class PhotoList(BaseModel):
    __root__: List[PhotoCreate]

@router.post("/photos/save", response_model=List[PhotoCreate])
def save_photos(photos: PhotoList, db: Session = Depends(get_db)):
    saved_photos = []
    for photo in photos.__root__:
        if photo.id:
            db_photo = db.query(Photo).filter(Photo.id == photo.id).first()
            if db_photo:
                if photo.url is not None:
                    db_photo.url = photo.url
                if photo.description is not None:
                    db_photo.description = photo.description
                if photo.article_id is not None:
                    db_photo.article_id = photo.article_id
                db.commit()
                db.refresh(db_photo)
                saved_photos.append(db_photo)
            else:
                new_photo = Photo(id=photo.id, url=photo.url or "", description=photo.description or "", article_id=photo.article_id)
                db.add(new_photo)
                db.commit()
                db.refresh(new_photo)
                saved_photos.append(new_photo)
        else:
            new_photo = Photo(url=photo.url or "", description=photo.description or "", article_id=photo.article_id)
            db.add(new_photo)
            db.commit()
            db.refresh(new_photo)
            saved_photos.append(new_photo)
    return saved_photos
