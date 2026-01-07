from fastapi import APIRouter
from pydantic import BaseModel
from controllers.user_controller import create_user as create_user_controller

router = APIRouter()

# POST 요청에서 받을 데이터 모델
class User(BaseModel):
    name: str
    age: int

# POST 요청
@router.post("/users")
def create_user(user: User):
    return create_user_controller(user)