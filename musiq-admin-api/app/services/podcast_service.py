from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
import shutil
from typing import Optional
import os


from model.podcast_model import podcast
from model.podcast_author_model import podcast_author
from model.category_model import categories
from services.admin_user_service import admin_get_email
from config.database import DIRECTORY
from services.podcast_author_service import *

###check podcast name for avoid repitition
def podcast_name_check(title,db):
    return db.query(podcast).filter(podcast.title == title,podcast.is_delete == False).first()

###get all podcast details
def podcast_get_all(db: Session,limit):
    return db.query(podcast).filter(podcast.is_delete == False).order_by(podcast.id).limit(limit).all()


###get single podcast details by id
def podcast_get_by_id(db: Session, id):
    return db.query(podcast).filter(podcast.id == id,podcast.is_delete == False).first()


###enter new podcast details
def podcast_details(db,model,email):
    podcastname = podcast_name_check(model.title,db)
    if podcastname:
        raise HTTPException(status_code=400, detail="podcast is already register")
    temp = admin_get_email(email,db)
    authors = db.query(podcast_author).filter(podcast_author.id.in_(model.author_id)).all()
    name = []
    for i in authors:
        name.append(i.author_name)
    category = db.query(categories).filter(categories.id.in_(model.category_id)).all()
    name1 = []
    for i in category:
        name1.append(i.category_name)
    db_podcast = podcast(title = model.title,
                    description = model.description,
                    authors_id = model.author_id,
                    authors_name = name,
                    category_id = model.category_id,
                    category_name = name1,
                    is_delete = False,
                    created_by =temp.id,
                    is_active = True)
    if model.title[0].isalpha():
        alphabet = model.title[0].upper()
    else:
        alphabet = "Mis"

    path1 = f"{DIRECTORY}/podcast/{alphabet}/{model.title}"
    if os.path.exists(path1):
        pass
    else:
        os.makedirs(path1)

    db.add(db_podcast)
    db.commit()
    db.flush(db_podcast)

    if model.image:
        s = base64.b64decode(model.image)
        filename = str(db_podcast.id)+".png"
        file_location = f"{path1}/image"
        if os.path.exists(file_location):
            pass    
        else:
            os.makedirs(file_location)
        file_location1 = f"{file_location}/{filename}"
        with open(file_location1, "wb+") as f:
            f.write(s)

        db_podcast.is_image = True
        db.commit()
    podcast_id = podcast_get_by_id(db,db_podcast.id)
    return podcast_id


###update existing podcast details
def podcast_update(db,id,podcast,email):
    db_podcast = podcast_get_by_id(db,id)
    if db_podcast:
        if podcast.title:
            podcastname = podcast_name_check(podcast.title,db)
            if podcastname:
                raise HTTPException(status_code=400, detail="podcast is already register")
            if db_podcast.title[0].isalpha():
                alphabet = db_podcast.title[0].upper()
            else:
                alphabet = "Mis"
            if podcast.title[0].isalpha():
                alphabet1 = podcast.title[0].upper()
            else:
                alphabet1 = "Mis"
    
            source = f"{DIRECTORY}/podcast/{alphabet}/{db_podcast.title}"
            dest = f"{DIRECTORY}/podcast/{alphabet1}/{podcast.title}"
            # if not(source == dest):
            if os.path.exists(source):
              os.replace(source, dest)    
            db_podcast.title = podcast.title

        if podcast.description:
            db_podcast.description = podcast.description

        if podcast.author_id:
            authors = db.query(podcast_author).filter(podcast_author.id.in_(podcast.author_id)).all()
            name = []
            for i in authors:
                name.append(i.author_name)
            db_podcast.authors_id = podcast.author_id
            db_podcast.authors_name = name
        else:
            pass

        if podcast.category_id:
            category = db.query(categories).filter(categories.id.in_(podcast.category_id)).all()
            name1 = []
            for i in category:
                name1.append(i.category_name)
            db_podcast.category_id = podcast.category_id
            db_podcast.category_name = name1
        if podcast.image:
            s = base64.b64decode(podcast.image)
            filename1 =  str(db_podcast.id)+".png"
            if podcast.title:
                if podcast.title[0].isalpha():
                    alphabet = podcast.title[0].upper()
                else:
                    alphabet = "Mis"
                name = podcast.title
            else:
                if db_podcast.title[0].isalpha():
                    alphabet = db_podcast.title[0].upper()
                else:
                    alphabet = "Mis"
                name = db_podcast.title

            file_location = f"{DIRECTORY}/podcast/{alphabet}/{name}/image"
            if os.path.exists(file_location):
                pass    
            else:
                os.makedirs(file_location)
            file_location2 = f"{file_location}/{filename1}"
            with open(file_location2, 'wb') as f:
                f.write(s)
            db_podcast.is_image = True  

        
        temp = admin_get_email(email,db)
        db_podcast.updated_by = temp.id
        db.commit()
        new_podcast = podcast_get_by_id(db,id)
        return new_podcast
    return False


###delete single podcast entirely by id
def podcast_delete(db,id):
    temp = podcast_get_by_id(db,id)
    if temp:
        temp.is_delete = True
        db.commit()
        return True
    return False