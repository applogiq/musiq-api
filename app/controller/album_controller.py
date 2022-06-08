from sqlalchemy.orm import Session
from datetime import datetime
import os
import shutil
import base64
from fastapi import HTTPException

from app.model.song_model import songs
from app.model.album_model import albums

def album_new_detail(db: Session,album,keyword):
    albumname =db.query(albums).filter(albums.name == album.name,albums.is_delete == 0).first()
    a ="AL00"
    if albumname:
        raise HTTPException(status_code=400, detail="Album is already register")

    while db.query(albums).filter(albums.album_id == a + keyword.upper(),albums.is_delete == 0).first():
        a = "AL0" + str(int(a[-1])+1)
    
    if album.name[0].isalpha():
        alphabet = album.name[0].upper()
    else:
        alphabet = "Mis"

    path1 = f"public/music/tamil/{alphabet}/{album.name}"

    if os.path.exists(path1):
        pass
    else:
        os.makedirs(path1)
    
    if album.image:
        s = base64.b64decode(album.image)
        filename1 = a+keyword.upper() +".png"
        if album.name[0].isalpha():
            alphabet = album.name[0].upper()
        else:
            alphabet = "Mis"
        file_location = f"public/music/tamil/{alphabet}/{album.name}/image"
        if os.path.exists(file_location):
            pass    
        else:
            os.makedirs(file_location)
        file_location2 = f"{file_location}/{filename1}"
        with open(file_location2, 'wb') as f:
            f.write(s)
        image = 1
    else:
        image = 0
       
        
    db_album = albums(name = album.name,
                    album_id = a+keyword.upper(),
                    released_year = album.released_year,
                    music_director = album.music_director,
                    no_of_songs = 0,
                    is_image = image,
                    is_delete = 0,
                    created_by = 1,
                    updated_by = 0,
                    is_active = 1)

    

    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return {"message":"data added"}

# def album_detail(db: Session,album,keyword):
#     albumname =db.query(albums).filter(albums.name == album.name,albums.is_delete == 0).first()
#     a ="AL00"
#     if albumname:
#         raise HTTPException(status_code=400, detail="Album is already register")

#     while db.query(albums).filter(albums.album_id == a + keyword.upper(),albums.is_delete == 0).first():
#         a = "AL0" + str(int(a[-1])+1)

        
#     db_album = albums(name = album.name,
#                     album_id = a+keyword.upper(),
#                     released_year = album.released_year,
#                     music_director = album.music_director,
#                     no_of_songs = 0,
#                     is_delete = 0,
#                     created_by = 1,
#                     updated_by = 0,
#                     is_active = 1)

#     if album.name[0].isalpha():
#         alphabet = album.name[0].upper()
#     else:
#         alphabet = "Mis"

#     path1 = f"public/music/tamil/{alphabet}/{album.name}"

#     if os.path.exists(path1):
#         pass
#     else:
#         os.makedirs(path1)

#     db.add(db_album)
#     db.commit()
#     db.refresh(db_album)
#     return {"message":"data added"}


def get_albums(db: Session):
    return db.query(albums).filter(albums.is_delete == 0).all()

def get_album(db: Session, album_id: int):
    temp = db.query(albums).filter(albums.id == album_id,albums.is_delete == 0).first()
    if temp:
        return temp
    else:
        return False

def album_update(db: Session,album_id: int,album,keyword):
    user_temp1 = db.query(albums).filter(albums.id == album_id,albums.is_delete == 0).first()
    if user_temp1:
        pass
    else:
        raise HTTPException(status_code=404, detail="album detail doesn't exist")

    if album.name:
        if user_temp1.name[0].isalpha():
            alphabet = user_temp1.name[0].upper()
        else:
            alphabet = "Mis"
        if album.name[0].isalpha():
            alphabet1 = album.name[0].upper()
        else:
            alphabet1 = "Mis"
   
        source = f"public/music/tamil/{alphabet}/{user_temp1.name}"
        dest = f"public/music/tamil/{alphabet1}/{album.name}"

        if os.path.exists(source):
            os.rename(source, dest)    
        else:
            os.makedirs(dest)

        temp = db.query(albums).filter(albums.id == album_id,albums.is_delete == 0,albums.is_image==1).first()
        if temp:
            demo = f"public/music/tamil/{alphabet1}/{album.name}/image/{user_temp1.name}.png"
            dest1 = f"public/music/tamil/{alphabet1}/{album.name}/image/{album.name}.png"
            if os.path.exists(demo):
                os.rename(demo,dest1)
            else:
                return False
        else:
            pass
        tempname = db.query(albums).filter(albums.name ==album.name,albums.is_delete == 0).first()
        if tempname:
            raise HTTPException(status_code=400, detail="album is already register")
        else:
            user_temp1.name = album.name

    if keyword:
        a ="AL00"
        while db.query(albums).filter(albums.album_id == a + keyword.upper(),albums.is_delete == 0).first():
            a = "AL0" + str(int(a[-1])+1)
      
        temp2 = db.query(songs).filter(songs.album_id == user_temp1.album_id,songs.is_delete == 0,songs.is_music==1).first()  
        if temp2:
            # for i in range(0,len(temp2)):
            temp2.album_id = a +keyword.upper()
        else:
            pass
        user_temp1.album_id = a +keyword.upper()
    
    if album.released_year:
        user_temp1.released_year = album.released_year
    
    if album.music_director:
        user_temp1.music_director = album.music_director

    if album.image:
        s = base64.b64decode(album.image)
        filename1 = a+keyword.upper() +".png"
        if album.name[0].isalpha():
            alphabet = album.name[0].upper()
        else:
            alphabet = "Mis"
        file_location = f"public/music/tamil/{alphabet}/{album.name}/image"
        if os.path.exists(file_location):
            pass    
        else:
            os.makedirs(file_location)
        file_location2 = f"{file_location}/{filename1}"
        with open(file_location2, 'wb') as f:
            f.write(s)



    user_temp1.is_active = 1 
    user_temp1.is_delete = 0
    user_temp1.created_by = 1
    user_temp1.updated_at = datetime.now()
    user_temp1.updated_by = 1

    db.commit()

    return {'message': "data updated"}

def album_delete(db: Session,album_id):
    temp = db.query(albums).filter(albums.id == album_id,albums.is_delete == 0).first()
    if temp:
        pass
    else:
        raise HTTPException(status_code=404, detail="album details doesn't exist")
    temp.is_delete = 1
    db.commit()
    return {"message":"Deleted"}

def upload_new_image_file(db: Session,album_id: int,uploaded_file):
    user_temp = db.query(albums).filter(albums.id == album_id,albums.is_delete == 0).first()
    if user_temp:
        filename1 = user_temp.name +"."+"png"
        if user_temp.name[0].isalpha():
            alphabet = user_temp.name[0].upper()
        else:
            alphabet = "Mis"
        file_location = f"public/music/tamil/{alphabet}/{user_temp.name}/image"
        if os.path.exists(file_location):
            pass    
        else:
            os.makedirs(file_location)
        file_location2 = f"{file_location}/{filename1}"
        with open(file_location2, "wb+") as file_object:
            shutil.copyfileobj(uploaded_file.file, file_object)  

        user_temp.is_image = 1
        db.commit()
        return {"info": f"file '{filename1}' saved at '{file_location2}'"}
    else:
        raise HTTPException(status_code=404, detail="album details doesn't exist")

def upload_base64_image_file(db: Session,album_id: int,img):
    user_temp = db.query(albums).filter(albums.id == album_id,albums.is_delete == 0).first()
    if user_temp:
        s = base64.b64decode(img)
        filename1 = user_temp.name +"."+"png"
        if user_temp.name[0].isalpha():
            alphabet = user_temp.name[0].upper()
        else:
            alphabet = "Mis"
        file_location = f"public/music/tamil/{alphabet}/{user_temp.name}/image"
        if os.path.exists(file_location):
            pass    
        else:
            os.makedirs(file_location)
        file_location2 = f"{file_location}/{filename1}"
        with open(file_location2, 'wb') as f:
            f.write(s)

        user_temp.is_image = 1
        db.commit()
        return  {'message': "decoded"},{"info": f"file '{filename1}' saved at '{file_location2}'"}
    else:
        raise HTTPException(status_code=404, detail="album details doesn't exist")


def get_album_image(db: Session,album_id):
    temp = db.query(albums).filter(albums.id == album_id,albums.is_delete == 0,albums.is_image == 1).first()
    if temp:
        user_temp = db.query(albums).filter(albums.id == album_id,albums.is_delete == 0,albums.is_image == 1).first()
        if user_temp:
            if user_temp.name[0].isalpha():
                alphabet = user_temp.name[0].upper()
            else:
                alphabet = "Mis" 
            file_location = f"public/music/tamil/{alphabet}/{user_temp.name}/image/{user_temp.name}.png"
            link = f"http://127.0.0.1:8000/{file_location}"
            return link
        else:
            raise HTTPException(status_code=404, detail="Image doesn't exist for this id")
    else:
        raise HTTPException(status_code=404, detail="check your id")


def delete_album_image(db: Session,album_id: int):
    user_temp = db.query(albums).filter(albums.id == album_id,albums.is_delete == 0,albums.is_image == 1).first()
    if user_temp:
        if user_temp:
            if user_temp.name[0].isalpha():
                alphabet = user_temp.name[0].upper()
            else:
                alphabet = "Mis" 
        user_temp.is_image = 0

        path =f"public/music/tamil/{alphabet}/{user_temp.name}/image/{user_temp.name}.png"
        os.remove(path)
        db.commit()
        return {'message': "album image removed"}
    else:
        return {'message': "Check your id"}