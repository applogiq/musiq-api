from requests import Session
from fastapi import Depends,HTTPException
from datetime import datetime
import os,time
import base64



# from utils.auth_handler import create_access_token
from model.song_model import *
from config.database import *
from model.album_model import *
from model.artist_model import artist
from services.admin_user_service import *
from services.album_service import *


def trending_hits(db,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_id,albums.album_name,albums.music_director_name,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.is_delete == False).order_by(songs.listeners.desc()).limit(limit).all()

def new_release(db,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_id,albums.album_name,albums.music_director_name,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.is_delete == False).order_by(songs.released_date.desc()).limit(limit).all()

def song_name_check(db,name):
    return db.query(songs).filter(songs.song_name == name,songs.is_delete == False).first()

def song_album_check(db,album_id,skip,limit):
    return db.query(songs).filter(songs.album_id == album_id,songs.is_delete == False).offset(skip).limit(limit).all()

def song_album_check_limit(db,album_id,skip,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_name,albums.music_director_name,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.album_id == album_id,songs.is_delete == False).offset(skip).limit(limit).all()

def song_artist_check(db,artist_id,skip,limit):
    return db.query(songs).filter(songs.artist_id.contains([artist_id]),songs.is_delete == False).offset(skip).limit(limit).all()

def song_artist_check_limit(db,artist_id,skip,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_name,albums.music_director_name,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.artist_id.contains([artist_id]),songs.is_delete == False).offset(skip).limit(limit).all()

def song_music_check(db,song_id):
    return  db.query(songs).filter(songs.id == song_id,songs.is_delete == False,songs.is_music == True).first()
     
def song_detail(db:Session,song,email):
    name =song_name_check(db,song.song_name)
    if name:
        if (name.artist_id) == (song.artist_id):
            raise HTTPException(status_code=400, detail={"success": False,'message': "This song already exist"})
        else:
            pass
    if song.album_id:
        album = album_get_by_id(song.album_id,db)
        if album:
            pass
        else:
            raise HTTPException(status_code=400, detail={"success": False,'message': "Check your album id"})
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
        if temp.album_name[0].isalpha():
            alphabet = temp.album_name[0].upper()
        else:
            alphabet = "Mis"
        file_location = f"{DIRECTORY}/music/tamil/{alphabet}/{temp.album_name}/songs"
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
    db_user = songs(song_name =  song.song_name.title(),
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

def song_get_all(db: Session, skip,limit):
    user =  db.query(songs).filter(songs.is_delete == False).offset(skip).limit(limit).all()
    for i in range(0,len(user)):
        user[i].duration = str(user[i].duration)
        user[i].released_date = str(user[i].released_date)
        album_details = album_get_by_id(user[i].album_id,db)
        user[i].album_details = album_details
        print(user[i].album_id)
    return user

def song_get_all_limit(db: Session, skip,limit):
    user = db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_id,albums.album_name,albums.music_director_name,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.is_delete == False).offset(skip).limit(limit).all()
    return user
    

def song_get_by_id(db: Session, song_id: int):
    user = db.query(songs).filter(songs.id == song_id,songs.is_delete == False).first() 
    if user:
        album_details = db.query(albums).filter(albums.id == user.album_id,albums.is_delete == False).first()
        user.duration = str(user.duration)
        user.released_date = str(user.released_date)
        user.album_details = album_details
        return user
    else:
        return False

def song_get_by_id_limit(db: Session, song_id: int):
    user = db.query().join(albums,albums.id == songs.album_id).filter(songs.id == song_id,songs.is_delete == False).all() 
    print(len(user))
    # user1 = db.query(songs).filter(artist.id.contains(songs[0].artist_id),songs.is_delete == False).all() 
    # print(user1)
    # if user:
    #     album_details = db.query(albums).filter(albums.id == user.album_id,albums.is_delete == False).first()
    #     user.duration = str(user.duration)
    #     user.released_date = str(user.released_date)
    #     user.album_details = album_details
    return user
    # else:
    #     return False


def song_update(db: Session,song_id: int,song,email):
    user_temp1 = db.query(songs).filter(songs.id == song_id,songs.is_delete == False).first()
    if user_temp1:
        if song.song_name:
            songname =song_name_check(db,song.song_name)
            if songname:
                if (songname.artist_id) == (song.artist_id):
                    raise HTTPException(status_code=400, detail={"success": False,'message': "This song already exist"})
                else:
                    pass
            user_temp1.song_name = song.song_name.title()          

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
            if temp.album_name[0].isalpha():
                alphabet = temp.album_name[0].upper()
            else:
                alphabet = "Mis"
            file_location = f"{DIRECTORY}/music/tamil/{alphabet}/{temp.album_name}/songs"
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
        result = song_get_by_id(db,song_id)
        return result

    
def delete_song_details(db: Session,song_id):
    user_temp = song_get_by_id(db,song_id)
    if user_temp:
        user_temp.is_delete = True
        db.commit()
        return True
    
