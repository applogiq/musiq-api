from requests import Session

from model.song_model import *
from config.database import *
from model.album_model import *
from services.album_service import *

###to get trending hits detail
def trending_hits(db,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_id,albums.album_name,albums.music_director_name,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.is_delete == False).order_by(songs.listeners.desc()).limit(limit).all()

###to get new release detail
def new_release(db,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_id,albums.album_name,albums.music_director_name,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.is_delete == False).order_by(songs.released_date.desc()).limit(limit).all()

###to check whether song name already used
def song_album_check(db,album_id,skip,limit):
    user = db.query(songs).filter(songs.album_id == album_id,songs.is_delete == False).offset(skip).limit(limit).all()
    for i in range(0,len(user)):
        user[i].duration = str(user[i].duration)
        user[i].released_date = str(user[i].released_date)
        album_details = album_get_by_id(user[i].album_id,db)
        user[i].album_details = album_details
        print(user[i].album_id)
    return user

###to fetch particular song details for particular album
def song_album_check_limit(db,album_id,skip,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_id,albums.album_name,albums.music_director_name,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.album_id == album_id,songs.is_delete == False).offset(skip).limit(limit).all()

###to fetch song details for particular artist
def song_artist_check(db,artist_id,skip,limit):
    user = db.query(songs).filter(songs.artist_id.contains([artist_id]),songs.is_delete == False).offset(skip).limit(limit).all()
    for i in range(0,len(user)):
        user[i].duration = str(user[i].duration)
        user[i].released_date = str(user[i].released_date)
        album_details = album_get_by_id(user[i].album_id,db)
        user[i].album_details = album_details
        print(user[i].album_id)
    return user

###to fetch particular song details for particular artist
def song_artist_check_limit(db,artist_id,skip,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_id,albums.album_name,albums.music_director_name,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.artist_id.contains([artist_id]),songs.is_delete == False).offset(skip).limit(limit).all()

###to check music is available for this id
def song_music_check(db,song_id):
    return  db.query(songs).filter(songs.id == song_id,songs.is_delete == False,songs.is_music == True).first()

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
    user = db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,albums.album_id,albums.album_name,albums.music_director_name,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.is_delete == False).offset(skip).limit(limit).all()
    return user

###get particular song detail
def song_get_by_id(db: Session, song_id: int):
    user = db.query(songs).filter(songs.id == song_id,songs.is_delete == False).first() 
    # print(album_details,1111111)
    if user:
        album_details = db.query(albums).filter(albums.id == user.album_id,albums.is_delete == False).first()
        user.duration = str(user.duration)
        user.released_date = str(user.released_date)
        user.album_details = album_details
        return user
    else:
        return False

####################SEARCH ENGINE########################
def search_engine(db,data):
    return db.query(songs.id,songs.song_name,songs.song_id,albums.album_name,albums.album_id,albums.music_director_name).join(albums,albums.id == songs.album_id).filter(songs.song_name.ilike(f'%{data}%')|albums.album_name.ilike(f'%{data}%')).all()