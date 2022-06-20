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

def album_get_by_id(id,db):
    return db.query(albums).filter(albums.id == id,albums.is_delete==False).first()

def album_get_all(db: Session, skip: int = 0, limit: int = 100):
    user = db.query(albums).filter(albums.is_delete == False).offset(skip).limit(limit).all()
    if user:
        return user
    else:
        return False


def albumname_check(albumname,db: Session):
    user = db.query(albums).filter(albums.name == albumname,albums.is_delete==False).first()
    return user

def album_image_check(album_id,db: Session):
    user= db.query(albums).filter(albums.id == album_id,albums.is_delete == False,albums.is_image == True).first()
    return user
    
def album_create(db,album,email):
        a ="AL001"
        while db.query(albums).filter(albums.album_id == a).first():
            a = "AL00" + str(int(a[-1])+1)
        
        if album.name[0].isalpha():
            alphabet = album.name[0].upper()
        else:
            alphabet = "Mis"

        path1 = f"{DIRECTORY}/music/tamil/{alphabet}/{album.name}"

        if os.path.exists(path1):
            pass
        else:
            os.makedirs(path1)
        
        if album.image:
            s = base64.b64decode(album.image)
            filename1 = a +".png"
            if album.name[0].isalpha():
                alphabet = album.name[0].upper()
            else:
                alphabet = "Mis"
            file_location = f"{DIRECTORY}/music/tamil/{alphabet}/{album.name}/image"
            if os.path.exists(file_location):
                pass    
            else:
                os.makedirs(file_location)
                # print(111111111111111)
            file_location2 = f"{file_location}/{filename1}"
            with open(file_location2, 'wb') as f:
                f.write(s)
            image = True
        else:
            image = False

        temp = admin_get_email(email,db)   
        name =db.query(artist).filter(artist.id.in_(album.music_director)).all()
        # print(temp4[0].name)
        artist_name = []
        for i in name:
            artist_name.append(i.name)
            print(artist_name)

        db_album = albums(name = album.name,
                        album_id = a,
                        released_year = album.released_year,
                        music_director = album.music_director,
                        music_director_name = artist_name,
                        no_of_songs = 0,
                        is_image = image,
                        is_delete = False,
                        created_by = temp.id,
                        is_active = 1)

        
        db.add(db_album)
        db.commit()
        db.refresh(db_album)
        return db_album

def album_update(db: Session,album_id: int,album,email):
    user_temp1 = album_get_by_id(album_id,db)
    if user_temp1:
        if album.name:
            if albumname_check(album.name,db):
                raise HTTPException(status_code=400, detail="album is already register")
            else:
                if user_temp1.name[0].isalpha():
                    alphabet = user_temp1.name[0].upper()
                else:
                    alphabet = "Mis"
                if album.name[0].isalpha():
                    alphabet1 = album.name[0].upper()
                else:
                    alphabet1 = "Mis"
        
                source = f"{DIRECTORY}/music/tamil/{alphabet}/{user_temp1.name}"
                dest = f"{DIRECTORY}/music/tamil/{alphabet1}/{album.name}"

                if os.path.exists(source):
                    os.rename(source, dest)    
                else:
                    os.makedirs(dest)
                user_temp1.name = album.name
        else:
            pass

        if album.released_year:
            user_temp1.released_year = album.released_year
        
        if album.music_director:
            name =db.query(artist).filter(artist.id.in_(album.music_director)).all()
  
            artist_name = []
            for i in name:
                artist_name.append(i.name)
                print(artist_name)
            user_temp1.music_director = album.music_director
            user_temp1.music_director_name = artist_name

        if album.image:
            s = base64.b64decode(album.image)
            filename1 =  user_temp1.album_id+".png"
            if album.name:
                if album.name[0].isalpha():
                    alphabet = album.name[0].upper()
                else:
                    alphabet = "Mis"
                name = album.name
            else:
                if user_temp1.name[0].isalpha():
                    alphabet = user_temp1.name[0].upper()
                else:
                    alphabet = "Mis"
                name = user_temp1.name

            file_location = f"{DIRECTORY}/music/tamil/{alphabet}/{name}/image"
            if os.path.exists(file_location):
                pass    
            else:
                os.makedirs(file_location)
            file_location2 = f"{file_location}/{filename1}"
            with open(file_location2, 'wb') as f:
                f.write(s)
            user_temp1.is_image = True

        temp = admin_get_email(email,db)
        user_temp1.updated_at = datetime.now()
        user_temp1.updated_by = temp.id

        
        db.commit()
        temp1 = album_get_by_id(album_id,db)
        print(temp1)
        return {"status": True,"message":"Updated Successfully","records":temp1}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message":"check your id..album doesn't exist"})

def delete_album_image(db: Session,album_id: int):
    user_temp = album_image_check(album_id,db)
    if user_temp:
        if user_temp:
            if user_temp.name[0].isalpha():
                alphabet = user_temp.name[0].upper()
            else:
                alphabet = "Mis" 
        user_temp.is_image = False

        path =f"{DIRECTORY}/music/tamil/{alphabet}/{user_temp.name}/image/{user_temp.album_id}.png"
        os.remove(path)
        db.commit()
        return {"status": True,"message":"album image removed"}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message":"check your id..Image doesn't exist"})
    
    

    

    
   