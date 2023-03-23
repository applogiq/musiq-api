from requests import Session

from model.user_model import *
from config.database import *
from model.artist_model import *
from services.user_service import get_email,get_by_id

###get all artist details
def artist_get_all(db: Session, skip: int = 0, limit: int = 100):
    user = db.query(artist).filter(artist.is_delete == False).order_by(artist.artist_name).offset(skip).limit(limit).all()
    if user:
        return user
    else:
        return False

###check whether image is available for artist or not
def artist_image_check(db,id):
    return db.query(artist).filter(artist.id == id,artist.is_delete == False,artist.is_image == True).first()

###get single artist details by id
def artist_get_by_id(db,id):
    return db.query(artist).filter(artist.id == id,artist.is_delete==False).first()

###limited artist details for home page(preference need to show first)
def artist_home_page(db,email):
    limit = 5
    temp = get_email(email,db)
    artist_pref = get_by_id(temp.id,db)
    length = len(artist_pref.preference["artist"])
    if limit >= length:
        result = {}
        artists = db.query(artist).filter(artist.artist_id.in_(artist_pref.preference["artist"]),artist.is_delete == False).all()
        artist1 = db.query(artist).filter(artist.artist_id.notin_(artist_pref.preference["artist"]),artist.is_delete == False).limit(limit-length).all()
        for i in range(0,len(artist1)):
            artists.append(artist1[i])
    else:
        artists = db.query(artist).filter(artist.is_delete == False).order_by(artist.artist_name).limit(limit).all()
    return artists


###to search for similar artist name from data
def artist_search_engine(db,data):
    return db.query(artist).filter(artist.artist_name.ilike(f'%{data}%')).all()