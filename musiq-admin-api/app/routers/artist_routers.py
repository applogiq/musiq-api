from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.artist_schema import *
from utils.auth_bearer import JWTBearer
from utils.auth_handler import *
from config.database import *
from controllers.artist_controller import *

router = APIRouter(tags=["artist"],prefix="/artist")

http_bearer = JWTBearer()

###to enter new artist detail
@router.post("/")
async def enter_artist_details(artists:ArtistSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    s = decodeJWT(token) 
    return create_artist_detail(db,artists,s["sub"])
    
###to get all artist details
@router.get("/",dependencies=[Depends(http_bearer)])
async def view_all_artist_details(db: Session = Depends(get_db),skip: int = 0, limit: int = 100,token: str = Depends(http_bearer)):
    return get_all_artist_detail(db)

###to get single aqrtist detail by their id
@router.get("/{artist_id}")
async def view_artist_details(artist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_artist_detail_by_id(db,artist_id)

###to update existing artist detail
@router.put("/{artist_id}")
async def update_artist_details(artist_id: int,artists:ArtistSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token) 
    return  update_artist(db,artist_id,artists,s["sub"])
   
###to remove image for particular artist
@router.delete("/image/{artist_id}")
async def remove_image(art_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return artist_delete_image(db,art_id)
    
###search functionality
@router.get("/list/search")
async def artist_search_function(data: str,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return artist_search_engine_details(db,data) 
