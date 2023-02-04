from requests import Session

from model.album_model import *
from config.database import *
from model.artist_model import *

###get album details by id
def album_get_by_id(id,db):
    return db.query(albums).filter(albums.id == id,albums.is_delete==False).first()

###get all album details
def album_get_all(db: Session, skip: int = 0, limit: int = 100):
    user = db.query(albums).filter(albums.is_delete == False).offset(skip).limit(limit).all()
    if user:
        return user
    else:
        return False

    
    

    

    
   