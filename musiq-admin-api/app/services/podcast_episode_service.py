from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
import shutil
from typing import Optional
from pydub import AudioSegment
from mutagen.mp3 import MP3


from model.podcast_model import podcast
from model.podcast_episode_model import podcast_episode
from model.podcast_author_model import podcast_author
from model.category_model import categories
from services.admin_user_service import admin_get_email
from config.database import DIRECTORY
from services.podcast_service import *


###to convert seconds to HH:MM:SS format
def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return(str(round(hours)).zfill(2), str(round(mins)).zfill(2), str(round(seconds)).zfill(2))

###to check presence of any episode
def episode_audio_check(db,id):
    return  db.query(podcast_episode).filter(podcast_episode.id == id,podcast_episode.is_delete == False,podcast_episode.is_audio == True).first()

###get podcast details by id
def get_podcast_name(id,db):
    return db.query(podcast).filter(podcast.id == id,podcast.is_delete == False).first()


###check repitition of episode name
def episode_name_check(id,title,db):
    return db.query(podcast_episode).filter(podcast_episode.episode_title == title,podcast_episode.podcast_id == id,podcast_episode.is_delete == False).first()


###get all episodes of all podcast
def episode_get_all(db: Session,limit):
    return db.query(podcast_episode).filter(podcast_episode.is_delete == False).order_by(podcast_episode.id).limit(limit).all()


###get episode by its id
def episode_get_by_id(db: Session, id: int):
    return db.query(podcast_episode).filter(podcast_episode.id == id,podcast_episode.is_delete == False).first()


###get all episode detail for particular podcast by id
def episode_get_by_podcastid(db: Session, id: int,limit):
    return db.query(podcast_episode).filter(podcast_episode.podcast_id == id,podcast_episode.is_delete == False).order_by(podcast_episode.episode_number).limit(limit).all()


###enter new podcast details for particular podcast
def episode_details(db,model,email,uploaded_file = None):
    podcastname = episode_name_check(model.podcast_id,model.episode_title,db)
    if podcastname:
        raise HTTPException(status_code=400, detail="Episode name is already chosen for this podcast")
    temp = admin_get_email(email,db)
    ##to count episode number
    a = 1
    while db.query(podcast_episode).filter(podcast_episode.podcast_id == model.podcast_id,podcast_episode.episode_number == a).first():
        a = a + 1
    
    db_podcast = podcast_episode(podcast_id = model.podcast_id,
                    episode_number = a,
                    episode_title = model.episode_title,
                    description = model.description,
                    subtitles = model.subtitles,
                    is_delete = False,
                    created_by =temp.id,
                    is_active = True)
    
    db.add(db_podcast)
    db.commit()
    db.flush(db_podcast)

    if uploaded_file:
        # podcast_name = get_podcast_name(model.podcast_id,db)
        podcast_id = podcast_get_by_id(db,model.podcast_id)
        if podcast_id.title[0].isalpha():
            alphabet = podcast_id.title[0].upper()
        else:
            alphabet = "Mis"
        print(podcast_id.title)
        print(alphabet)
        file_location = f"{DIRECTORY}/podcast/{alphabet}/{podcast_id.title}/episodes"
        if not os.path.exists(file_location):
            os.makedirs(file_location)
        # file = uploaded_file.filename.split(".")
        filename = str(db_podcast.id) + ".mp3" 
        file1 = f"{file_location}/{filename}"
        with open(file1, "wb") as file_object:
            shutil.copyfileobj(uploaded_file.file, file_object) 
        podcast_id.no_of_episode =  1
        
        audio = MP3(uploaded_file.file)
        s = convert(audio.info.length)
        duration =f"{s[0]}:{s[1]}:{s[2]}"
        db_podcast.duration = duration
        # duration############
        db_podcast.is_audio = True
        db.commit()
    podcast_id = episode_get_by_id(db,db_podcast.id)
    return podcast_id


###update podcast episode details from existing details
def episode_update(db,id,model,email,uploaded_file):
    episodes =episode_get_by_id(db,id)
    if episodes:
        if model.episode_title:    
            podcastname = episode_name_check(episodes.podcast_id,model.episode_title,db)
            if podcastname:
                raise HTTPException(status_code=400, detail="Episode name is already chosen for this podcast")
            episodes.episode_title = model.episode_title

        if model.description:
            episodes.description = model.description

        if model.subtitles:
            episodes.subtitles = model.subtitles

        if uploaded_file:
            podcast_id = podcast_get_by_id(db,episodes.podcast_id)
            if podcast_id.title[0].isalpha():
                alphabet = podcast_id.title[0].upper()
            else:
                alphabet = "Mis"
            file_location = f"{DIRECTORY}/podcast/{alphabet}/{podcast_id.title}/episodes"
            if not os.path.exists(file_location):
                os.makedirs(file_location)
            filename = str(episodes.id) + ".mp3" 
            file1 = f"{file_location}/{filename}"
            with open(file1, "wb") as file_object:
                shutil.copyfileobj(uploaded_file.file, file_object) 
            podcast_id.no_of_episode =  1
            
            audio = MP3(uploaded_file.file)
            s = convert(audio.info.length)
            duration =f"{s[0]}:{s[1]}:{s[2]}"
            print(duration)
            episodes.duration = duration
            episodes.is_audio = True

        temp = admin_get_email(email,db)
        episodes.updated_by = temp.id
        db.commit()
        podcast_id = episode_get_by_id(db,episodes.id)
        return podcast_id
    return False


##to delete episode details from particular podcast
def episode_delete(db,id):
    temp = episode_get_by_id(db,id)
    if temp:
        temp.is_delete = True
        db.commit()
        return True
    return False