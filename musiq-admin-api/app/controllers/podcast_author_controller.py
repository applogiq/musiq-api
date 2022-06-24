from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.podcast_author_service import *

def create_author_details(db,author,email):
    temp = author_details(db,author,email)
    if temp:
        return {"success":True,'message': "author details added","records": temp}
    else:
        return {'message': "check your details","success": False}
