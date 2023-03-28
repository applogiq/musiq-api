from requests import Session

from model.song_model import *
from config.database import *
from model.album_model import *
from services.album_service import *

###to get trending hits detail
def trending_hits(db,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,songs.duration,albums.album_id,albums.album_name,albums.music_director_name,albums.premium_status,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.is_delete == False).order_by(songs.listeners.desc()).limit(limit).all()

###to get new release detail
def new_release(db,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,songs.duration,albums.album_id,albums.album_name,albums.music_director_name,albums.premium_status,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.is_delete == False).order_by(songs.released_date.desc()).limit(limit).all()

###to check whether song name already used
def song_album_check(db,album_id,skip,limit):
    user = db.query(songs).filter(songs.album_id == album_id,songs.is_delete == False).offset(skip).limit(limit).all()
    for i in range(0,len(user)):
        user[i].duration = str(user[i].duration)
        user[i].released_date = str(user[i].released_date)
        album_details = album_get_by_id(user[i].album_id,db)
        user[i].album_details = album_details
    return user

###to fetch particular song details for particular album
def song_album_check_limit(db,album_id,skip,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,songs.duration,albums.album_id,albums.album_name,albums.music_director_name,albums.premium_status,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.album_id == album_id,songs.is_delete == False).offset(skip).limit(limit).all()

###to fetch song details for particular artist
def song_artist_check(db,artist_id,skip,limit):
    user = db.query(songs).filter(songs.artist_id.contains([artist_id]),songs.is_delete == False).offset(skip).limit(limit).all()
    for i in range(0,len(user)):
        user[i].duration = str(user[i].duration)
        user[i].released_date = str(user[i].released_date)
        album_details = album_get_by_id(user[i].album_id,db)
        user[i].album_details = album_details
    return user

###to fetch particular song details for particular artist
def song_artist_check_limit(db,artist_id,skip,limit):
    return db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,songs.duration,albums.album_id,albums.album_name,albums.music_director_name,albums.premium_status,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.artist_id.contains([artist_id]),songs.is_delete == False).offset(skip).limit(limit).all()

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
    return user

#get all song particular details 
def song_get_all_limit(db: Session, skip,limit):
    user = db.query(songs.id,songs.song_name,songs.lyrics,songs.is_music,songs.artist_id,songs.duration,albums.album_id,albums.album_name,albums.music_director_name,albums.premium_status,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.is_delete == False).offset(skip).limit(limit).all()
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

####################SEARCH ENGINE########################
def search_engine(db,data):
    return db.query(songs.id,songs.song_name,songs.song_id,songs.duration,albums.album_name,albums.album_id,albums.premium_status,albums.music_director_name,albums.is_image).join(albums,albums.id == songs.album_id).filter(songs.song_name.ilike(f'%{data}%')|albums.album_name.ilike(f'%{data}%'),songs.is_delete == False).all()