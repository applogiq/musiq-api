from sqlalchemy.orm import Session

from model.aura_model import aura

###get all aura details
def aura_get_all(db: Session,limit):
    return db.query(aura).filter(aura.is_delete == False).limit(limit).all()

###get aura details by id 
def aura_get_by_id(db: Session, aura_id: int):
    auras = db.query(aura).filter(aura.id == aura_id,aura.is_delete == False).first()
    if auras:
        return auras
    else:
        return False