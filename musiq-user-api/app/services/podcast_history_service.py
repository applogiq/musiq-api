from sqlalchemy.orm import Session
from datetime import datetime

from model.podcast_model import podcast
from model.podcast_history_model import podcast_history
from model.podcast_episode_model import podcast_episode
from services.user_service import get_email
from config.database import DIRECTORY
# from services.podcast_author_service import *

import psycopg2
# from config.database import IPAddr

###enter single user podcast history details
def podcast_history_detail(db: Session,history,email):
    temp = get_email(email,db)
    db_history = podcast_history(user_id = history.user_id,
                        podcast_id = history.podcast_id,
                        episode_number = history.episode_number,
                        paused_timing = history.paused_timing,
                        created_by = temp.id,
                        created_at = datetime.now()
                        )

    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

###get podcast recents of single user by using stored procedure in postgres database
def podcast_recent_user(id):
    conn = psycopg2.connect(user="postgres",
                            password="12345678",
                            host='localhost',
                            port="5432",
                            database="music")
    cur = conn.cursor()
    cur.execute('''SELECT get_recent_podcast(%s)''', str(id))
    conn.commit()
    result = cur.fetchall()
    a = []
    n = {}
    for row in result:
        s = row[0].replace('(', '').replace(')', '').split(",")
        n={"user_id":s[0],"podcast_id":s[1],"episode_number":s[2],"paused_timing":s[3]}
        a.append(n)
    cur.close()
    return a
