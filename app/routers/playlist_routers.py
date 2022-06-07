from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session

from app.auth.auth_bearer import JWTBearer
from app.controller.playlist_controller import get_playlist, get_playlists, playlist_delete, playlist_detail, playlist_update
from app.controller.user_controller import get_db
from app.schema.playlist_schema import PlaylistSchema


router = APIRouter(tags=["playlist"],prefix='/playlist')

http_bearer = JWTBearer()

@router.post("/")
async def enter_playlist_details(playlists:PlaylistSchema,db: Session = Depends(get_db)): 
    # pass
    playlist = playlist_detail(db,playlists)
    return playlist

@router.get("/")
async def view_all_playlist_details(db: Session = Depends(get_db)):#,token: str = Depends(http_bearer)
    try:
        users = get_playlists(db)
        return {"records": users,"total_records" : len(users),"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})
    

@router.get("/{playlist_id}")
async def view_playlist_details(playlist_id: int,db: Session = Depends(get_db)):
    playlists = get_playlist(db, playlist_id)
    if playlists:
        return {"records": playlists,"total_records" : 1,"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.put("/{playlist_id}")
async def update_playlist_details(playlist_id: int,name: str,db: Session = Depends(get_db)):
    temp = playlist_update(db,playlist_id,name)
    return temp
   
@router.delete("/{playlist_id}")
async def delete_playlist_details(playlist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = playlist_delete(db,playlist_id)
    return temp