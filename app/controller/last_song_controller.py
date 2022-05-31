from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from app.model.last_song_model import last_songs

from app.model.song_model import songs
from app.model.album_model import albums


def user_last_song(db: Session,song):
    user_temp = db.query(last_songs).filter(last_songs.user_id == song.user_id,songs.is_delete == 0).first()
    if user_temp:
        song_temp = db.query(songs).filter(songs.song_id == song.song_id,songs.is_delete == 0).first()
        user_temp.song_id = song.song_id
        user_temp.duration = song_temp.duration
        user_temp.paused_timing = song.paused_timing
        user_temp.updated_at = datetime.now()
        if song.paused_timing >= "00:01:00":
            s = song_temp.listeners
            if s:
                pass
            else:
                s = 0
            song_temp.listeners = s+1
        else:
            pass
        db.commit()
        return {'message': "song detail updated"}
    else:
        raise HTTPException(status_code=404, detail="Check your id!!!")


def get_last_song(db: Session, user_id: int):
    user = db.query(last_songs).filter(last_songs.id == user_id,last_songs.is_delete == 0).first()
    # print(str(user.duration)>"5:00:00")
    if user:
        return user
    else:
        return False

def get_last_songs(db: Session):
    return db.query(last_songs).filter(last_songs.is_delete == 0).all()