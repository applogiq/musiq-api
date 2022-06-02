from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from app.model.recent_model import recents
from app.model.song_model import songs



def user_recent_song(db: Session,song):
    user_temp = db.query(recents).filter(recents.user_id == song.user_id,recents.is_delete == 0).first()
    if user_temp:
        temp = []
        if len(user_temp.song_id["songs"]):
            temp = list(user_temp.song_id["songs"])
        if len(user_temp.song_id["songs"]) > 1:
            s = len(user_temp.song_id["songs"])
        else:
            s = 1
        if s == 30:  
            if song.song_id in temp:
                for i in range(0,s):
                    if i < len(user_temp.song_id["songs"]):
                        if song.song_id == temp[i]:
                            temp.pop(i)
                            temp.append(song.song_id)
            else:
                temp.pop(0)
                temp.append(song.song_id)
        elif s < 30:
            if song.song_id in temp:
                for i in range(0,s):
                    if i < len(user_temp.song_id["songs"]):
                        if song.song_id == temp[i]:
                            temp.pop(i)
                            temp.append(song.song_id)
            else:
                temp.append(song.song_id)
        user_temp.song_id["songs"] = temp
        user_temp.updated_at = datetime.now()
        user_temp.updated_by = 1
        db.commit()
        return {"message":"data added"}
    else:
        raise HTTPException(status_code=404, detail="Check your id!!!")


def get_user_song(db: Session, user_id: int):
    user = db.query(recents).filter(recents.id == user_id,recents.is_delete == 0).first()
    if user:
        return user
    else:
        return False

def get_users_songs(db: Session):
    return db.query(recents).filter(recents.is_delete == 0).all()


    # {"songs": ["SG001", "SG002", "SG003", "SG004", "SG005", "SG006", "SG007", "SG008", "SG009", "SG0010", "SG0011", "SG0012", "SG0013", "SG0014", "SG0015", "SG0016", "SG0017", "SG0018", "SG0019", "SG0020", "SG0021", "SG0022", "SG0023", "SG0024", "SG0025", "SG0026", "SG0027", "SG0028", "SG0029", "SG0030"]}

    # def user_recent_song(db: Session,song):
    # user_temp = db.query(recents).filter(recents.user_id == song.user_id,recents.is_delete == 0).first()
    # if user_temp:
    #     if len(user_temp.song_id["songs"]):
    #         temp = list(user_temp.song_id["songs"])
    #         print(temp,1)
    #     # else:
    #     #     temp = []
    #         print(len(user_temp.song_id["songs"]))
    #         if len(user_temp.song_id["songs"]) > 1:
    #             s = len(user_temp.song_id["songs"])
    #             print(s,122)
    #         else:
    #             s = 1
    #             print(s,2)
    #         if s == 30:  
    #             print(22222222)
    #             if song.song_id in temp:
    #                 for i in range(0,s):
    #                     if i < len(user_temp.song_id["songs"]):
    #                         if song.song_id == temp[i]:
    #                             temp.pop(i)
    #                             print(len(temp),11111)
    #                             temp.append(song.song_id)
    #             else:
    #                 print(333333)
    #                 temp.pop(0)
    #                 temp.append(song.song_id)
    #             print(temp,2)
    #         elif s < 30:
    #             if song.song_id in temp:
    #                 for i in range(0,s):
    #                     if i < len(user_temp.song_id["songs"]):
    #                         if song.song_id == temp[i]:
    #                             temp.pop(i)
    #                             print(len(temp),3333)
    #                             temp.append(song.song_id)
    #             else:
    #                 temp.append(song.song_id)
    #                 print(temp,3)
    #     print(temp,4)
    #     user_temp.song_id["songs"] = temp
    #     db.commit()
    #     return {"message":"data added"}
    # else:
    #     raise HTTPException(status_code=404, detail="Check your id!!!")