from sqlalchemy.orm import Session
from datetime import datetime
from app.model.artist_model import artist
import shutil
import base64
from fastapi import HTTPException
import os
from app.model.song_model import songs

def artist_detail(db: Session,artists):
    artistname =db.query(artist).filter(artist.name == artists.name,artist.is_delete == 0).first()
    a ="AR00"
    if artistname:
        # return ("Artist is already register")
        raise HTTPException(status_code=400, detail="Artist is already register")
    while db.query(artist).filter(artist.artist_id == a + artists.name[0:3].upper(),artist.is_delete == 0).first():
        # return(True)
        a = "AR0" + str(int(a[-1])+1)
    db_user = artist(name = artists.name,
                    artist_id = a+artists.name[0:3].upper(),
                    is_image = 0,
                    is_delete = 0,
                    created_by = 1,
                    updated_by = 0,
                    is_active = 1)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message":"data added"}

def upload_art_image_file(db: Session,art_id: int,uploaded_file):
    user_temp = db.query(artist).filter(artist.id == art_id,artist.is_delete == 0).first()
    if user_temp: 
        filename1 = user_temp.artist_id+".png"
        file_location = f"song/artists/{filename1}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(uploaded_file.file, file_object)  

        user_temp.is_image = 1
        db.commit()
        return {"info": f"file '{filename1}' saved at '{file_location}'"}
    else:
        raise HTTPException(status_code=404, detail="artist details doesn't exist")

def upload_base64_art_file(db: Session,artist_id: int,img):
    user = db.query(artist).filter(artist.id == artist_id,artist.is_delete == 0).first()
    if user:
        s = base64.b64decode(img)
        filename1 = user.artist_id+".png"
        file_location = f"song/artists/{filename1}"
        with open(file_location, "wb+") as f:
            f.write(s)  

        user.is_image = 1
        db.commit()
        return {"info": f"file '{filename1}' saved at '{file_location}'"}
    else:
        #  return {'message': "song details doesn't exist"},{"info": "check your details"}
        raise HTTPException(status_code=404, detail="artist details doesn't exist")


def get_artists(db: Session):
    return db.query(artist).filter(artist.is_delete == 0).all()

def get_artist(db: Session, art_id: int):
    artists = db.query(artist).filter(artist.id == art_id,artist.is_delete == 0).first()
    if artists:
        return artists
    else:
        return False

def artist_song(db: Session, art_id: int):
    song = db.query(songs).filter(songs.is_delete == 0).all()
    try:
        s = []
        for i in range(0,len(song)):
            print(i)
            if art_id in song[i].artist_id["artist"]:
                s.append(song[i])
        return s
    except:
        raise HTTPException(status_code=404, detail="artist detail doesn't exist")
            # artists = db.query(songs).filter(songs[i].artist_id["artist"] == art_id,songs.is_delete == 0).first()
        # return artist

def artist_update(db: Session,art_id: int,artists):
    user_temp1 = db.query(artist).filter(artist.id == art_id,artist.is_delete == 0).first()
    if user_temp1:
        pass
    else:
        # return {"message":"artist detail doesn't exist"}
        raise HTTPException(status_code=404, detail="artist detail doesn't exist")

    if artists.name:
        a ="AR00"
       
        a = "AR0" + str(int(a[-1])+1)
        tempname = db.query(artist).filter(artist.name ==artists.name,artist.is_delete == 0).first()
        if tempname:
            # return ("Artist is already register")
            raise HTTPException(status_code=400, detail="Artist is already register")
        else:
            user_temp1.name = artists.name
            if db.query(artist).filter(artist.artist_id == a + artists.name[0:3].upper(),artist.is_delete == 0).first():
                a = "AR0" + str(int(a[-1])+1)
                user_temp1.artist_id = a + artists.name[0:3].upper()
            else: 
                user_temp1.artist_id = a +artists.name[0:3].upper()
    user_temp1.is_active = 1 
    user_temp1.is_delete = 0
    user_temp1.created_by = 1
    user_temp1.updated_at = datetime.now()
    user_temp1.updated_by = 1

    db.commit()

    return {'message': "data updated"}

def artist_delete(db: Session,art_id):
    user_temp = db.query(artist).filter(artist.id == art_id,artist.is_delete == 0).first()
    if user_temp:
        pass
    else:
        # return {"message":"artist details doesn't exist"}
        raise HTTPException(status_code=404, detail="artist details doesn't exist")
    user_temp.is_delete = 1
    db.commit()
    return {"message":"Deleted"}

def get_image(db: Session,art_id):
    temp = db.query(artist).filter(artist.id == art_id,artist.is_delete == 0).first()
    if temp:
        user_temp = db.query(artist).filter(artist.id == art_id,artist.is_delete == 0,artist.is_image == 1).first()
        if user_temp:
            # filename = f"music/artist_images/{user_temp.artist_id}.png"
            # print(filename)
            link = f"http://127.0.0.1:8000/song/artists/{user_temp.artist_id}.png"
            return link
        else:
            # return {"message":"Image doesn't exist for this id"}
            raise HTTPException(status_code=404, detail="Image doesn't exist for this id")
    else:
        raise HTTPException(status_code=404, detail="check your id")

def delete_image(db: Session,art_id: int):
    user_temp = db.query(artist).filter(artist.id == art_id,artist.is_delete == 0,artist.is_image == 1).first()
    if user_temp:
        user_temp.is_image = 0

        file = user_temp.artist_id+".png"
        path = f"song/artists/{file}"
        os.remove(path)
        db.commit()
        return {'message': "artist image removed"}
    else:
        return {'message': "Check your id"}
