from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException,Query
from pydantic import Required
from typing import Union
from sqlalchemy.orm import Session

from app.schema.artist_schema import ArtistSchema
from app.auth.auth_bearer import JWTBearer
from app.controller.user_controller import get_db
from app.controller.artist_controller import artist_delete, artist_detail, artist_song, artist_update, delete_image, get_artist, get_artists, get_image,upload_art_image_file, upload_base64_art_file



router = APIRouter()

http_bearer = JWTBearer()

@router.post("/artist", tags=["artist"])
async def enter_artist_details(artists:ArtistSchema,keyword: str = Query(default=Required, min_length=3, max_length=3),db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    artist = artist_detail(db,artists,keyword)
    return artist

@router.post("/artist/image/{art_id}",tags=["artist"])
async def upload_img_file(art_id: str,uploaded_file: UploadFile = File(...),db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    artist = upload_art_image_file(db,art_id,uploaded_file)
    return artist

@router.post("/artist/image-base64/{artist_id}",tags=["artist"])
async def upload_b64_img_file(artist_id: str,img: str = Body(...) ,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = upload_base64_art_file(db,artist_id,img)
    return temp

@router.get("/artist", tags=["artist"])
async def view_all_artist_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    try:
        users = get_artists(db)
        return {"records": users,"total_records" : len(users),"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

@router.get("/artist/{art_id}", tags=["artist"])
async def view_artist_details(art_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    artists = get_artist(db, art_id)
    if artists:
        return {"records": artists,"total_records" : 1,"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.get("/artist/songs/{art_id}", tags=["artist"])
async def view_artist_songs(art_id: str,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    artists = artist_song(db, art_id)
    if artists:
        return {"records": artists,"total_records" : len(artists),"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.get("/artist/image/{art_id}", tags=["artist"])
async def get_artist_iamge(art_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = get_image(db,art_id)
    return temp
    
@router.put("/artist/{art_id}", tags=["artist"])
async def update_artist_details(art_id: int,artists: ArtistSchema,keyword: Union[str, None] = Query(default=None, fixed_length=3),db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = artist_update(db,art_id,artists,keyword)
    return temp

@router.delete("/artist/{art_id}", tags=["artist"])
async def delete_artist_details(art_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = artist_delete(db,art_id)
    return temp

@router.delete("/artist/image/{art_id}", tags=["artist"])
async def remove_image(art_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    user = delete_image(db,art_id)
    return user