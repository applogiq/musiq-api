from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session

from app.schema.artist_schema import ArtistSchema
from app.auth.auth_bearer import JWTBearer
from app.controller.user_controller import get_db
from app.controller.artist_controller import artist_delete, artist_detail, artist_song, artist_update, delete_image, get_artist, get_artists, get_image,upload_art_image_file, upload_base64_art_file



router = APIRouter()

http_bearer = JWTBearer()

@router.post("/artist", tags=["artist"])
async def enter_artist_details(artists:ArtistSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): #,token: str = Depends(http_bearer)
    artist = artist_detail(db,artists)
    return artist

@router.post("/artist/image/{art_id}",tags=["artist"])
async def upload_img_file(art_id: str,uploaded_file: UploadFile = File(...),db: Session = Depends(get_db),token: str = Depends(http_bearer)): #,token: str = Depends(http_bearer)
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
        # return {"message": "couldn't fetch","success":False}
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

@router.get("/artist/{art_id}", tags=["artist"])
async def view_artist_details(art_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    artists = get_artist(db, art_id)
    if artists:
        return {"records": artists,"total_records" : 1,"sucess":True}
    else:
        # return {"message": "couldn't fetch,check your id","sucess":False}
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.get("/artist/songs/{art_id}", tags=["artist"])
async def view_artist_songs(art_id: str,db: Session = Depends(get_db)):#,token: str = Depends(http_bearer)
    artists = artist_song(db, art_id)
    if artists:
        # return artists
        return {"records": artists,"total_records" : len(artists),"sucess":True}
    else:
        # return {"message": "couldn't fetch,check your id","sucess":False}
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})
    
@router.put("/artist/{art_id}", tags=["artist"])
async def update_artist_details(art_id: int,artists: ArtistSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = artist_update(db,art_id,artists)
    return temp

@router.delete("/artist/{art_id}", tags=["artist"])
async def delete_artist_details(art_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = artist_delete(db,art_id)
    return temp

@router.get("/artist/image/{art_id}", tags=["artist"])
async def get_artist_iamge(art_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = get_image(db,art_id)
    return temp
# IMAGEDIR = "music/artist_images/"

# @router.get("/images/")
# async def read_random_file():
#     print(222222222222222222)

#     # get a random file from the image directory
#     files = os.listdir(IMAGEDIR)
#     random_index = randint(0, len(files) - 1)

#     path = f"{IMAGEDIR}{files[random_index]}"
#     print(path)
#     print(111111111111111111111111111111111)
    
#     # notice you can use FileResponse now because it expects a path
#     return FileResponse(path)

@router.delete("/artist/image/{art_id}", tags=["artist"])
async def remove_profile(art_id: int,db: Session = Depends(get_db)):
    user = delete_image(db,art_id)
    return user