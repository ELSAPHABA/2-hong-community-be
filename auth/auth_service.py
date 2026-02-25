from sqlalchemy.orm import Session
from models import User
from auth.auth_schemas import SignupRequest
from auth.auth_utils import get_password_hash, verify_password
from fastapi import UploadFile, HTTPException, status
import os
import shutil

UPLOAD_DIR = "public/image/profile"

def is_email_exist(email: str, db: Session) -> bool:
    user = db.query(User).filter(User.email == email).first()
    return user is not None

def is_nickname_exist(nickname: str, db: Session) -> bool:
    user = db.query(User).filter(User.nickname == nickname).first()
    return user is not None

def create_user(email: str, password: str, nickname: str, profileImage: UploadFile, db: Session):
    # 1. 유저 생성 (프로필 이미지는 FE에서 S3 업로드 후 URL을 넘겨주거나 별도 API로 처리한다고 가정)
    new_user = User(
        email=email,
        password=get_password_hash(password),
        nickname=nickname,
        profile_image_url=None # 필요 시 FE에서 받은 URL로 업데이트
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.password):
        return None
    
    return user
