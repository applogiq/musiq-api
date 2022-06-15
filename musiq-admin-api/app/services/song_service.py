from requests import Session
from fastapi import Depends,HTTPException
from datetime import datetime
import os,time
import base64

# from utils.auth_handler import create_access_token
from model.song_model import *
from config.database import *
from model.album_model import *

def song_name_check(db,name):
    return db.query(songs).filter(songs.name == name,songs.is_delete == 0).first()


def song_detail(db:Session,song):
    # try:
    name =db.query(songs).filter(songs.name == song.name,songs.is_delete == 0).first()
    if name:
        if (name.artist_id["artist"]) == (song.artist_id["artist"]):
            raise HTTPException(status_code=400, detail="This song alreay exist")
        else:
            pass
    # if song.album_id:
    #     album = db.query(albums).filter(albums.album_id == song.album_id,albums.is_delete == 0).first()
    #     if album:
    #         pass
    #     else:
    #         raise HTTPException(status_code=400, detail="Check your album id")
    # else:
    #     raise HTTPException(status_code=400, detail="Enter Your album id")

    a ="SG001"
    while db.query(songs).filter(songs.song_id == a).first():
        a = "SG00" + str(int(a[-1])+1)
    if song.music:
        s = base64.b64decode(song.music)
        filename1 = a +"."+"wav"
        temp = db.query(albums).filter(albums.id == song.album_id,albums.is_delete == 0).first()
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
        music = 1
    else:
        music = 0
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
                    is_active = 1, 
                    is_delete = 0, 
                    created_by = "admin", 
                    is_music = music)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True