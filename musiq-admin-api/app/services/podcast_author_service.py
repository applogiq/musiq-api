from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
import shutil

from model.podcast_author_model import podcast_author
from services.admin_user_service import admin_get_email
from config.database import DIRECTORY


def author_name_check(name,db):
    return db.query(podcast_author).filter(podcast_author.author_name == name,podcast_author.is_delete == False).first()

def author_get_all(db: Session):
    return db.query(podcast_author).filter(podcast_author.is_delete == False).all()

def author_get_by_id(db: Session, id: int):
    return db.query(podcast_author).filter(podcast_author.id == id,podcast_author.is_delete == False).first()



def author_details(db,author,email,uploaded_file = None):
    authorname = author_name_check(author.author_name,db)
    if authorname:
        raise HTTPException(status_code=400, detail="author is already register")
    temp = admin_get_email(email,db)
    db_author = podcast_author(author_name = author.author_name,
                    is_delete = False,
                    created_by =temp.id,
                    is_active = True)

    db.add(db_author)
    db.commit()
    db.flush(db_author)

    if uploaded_file:
        filename = db_author.id+".png"
        file_location = f"{DIRECTORY}/author/{filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(uploaded_file.file, file_object)  

        db_author.is_image = True
        db.commit()
    return db_author