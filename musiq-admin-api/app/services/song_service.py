from requests import Session
from fastapi import Depends,HTTPException
from datetime import datetime
import os
import base64
import shutil
from mutagen.mp3 import MP3

from model.song_model import *
from config.database import *
from model.album_model import *
from services.admin_user_service import *
from services.album_service import *

###convert the seconds to HH:MM:SS format for song duration
def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return(str(round(hours)).zfill(2), str(round(mins)).zfill(2), str(round(seconds)).zfill(2))

###to get trending hits detail
def trending_hits(db,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_id,albums.album_name,albums.music_director_name,albums.premium_status,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.is_delete == False).order_by(songs.listeners.desc()).limit(limit).all()

###to get new release detail
def new_release(db,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_id,albums.album_name,albums.music_director_name,albums.premium_status,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.is_delete == False).order_by(songs.released_date.desc()).limit(limit).all()

###to check whether song name already used
def song_name_check(db,name):
    return db.query(songs).filter(songs.song_name == name,songs.is_delete == False).first()

###to fetch songs for particular album
def song_album_check(db,album_id,skip,limit):
    return db.query(songs).filter(songs.album_id == album_id,songs.is_delete == False).offset(skip).limit(limit).all()

###to fetch particular song details for particular album
def song_album_check_limit(db,album_id,skip,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_name,albums.music_director_name,albums.premium_status,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.album_id == album_id,songs.is_delete == False).offset(skip).limit(limit).all()

###to fetch song details for particular artist
def song_artist_check(db,artist_id,skip,limit):
    return db.query(songs).filter(songs.artist_id.contains([artist_id]),songs.is_delete == False).offset(skip).limit(limit).all()

###to fetch particular song details for particular artist
def song_artist_check_limit(db,artist_id,skip,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_name,albums.music_director_name,albums.premium_status,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.artist_id.contains([artist_id]),songs.is_delete == False).offset(skip).limit(limit).all()

###to check music is available for this id
def song_music_check(db,song_id):
    return  db.query(songs).filter(songs.id == song_id,songs.is_delete == False,songs.is_music == True).first()

###enter new song details with song(base64)    
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
    song_length = len(db.query(songs).all())
    if song_length:
        b = song_length+1
    else:
        b = 1
    a = "SG00"+str(b)
    # while db.query(songs).filter(songs.song_id == a).first():
    #     a = "SG00" + str(int(a[-1])+1)
    if song.music:
        s = base64.b64decode(song.music)
        filename1 = a +"."+"wav"
        num = album.no_of_songs
        if album.album_name[0].isalpha():
            alphabet = album.album_name[0].upper()
        else:
            alphabet = "Mis"
        file_location = f"{DIRECTORY}/music/tamil/{alphabet}/{album.album_name}/songs"
        if os.path.exists(file_location):
            pass    
        else:
            os.makedirs(file_location)
        file_location2 = f"{file_location}/{filename1}"
        with open(file_location2, 'wb') as f:
            f.write(s)

        album.no_of_songs = num+1
        
        music = True
    else:
        music = False
    db_admin = admin_get_email(email,db)
    db_user = songs(song_name =  song.song_name.title(),
                    song_id = a,
                    artist_id = song.artist_id,
                    album_id = song.album_id,
                    genre_id = song.genre_id,
                    lyrics = song.lyrics,
                    released_date =  song.released_date,
                    song_size = song.song_size,
                    label =  song.label,
                    # premium_status = album.premium_status,
                    is_active = True, 
                    is_delete = False, 
                    created_by = db_admin.id, 
                    is_music = music)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

###enter song details alone
def song_new_detail(db:Session,song,email):
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
    
    temp = admin_get_email(email,db)
    db_user = songs(song_name =  song.song_name.title(),
                    song_id = a,
                    artist_id = song.artist_id,
                    album_id = song.album_id,
                    genre_id = song.genre_id,
                    duration = "00:00:00",
                    lyrics = song.lyrics,
                    released_date =  song.released_date,
                    song_size = song.song_size,
                    # premium_status = album.premium_status,
                    label =  song.label,
                    is_active = True, 
                    is_delete = False, 
                    created_by = temp.id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

###upload music for particular id
def music_upload(db,id,uploaded_file):
    db_song = song_get_by_id(db,id)
    if db_song:
        s = (uploaded_file.filename).split(".")
        filename1 = db_song.song_id +"."+s[-1]
        temp = album_get_by_id(db_song.album_id,db)
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
            shutil.copyfileobj(uploaded_file.file, f)

        temp.no_of_songs = num+1
        if s[-1] == "mp3":
            audio = MP3(uploaded_file.file)
            s = convert(audio.info.length)
            song_duration =f"{s[0]}:{s[1]}:{s[2]}"
        db_song.is_music = True
        db_song.duration = song_duration
        db.commit()
        temp = song_get_by_id(db,id)
        return temp
    return False


###get all song details
def song_get_all(db: Session, skip,limit):
    user =  db.query(songs).filter(songs.is_delete == False).offset(skip).limit(limit).all()
    for i in range(0,len(user)):
        user[i].duration = str(user[i].duration)
        user[i].released_date = str(user[i].released_date)
        album_details = album_get_by_id(user[i].album_id,db)
        user[i].album_details = album_details
        print(user[i].album_id)
    return user


#get all song particular details 
def song_get_all_limit(db: Session, skip,limit):
    user = db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_id,albums.album_name,albums.music_director_name,albums.premium_status,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.is_delete == False).offset(skip).limit(limit).all()
    return user
    

###get particular song detail
def song_get_by_id(db: Session, song_id: int):
    db_song = db.query(songs).filter(songs.id == song_id,songs.is_delete == False).first() 
    if db_song:
        album_details = db.query(albums).filter(albums.id == db_song.album_id,albums.is_delete == False).first()
        artist_details = db.query(artist).filter(artist.id.in_(db_song.artist_id),artist.is_delete == False).all()
        db_song.duration = str(db_song.duration)
        db_song.released_date = str(db_song.released_date)
        db_song.album_details = album_details
        db_song.artist_details = artist_details
        return db_song
    else:
        return False


# ###get particular song particular detail
# def song_get_by_id_limit(db: Session, song_id: int):
#     return db.query().join(albums,albums.id == songs.album_id).filter(songs.id == song_id,songs.is_delete == False).all() 


###to update song details
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

###to delete single song detail by id
def delete_song_details(db: Session,song_id):
    user_temp = song_get_by_id(db,song_id)
    if user_temp:
        user_temp.is_delete = True
        db.commit()
        return True
    

####################SEARCH ENGINE########################
def search_engine(db,data):
    return db.query(songs.id,songs.song_name,songs.song_id,albums.album_name,albums.album_id,albums.music_director_name).join(albums,albums.id == songs.album_id).filter(songs.song_name.ilike(f'%{data}%')|albums.album_name.ilike(f'%{data}%')).all()


            