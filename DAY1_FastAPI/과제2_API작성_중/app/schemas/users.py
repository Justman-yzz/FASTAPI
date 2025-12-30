from enum import Enum
from typing import Optional
from fastapi import Query
from pydantic import BaseModel, Field

class Gender(str, Enum): # 📝 Enum이라 male/female만 통과
    male = "male"
    female = "female"

class UserCreate(BaseModel): # 💡 Body검증용
    username: str = Field(min_length=1)
    age: int
    gender: Gender

class UserUpdate(BaseModel): # 💡 부분수정 
    username: Optional[str] = None # 📝 부분 수정이라 Optionalfh 
    age: Optional[int] = None

class UserOut(BaseModel): # 💡 id, username, age, gender만 딱 나오도록
    id: int
    username: str
    age: int
    gender: Gender

## 🔥 username, age, gender 이외의 쿼리 매개변수는 받지 않고 에러 반환
class UserSearchQuery(BaseModel):
    username: str | None = Query(default=None)
    age: int | None = Query(default=None, gt=0)
    gender: Gender | None = Query(default=None)