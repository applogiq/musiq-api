import psycopg2
from config.database import IPAddr
# import config


def add_part(id):
    conn = psycopg2.connect(user="postgres",
                            password="12345678",
                            host='localhost',
                            port="5432",
                            database="music")
    cur = conn.cursor()
    print(11111111)

    cur.execute('''SELECT get_recent_podcast(%s)''', str(id))
    print(2222222222)

    conn.commit()
    result = cur.fetchall()
    a = []
    n = {}
    for row in result:
        # print(row[0])
        # char = ["(",]
        s = row[0].replace('(', '').replace(')', '').split(",")
        # n["user_id"] = s[0]
        # n["podcast_id"] = s[1]
        # n["episode_number"] = s[2]
        # n["paused_timing"] = s[3]
        n={"user_id":s[0],"podcast_id":s[1],"episode_number":s[2],"paused_timing":s[3]}
        a.append(n)
        print(s)
        # print(a,n,111111111111111111)
    # print(s)
    # print(a)
    # print(n)
    
    cur.close()
    return a

    # sites_result = s.fetchall()
    # sites = ["." + site[0] for site in sites_result]
    # print("Allowed hosts")
    # print(sites)
    # return sites

    # print(s)

    # commit the transaction
    # conn.commit()

    # # close the cursor
    # cur.close()
    # except (Exception, psycopg2.DatabaseError) as error:
    #     print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()
    # return cur.values()






# from requests import Session
# from fastapi import Depends,HTTPException
# from datetime import datetime
# import os,time
# import base64



# # from utils.auth_handler import create_access_token
# from model.demo_genre_model import *
# from config.database import *
# from model.album_model import *
# from services.admin_user_service import *
# from services.album_service import *

# def demo_check(db):
#     # query1 = db.query(songs).filter(songs.is_delete == False).all()
#     query1 = db.query(demo_genre).all()
#     # query1 = db.query(songs.id, songs.name).filter(songs.artist_id[0].in_([artist_id])).all()
#     #query1 = db.query(songs.album_id, songs.name).filter(songs.artist_id.in_([1,2])).all()
#     # print(query1[1].artist_id)
#     # if 1 in query1[1].artist_id:
#     #     print(True)
#     # print(query1)

#     return query1

# # import wave
# # import contextlib
# # fname = f"{DIRECTORY}/music/tamil/Mis/3/songs/SG001.wav"
# # with contextlib.closing(wave.open(fname,'r')) as f:
# #     frames = f.getnframes()
# #     rate = f.getframerate()
# #     duration = frames / float(rate)
# #     print(duration)