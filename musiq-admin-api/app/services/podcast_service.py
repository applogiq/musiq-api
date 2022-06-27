from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
import shutil
from typing import Optional


from model.podcast_model import podcast
from model.podcast_author_model import podcast_author
from model.category_model import categories
from services.admin_user_service import admin_get_email
from config.database import DIRECTORY
from services.podcast_author_service import *


def podcast_name_check(title,db):
    return db.query(podcast).filter(podcast.title == title,podcast.is_delete == False).first()

def podcast_get_all(db: Session,limit):
    return db.query(podcast).filter(podcast.is_delete == False).order_by(podcast.id).limit(limit).all()

def podcast_get_by_id(db: Session, id: int):
    return db.query(podcast).filter(podcast.id == id,podcast.is_delete == False).first()

def podcast_details(db,model,email,uploaded_file = None):
    podcastname = podcast_name_check(model.title,db)
    if podcastname:
        raise HTTPException(status_code=400, detail="podcast is already register")
    temp = admin_get_email(email,db)
    authors = db.query(podcast_author).filter(podcast_author.id.in_(model.author_id[0].split(","))).all()
    name = []
    for i in authors:
        name.append(i.author_name)
    category = db.query(categories).filter(categories.id.in_(model.category_id[0].split(","))).all()
    name1 = []
    for i in category:
        name1.append(i.category_name)
    db_podcast = podcast(title = model.title,
                    description = model.description,
                    authors_id = model.author_id[0].split(","),
                    authors_name = name,
                    category_id = model.category_id[0].split(","),
                    category_name = name1,
                    is_delete = False,
                    created_by =temp.id,
                    is_active = True)

    db.add(db_podcast)
    db.commit()
    db.flush(db_podcast)

    if uploaded_file:
        filename = str(db_podcast.id)+".png"
        file_location = f"{DIRECTORY}/podcast/{filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(uploaded_file.file, file_object)  

        db_podcast.is_image = True
        db.commit()
    podcast_id = podcast_get_by_id(db,db_podcast.id)
    return podcast_id


def podcast_update(db,id,podcast,email,file):
    db_podcast = podcast_get_by_id(db,id)
    if db_podcast:
        if podcast.title:
            podcastname = podcast_name_check(podcast.title,db)
            if podcastname:
                raise HTTPException(status_code=400, detail="podcast is already register")
            db_podcast.title = podcast.title
        if podcast.description:
            db_podcast.description = podcast.description
        if podcast.author_id:
            authors = db.query(podcast_author).filter(podcast_author.id.in_(podcast.author_id[0].split(","))).all()
            name = []
            for i in authors:
                name.append(i.author_name)
            db_podcast.authors_id = podcast.author_id[0].split(",")
            db_podcast.authors_name = name
        if podcast.category_id:
            category = db.query(categories).filter(categories.id.in_(podcast.category_id[0].split(","))).all()
            name1 = []
            for i in category:
                name1.append(i.category_name)
            db_podcast.category_id = podcast.category_id[0].split(",")
            db_podcast.category_name = name1
        temp = admin_get_email(email,db)
        db_podcast.updated_by = temp.id
        db.commit()
        new_podcast = podcast_get_by_id(db,id)
        return new_podcast
    return False

def podcast_delete(db,id):
    temp = podcast_get_by_id(db,id)
    if temp:
        temp.is_delete = True
        db.commit()
        return True
    return False