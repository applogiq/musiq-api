from requests import Session
from fastapi import Depends,HTTPException
from datetime import datetime
import os,time
import base64


# from utils.auth_handler import create_access_token
from model.song_model import *
from config.database import *
from model.album_model import *
from services.album_service import *

def song_album_check(db,album_id,skip,limit):
    user = db.query(songs).filter(songs.album_id == album_id,songs.is_delete == False).offset(skip).limit(limit).all()
    for i in range(0,len(user)):
        user[i].duration = str(user[i].duration)
        user[i].released_date = str(user[i].released_date)
        album_details = album_get_by_id(user[i].album_id,db)
        user[i].album_details = album_details
        print(user[i].album_id)
    return user

def song_artist_check(db,artist_id,skip,limit):
    user = db.query(songs).filter(songs.artist_id.contains([artist_id]),songs.is_delete == False).offset(skip).limit(limit).all()
    for i in range(0,len(user)):
        user[i].duration = str(user[i].duration)
        user[i].released_date = str(user[i].released_date)
        album_details = album_get_by_id(user[i].album_id,db)
        user[i].album_details = album_details
        print(user[i].album_id)
    return user


def song_music_check(db,song_id):
    return  db.query(songs).filter(songs.id == song_id,songs.is_delete == False,songs.is_music == True).first()


def song_get_all(db: Session, skip,limit):
    user =  db.query(songs).filter(songs.is_delete == False).offset(skip).limit(limit).all()
    for i in range(0,len(user)):
        user[i].duration = str(user[i].duration)
        user[i].released_date = str(user[i].released_date)
        album_details = album_get_by_id(user[i].album_id,db)
        user[i].album_details = album_details
        print(user[i].album_id)
    return user

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