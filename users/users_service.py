from sqlalchemy.orm import Session
from models import User
from fastapi import HTTPException, status, UploadFile
from auth.auth_utils import get_password_hash
import os
import shutil

UPLOAD_DIR = "public/image/profile"

def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="USER_NOT_FOUND")
    return user

def update_user(user_id: int, update_data: dict, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="USER_NOT_FOUND")
    
    if "nickname" in update_data:
        user.nickname = update_data["nickname"]
    if "profileImageUrl" in update_data:
        user.profile_image_url = update_data["profileImageUrl"]
        
    db.commit()
    db.refresh(user)
    return user

def update_user_password(user_id: int, new_password: str, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="USER_NOT_FOUND")
    
    user.password = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return user

def delete_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="USER_NOT_FOUND")
        
    db.delete(user)
    db.commit()
    return True

def upload_profile_image(user_id: int, file: UploadFile, db: Session):
    # FE에서 S3에 직접 업로드하므로 이 로직은 비활성화하거나 S3 업로드로 교체해야 합니다.
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="S3_UPLOAD_REQUIRED_ON_FE")
