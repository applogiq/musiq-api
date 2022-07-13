import bcrypt
from requests import Session
from model.user_model import users
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

###to encode password 
def get_password_hash(password):
    return pwd_context.hash(password)

###to decode hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)




# def create_hash_paswword(password):
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed_password

# # def check_password(db: Session,email,password):
# #     db_user_info = db.query(users).filter(users.email == email).first()
# #     return bcrypt.checkpw(password.encode('utf-8'), db_user_info.password.encode('utf-8'))

# def check_password(db: Session,email,password):
#     db_user_info = db.query(users).filter(users.email == email).first()
#     db_user_info.password = (bytes(db_user_info.password, 'utf-8'))
#     # if bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) == bytes(db_user_info.password, 'utf-8'):
#     #     print(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),11111111)
#     #     print(bytes(db_user_info.password, 'utf-8'))
#     # else:
#     # print(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),11111111)
#     # db_user_info.password = (bytes(db_user_info.password, 'utf-8'))
#     # print(db_user_info.password.decode('utf-8'),33333)
#     # print(2222)
#     if bcrypt.checkpw(password, db_user_info.password):
#     # if bcrypt.hashpw(password, db_user_info.password) == db_user_info.password:
#         print(111111)
#     return True  