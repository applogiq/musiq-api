from fastapi import HTTPException
import re
from typing import BinaryIO,Optional
from fastapi import status,HTTPException,Request
from fastapi.responses import StreamingResponse

from services.song_service import *
from services.album_service import *

###response of recent trending songs
def get_trending_hits(db,limit):
    db_song = trending_hits(db,limit)
    if db_song:
        return {"success":True,"message":"song details fetched successfully","records": db_song,"totalrecords" : len(db_song)}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch,check your id"})

###response of new release songs details
def get_new_release(db,limit):
    db_song = new_release(db,limit)
    if db_song:
        return {"success":True,"message":"song details fetched successfully","records": db_song,"totalrecords" : len(db_song)}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch,check your id"})


###response after entering new song detail
def enter_new_song_detail(db,song,email):
    db_song = song_new_detail(db,song,email)
    if db_song:
        return {"success":True,'message': "song details added","records": db_song}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "check your details"})


###response after entering new song detail with base64
def enter_song_detail(db,song,email):
    db_song = song_detail(db,song,email)
    if db_song:
        return {"success":True,'message': "song details added","records": db_song}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "check your details"})

###get single song details response
def get_song_by_id(db, song_id):
    db_song = song_get_by_id(db, song_id)
    if db_song:
        return {"success":True,"message":"Song details fetched successfully","records": db_song,"totalrecords" : 1}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch,check your id"})
    
###response of album based songs
def album_song_check(db,album_id,skip,limit):
    db_song = song_album_check_limit(db,album_id,skip,limit)
    if db_song:
        return {"success":True,"message":"Song details fetched successfully","records": db_song,"totalrecords" : len(db_song)}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch,check your id"})

###response of artist based songs
def artist_song_check(db,artist_id,skip,limit):
    db_song = song_artist_check_limit(db,artist_id,skip,limit)
    if db_song:
        return {"success":True,"message":"Song details fetched successfully","records": db_song,"totalrecords" : len(db_song)}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch,check your id"})

###all song details response
def get_all_song(db, skip,limit):
    db_song = song_get_all_limit(db, skip,limit)
    if db_song:
        return {"success":True,"message":"song details fetched successfully","records": db_song,"totalrecords" : len(db_song)}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch,check your id"})

##response of updating song detail
def update_song(db,song_id,song,email):
    db_song = song_update(db,song_id,song,email)
    if db_song:
        return {"status": True,"message":"updated Successfully","records":db_song}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "song details doesn't exist"})

###upload music as file response
def music_upload_details(db,id,file):
    db_song = music_upload(db,id,file)
    if db_song:
        return {"status": True,"message":"updated Successfully","records":db_song}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "song details doesn't exist"})

###delete entire song details reponses
def song_delete(db: Session,song_id):
    db_song = delete_song_details(db,song_id)
    if db_song:
        return {"success": True,"message":"song deleted"}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "song details doesn't exist"})





####response of search engine
def search_engine_details(db,data):
    db_song = search_engine(db,data)
    if db_song:
        return {"success":True,"message":"Song details fetched successfully","records": db_song,"totalrecords" : len(db_song)}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch"})

###music streaming response
def song_response(db,id,request):
    user_temp = song_music_check(db,id)
    if user_temp:
        temp = album_get_by_id(user_temp.album_id,db)
        if temp.album_name[0].isalpha():
            alphabet = temp.album_name[0].upper()
        else:
            alphabet = "Mis" 
        file_location = f"{DIRECTORY}/music/tamil/{alphabet}/{temp.album_name}/songs/{user_temp.song_id}.mp3"
        return range_requests_response(
            request, file_path=file_location, content_type="audio/mp3" 
        )
    else:
        raise HTTPException(status_code=404, detail={"success": False,"message":"music doesn't exist for this id"})

        
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
