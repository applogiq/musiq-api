from sqlalchemy.orm import Session
from app.model.album_model import albums
from app.model.song_model import songs
from datetime import datetime
from fastapi.responses import StreamingResponse
from typing import BinaryIO,Optional
from fastapi import status,HTTPException,Request
import os
import shutil
import base64

from app.config.database import  SessionLocal 
from app.schema.song_schema import SongSchema
from app.model.album_model import albums

def song_new_detail(db:Session,song):
    # try:
    user_name =db.query(songs).filter(songs.song_name == song.song_name,songs.is_delete == 0).first()
    if user_name:
        if (user_name.artist_id["artist"])== (song.artist_id["artist"]):
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
        temp = db.query(albums).filter(albums.album_id == song.album_id,albums.is_delete == 0).first()
        num = temp.no_of_songs
        if temp.name[0].isalpha():
            alphabet = temp.name[0].upper()
        else:
            alphabet = "Mis"
        file_location = f"public/music/tamil/{alphabet}/{temp.name}/songs"
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
    # if song.image:
    #     pass
        # db.commit()
        # return  {'message': "decoded"},{"info": f"file '{filename1}' saved at '{file_location2}'"}
    db_user = songs(song_name =  song.song_name,
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
                    created_by = 1, 
                    updated_by = 0,
                    is_music = music)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True
    # except:
    #     return False







def song_detail(db: Session, song = SongSchema):
    user_name =db.query(songs).filter(songs.song_name == song.song_name,songs.is_delete == 0).first()
    if user_name:
        if (user_name.artist_id["artist"])== (song.artist_id["artist"]):
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
    db_user = songs(song_name =  song.song_name,
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
                    created_by = 1, 
                    updated_by = 0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True

def get_song(db: Session, song_id: int):
    # user = db.query(songs).filter(songs.id == song_id,songs.is_delete == 0).first()
    user = db.query(songs).filter(songs.id == song_id,songs.is_delete == 0).first()
    album_details = db.query(albums).filter(albums.album_id == user.album_id,albums.is_delete == 0).first()
    print(album_details,1111111)
    if user:
        user.duration = str(user.duration)
        user.released_date = str(user.released_date)
        user.album_details = album_details
        return user
    else:
        return False

def get_songs(db: Session, skip: int = 0, limit: int = 100):
    user =  db.query(songs).filter(songs.is_delete == 0).offset(skip).limit(limit).all()
    for i in range(0,len(user)):
        user[i].duration = str(user[i].duration)
        user[i].released_date = str(user[i].released_date)
        album_details = db.query(albums).filter(albums.album_id == user[i].album_id,albums.is_delete == 0).first()
        user[i].album_details = album_details
    return user


def song_update(db: Session,song_id: int,song):
    user_temp1 = db.query(songs).filter(songs.id == song_id,songs.is_delete == 0).first()
    if user_temp1:
        if song.song_name:
            songname =db.query(songs).filter(songs.song_name == song.song_name,songs.is_delete == 0).first()
            if songname:
                if (songname.artist_id["artist"])== (song.artist_id["artist"]):
                    raise HTTPException(status_code=400, detail="This song alreay exist")
                else:
                    pass
        user_temp1.song_name = song.song_name  
                    

        if song.artist_id["artist"]:
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
            temp = db.query(albums).filter(albums.album_id == user_temp1.album_id,albums.is_delete == 0).first()
            num = temp.no_of_songs
            if temp.name[0].isalpha():
                alphabet = temp.name[0].upper()
            else:
                alphabet = "Mis"
            file_location = f"public/music/tamil/{alphabet}/{temp.name}/songs"
            if os.path.exists(file_location):
                pass    
            else:
                os.makedirs(file_location)
            file_location2 = f"{file_location}/{filename1}"
            with open(file_location2, 'wb') as f:
                f.write(s)

            user_temp1.is_music = 1
     

        user_temp1.updated_at = datetime.now()
        user_temp1.updated_by = 1
        

        db.commit()

        return {'message': "data updated"}
    else:
        raise HTTPException(status_code=404, detail="song detail doesn't exist")
   

def upload_new_song_file(db: Session,song_id: int,uploaded_file):
    user_temp = db.query(songs).filter(songs.id == song_id,songs.is_delete == 0).first()
    if user_temp: 
        # user_temp2 = db.query(songs).filter(songs.id == song_id,songs.is_delete == 0,songs.is_music==1).first()
        # if user_temp2:
        #     raise HTTPException(status_code=400, detail="song is already uploaded for this id")
        # else:
        #     pass
     
        filename1 = user_temp.song_name +"."+"wav"

        temp = db.query(albums).filter(albums.album_id == user_temp.album_id,albums.is_delete == 0).first()
        if temp:
            name = temp.name
            s = temp.no_of_songs
            if name[0].isalpha():
                alphabet = name[0].upper()
            else:
                alphabet = "Mis"

            file_location = f"public/music/tamil/{alphabet}/{name}/songs"

            if os.path.exists(file_location):
                pass    
            else:
                os.makedirs(file_location)
            file_location2 = f"{file_location}/{filename1}"

            with open(file_location2, "wb+") as file_object:
                shutil.copyfileobj(uploaded_file.file, file_object)
            temp.no_of_songs = s+1        
        else:
            raise HTTPException(status_code=404, detail="Couldn't fetch album details.Check your album ID")

        user_temp.is_music = 1
        db.commit()
        return {"info": f"file '{filename1}' saved at '{file_location2}'"}
    else:
        raise HTTPException(status_code=404, detail="song details doesn't exist")


def upload_base64_song_file(db: Session,song_id: int,song):
    # user_temp = db.query(songs).filter(songs.id == song_id,songs.is_delete == 0,songs.is_music==1).first()
    # # if user_temp:
    # #     raise HTTPException(status_code=400, detail="song is already uploaded for this id")
    # # else:
    user = db.query(songs).filter(songs.id == song_id,songs.is_delete == 0).first()
    if user:
        s = base64.b64decode(song)
        filename1 = user.song_name +"."+"wav"
        temp = db.query(albums).filter(albums.album_id == user.album_id,albums.is_delete == 0).first()
        num = temp.no_of_songs
        if temp.name[0].isalpha():
            alphabet = temp.name[0].upper()
        else:
            alphabet = "Mis"
        file_location = f"public/music/tamil/{alphabet}/{temp.name}/songs"
        if os.path.exists(file_location):
            pass    
        else:
            os.makedirs(file_location)
        file_location2 = f"{file_location}/{filename1}"
        with open(file_location2, 'wb') as f:
            f.write(s)

        temp.no_of_songs = num+1
        user.is_music = 1
        db.commit()
        return  {'message': "decoded"},{"info": f"file '{filename1}' saved at '{file_location2}'"}
    else:
        raise HTTPException(status_code=404, detail="song details doesn't exist")

def delete_song_details(db: Session,song_id):
    user_temp = db.query(songs).filter(songs.id == song_id,songs.is_delete == 0).first()
    if user_temp:
        pass
    else:
        raise HTTPException(status_code=404, detail="song details doesn't exist")
    user_temp.is_delete = 1
    db.commit()
    return {"message":"Deleted"}


####### AUDIO STREAMING ########

def send_bytes_range_requests(
    file_obj: BinaryIO, start: int, end: int, chunk_size: int = 30_000 
):
    """Send a file in chunks using Range Requests specification RFC7233

    `start` and `end` parameters are inclusive due to specification
    """
    with file_obj as f:
        f.seek(start)
        while (pos := f.tell()) <= end:
            read_size = min(chunk_size, end + 1 - pos)
            yield f.read(read_size)


def _get_range_header(range_header: str, file_size: int) -> tuple[int, int]:
    def _invalid_range():
        return HTTPException(
            status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail=f"Invalid request range (Range:{range_header!r})",
        )

    try:
        h = range_header.replace("bytes=", "").split("-")
        start = int(h[0]) if h[0] != "" else 0
        end = int(h[1]) if h[1] != "" else file_size - 1
    except ValueError:
        raise _invalid_range()

    if start > end or start < 0 or end > file_size - 1:
        raise _invalid_range()
    return start, end


def range_requests_response(
    request: Request, file_path: str, content_type: str
):

    file_size = os.stat(file_path).st_size  
    range_header = request.headers.get("range")
    print(range_header)

    start = 100000
    end = file_size - 1
    status_code = status.HTTP_200_OK

    headers = {
        "content-type": content_type,
        "accept-ranges": "bytes",
        "content-encoding": "identity",
        "content-length": str(file_size - start),
        "access-control-expose-headers": (
            "content-type, accept-ranges, content-length, "
            "content-range, content-encoding"
        ),
    }
    

    if range_header is not None:
        start, end = _get_range_header(range_header, file_size)
        size = end - start + 1
        headers["content-length"] = str(size)
        headers["content-range"] = f"bytes {start}-{end}/{file_size }"
        status_code = status.HTTP_206_PARTIAL_CONTENT

    return StreamingResponse(
        send_bytes_range_requests(open(file_path, mode="rb"), start, end),
        headers=headers,
        status_code=status_code,
    )

####### AUDIO STREAMING ########