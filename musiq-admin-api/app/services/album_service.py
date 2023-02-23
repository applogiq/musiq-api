from requests import Session
from fastapi import Depends,HTTPException
from datetime import datetime
import os,time
import base64

# from utils.auth_handler import create_access_token
from model.album_model import *
from config.database import *
from model.artist_model import *
from  services.admin_user_service import *

###get album details by id
def album_get_by_id(id,db):
    return db.query(albums).filter(albums.id == id,albums.is_delete==False).first()

###get all album details
def album_get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(albums).filter(albums.is_delete == False).offset(skip).limit(limit).all()

###check album name to avoid reptition
def albumname_check(albumname,db: Session):
    return db.query(albums).filter(albums.album_name == albumname,albums.is_delete==False).first()
    
###check whether album image is uploaded or not
def album_image_check(album_id,db: Session):
    return db.query(albums).filter(albums.id == album_id,albums.is_delete == False,albums.is_image == True).first()
    
###Enter new album details   
def album_create(db,album,email):
    album_length = len(db.query(albums).all())
    if album_length:
        b = album_length+1
    else:
        b = 1
    a = "AL00"+str(b)
    # a ="AL001"
    # while db.query(albums).filter(albums.album_id == a).first():
    #     a = "AL00" + str(int(a[-1])+1)
    if album.album_name[0].isalpha():
        alphabet = album.album_name[0].upper()
    else:
        alphabet = "Mis"

    path1 = f"{DIRECTORY}/music/tamil/{alphabet}/{album.album_name}"

    if os.path.exists(path1):
        pass
    else:
        os.makedirs(path1)
    
    if album.image:
        s = base64.b64decode(album.image)
        filename1 = a +".png"
        if album.album_name[0].isalpha():
            alphabet = album.album_name[0].upper()
        else:
            alphabet = "Mis"
        file_location = f"{DIRECTORY}/music/tamil/{alphabet}/{album.album_name}/image"
        if os.path.exists(file_location):
            pass    
        else:
            os.makedirs(file_location)
        file_location2 = f"{file_location}/{filename1}"
        with open(file_location2, 'wb') as f:
            f.write(s)
        image = True
    else:
        image = False

    temp = admin_get_email(email,db)   
    name =db.query(artist).filter(artist.id.in_(album.music_director)).all()
    artist_name = []
    for i in name:
        artist_name.append(i.artist_name)
        print(artist_name)

    db_album = albums(album_name = album.album_name,
                    album_id = a,
                    released_year = album.released_year,
                    music_director = album.music_director,
                    music_director_name = artist_name,
                    no_of_songs = 0,
                    premium_status = album.premium_status,
                    is_image = image,
                    is_delete = False,
                    created_by = temp.id,
                    is_active = 1)

    
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album


###update existing album details
def album_update(db: Session,album_id: int,album,email):
    user_temp1 = album_get_by_id(album_id,db)
    if user_temp1:
        if album.album_name:
            if albumname_check(album.album_name,db):
                raise HTTPException(status_code=400, detail="album is already register")
            else:
                if user_temp1.album_name[0].isalpha():
                    alphabet = user_temp1.album_name[0].upper()
                else:
                    alphabet = "Mis"
                if album.album_name[0].isalpha():
                    alphabet1 = album.album_name[0].upper()
                else:
                    alphabet1 = "Mis"
        
                source = f"{DIRECTORY}/music/tamil/{alphabet}/{user_temp1.album_name}"
                dest = f"{DIRECTORY}/music/tamil/{alphabet1}/{album.album_name}"

                if os.path.exists(source):
                    os.rename(source, dest)    
                else:
                    os.makedirs(dest)
                user_temp1.album_name = album.album_name
        else:
            pass

        if album.released_year:
            user_temp1.released_year = album.released_year
        
        if album.music_director:
            name =db.query(artist).filter(artist.id.in_(album.music_director)).all()
  
            artist_name = []
            for i in name:
                artist_name.append(i.artist_name)
                print(artist_name)
            user_temp1.music_director = album.music_director
            user_temp1.music_director_name = artist_name

        if album.image:
            s = base64.b64decode(album.image)
            filename1 =  user_temp1.album_id+".png"
            if album.album_name:
                if album.album_name[0].isalpha():
                    alphabet = album.album_name[0].upper()
                else:
                    alphabet = "Mis"
                name = album.album_name
            else:
                if user_temp1.album_name[0].isalpha():
                    alphabet = user_temp1.album_name[0].upper()
                else:
                    alphabet = "Mis"
                name = user_temp1.album_name

            file_location = f"{DIRECTORY}/music/tamil/{alphabet}/{name}/image"
            if os.path.exists(file_location):
                pass    
            else:
                os.makedirs(file_location)
            file_location2 = f"{file_location}/{filename1}"
            with open(file_location2, 'wb') as f:
                f.write(s)
            user_temp1.is_image = True
        
        if album.premium_status:
            user_temp1.premium_status = album.premium_status

        temp = admin_get_email(email,db)
        user_temp1.updated_at = datetime.now()
        user_temp1.updated_by = temp.id

        
        db.commit()
        temp1 = album_get_by_id(album_id,db)
        return temp1
    return False


###remove album image by it's id
def album_image_delete(db: Session,album_id: int):
    user_temp = album_image_check(album_id,db)
    if user_temp:
        if user_temp:
            if user_temp.album_name[0].isalpha():
                alphabet = user_temp.album_name[0].upper()
            else:
                alphabet = "Mis" 
        user_temp.is_image = False

        path =f"{DIRECTORY}/music/tamil/{alphabet}/{user_temp.album_name}/image/{user_temp.album_id}.png"
        os.remove(path)
        db.commit()
        return True
    return False

    
    

    

    
   