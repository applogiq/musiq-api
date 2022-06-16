from requests import Session
from fastapi import Depends,HTTPException
from datetime import datetime
import os,time
import base64



# from utils.auth_handler import create_access_token
from model.song_model import *
from config.database import *
from model.album_model import *
from services.admin_user_service import *
from services.album_service import *

def song_name_check(db,name):
    return db.query(songs).filter(songs.name == name,songs.is_delete == False).first()

def song_album_check(db,album_id):
    return db.query(songs).filter(songs.album_id == album_id,songs.is_delete == False).all()

def song_artist_check(db,artist_id):
    return db.query(songs).filter(songs.artist_id.contains([artist_id])).all()
  
     


def song_detail(db:Session,song,email):
    # try:
    name =song_name_check(db,song.name)
    if name:
        if (name.artist_id["artist"]) == (song.artist_id["artist"]):
            raise HTTPException(status_code=400, detail="This song alreay exist")
        else:
            pass
    if song.album_id:
        album = album_get_by_id(song.album_id,db)
        if album:
            pass
        else:
            raise HTTPException(status_code=400, detail="Check your album id")
    else:
        raise HTTPException(status_code=400, detail="Enter Your album id")

    a ="SG001"
    while db.query(songs).filter(songs.song_id == a).first():
        a = "SG00" + str(int(a[-1])+1)
    if song.music:
        s = base64.b64decode(song.music)
        filename1 = a +"."+"wav"
        temp = album_get_by_id(song.album_id,db)
        num = temp.no_of_songs
        if temp.name[0].isalpha():
            alphabet = temp.name[0].upper()
        else:
            alphabet = "Mis"
        file_location = f"{DIRECTORY}/music/tamil/{alphabet}/{temp.name}/songs"
        if os.path.exists(file_location):
            pass    
        else:
            os.makedirs(file_location)
        file_location2 = f"{file_location}/{filename1}"
        with open(file_location2, 'wb') as f:
            f.write(s)

        temp.no_of_songs = num+1
        music = True
    else:
        music = False
    temp = admin_get_email(email,db)
    db_user = songs(name =  song.name,
                    song_id = a,
                    artist_id = song.artist_id,
                    album_id = song.album_id,
                    genre_id = song.genre_id,
                    duration = song.duration,
                    lyrics = song.lyrics,
                    released_date =  song.released_date,
                    song_size = song.song_size,
                    label =  song.label,
                    is_active = True, 
                    is_delete = False, 
                    created_by = temp.id, 
                    is_music = music)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_songs(db: Session, skip,limit):
    user =  db.query(songs).filter(songs.is_delete == False).offset(skip).limit(limit).all()
    for i in range(0,len(user)):
        user[i].duration = str(user[i].duration)
        user[i].released_date = str(user[i].released_date)
        album_details = album_get_by_id(user[i].album_id,db)
        user[i].album_details = album_details
        print(user[i].album_id)
    return user

def get_song(db: Session, song_id: int):
    user = db.query(songs).filter(songs.id == song_id,songs.is_delete == False).first()
    album_details = db.query(albums).filter(albums.id == user.album_id,albums.is_delete == False).first()
    print(album_details,1111111)
    if user:
        user.duration = str(user.duration)
        user.released_date = str(user.released_date)
        user.album_details = album_details
        return user
    else:
        return False

def song_update(db: Session,song_id: int,song,email):
    user_temp1 = db.query(songs).filter(songs.id == song_id,songs.is_delete == False).first()
    if user_temp1:
        if song.name:
            songname =db.query(songs).filter(songs.name == song.name,songs.is_delete == False).first()
            if songname:
                if (songname.artist_id) == (song.artist_id):
                    raise HTTPException(status_code=400, detail="This song alreay exist")
                else:
                    pass
        user_temp1.name = song.name  
                    

        if song.artist_id:
            user_temp1.artist_id = song.artist_id
        if song.album_id:
            user_temp1.album_id = song.album_id
        if song.genre_id["genres"]:
            user_temp1.genre_id = song.genre_id
        if song.duration:
            user_temp1.duration = song.duration
        if song.lyrics:
            user_temp1.lyrics = song.lyrics
        if song.released_date:
            user_temp1.released_date = song.released_date
        if song.song_size:
            user_temp1.song_size = song.song_size
        if song.label:
            user_temp1.label = song.label
        if song.music:
            s = base64.b64decode(song.music)
            filename1 = user_temp1.song_id +"."+"wav"
            temp = db.query(albums).filter(albums.id == user_temp1.album_id,albums.is_delete == False).first()
            num = temp.no_of_songs
            if temp.name[0].isalpha():
                alphabet = temp.name[0].upper()
            else:
                alphabet = "Mis"
            file_location = f"public/music/tamil/{alphabet}/{temp.name}/songs"
            if os.path.exists(file_location):
                pass    
            else:
                os.makedirs(file_location)
            file_location2 = f"{file_location}/{filename1}"
            with open(file_location2, 'wb') as f:
                f.write(s)

            user_temp1.is_music = True
            temp.no_of_music = num+1
     
        temp1 = admin_get_email(email,db)
        user_temp1.updated_at = datetime.now()
        user_temp1.updated_by = temp1.id
        

        db.commit()

        return {'message': "data updated"}
    else:
        raise HTTPException(status_code=404, detail="song detail doesn't exist")
