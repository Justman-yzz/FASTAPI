# main.py

from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Request

from app.models.users import UserModel
from app.schemas.users import UserCreate, UserOut, UserUpdate, UserSearchQuery

app = FastAPI()

UserModel.create_dummy() # API 테스트를 위한 더미를 생성하는 메서드 입니다.

# 1) POST/users 만들기 📝 유저생성
@app.post("/users")
async def create_user(payload: UserCreate):
	user = UserModel.create(
		username = payload.username,
		age=payload.age,
		gender=payload.gender.value,
	)
	return {"id": user.id}


# 2) GET/users 📝 전체조회
@app.get("/users")
async def list_users():
    users = UserModel.all()
    if not users:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

    return [UserOut(id=u.id, username=u.username, age=u.age, gender=u.gender) for u in users]


# 3) GET/users/{user_id} 📝 특정 유저조회
@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

    return UserOut(id=user.id, username=user.username, age=user.age, gender=user.gender)


# 4) PATCH/users/{user_id} 📝 특정 유저 부분 수정
@app.patch("/users/{user_id}")
async def update_user(
    user_id: int = Path(gt=0),
    payload: UserUpdate = ...,
):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

    user.update(username=payload.username, age=payload.age)

    return UserOut(id=user.id, username=user.username, age=user.age, gender=user.gender)


# 5) DELETE/users/{user_id} 📝 특정 유저 삭제
@app.delete("/users/{user_id}")
async def delete_user(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 유저는 삭제할 수 없습니다.")

    user.delete()
    return {"detail": f"User: {user_id}, 성공적으로 삭제처리 되었습니다."}


# 6) GET/users/search 📝 특정 유저 검색
## 🔥 username, age, gender 이외의 쿼리 매개변수는 받지 않고 에러 반환
## → 추가 쿼리 금지 를 직접 체크
@app.get("/users/search")
async def search_users(request: Request, q: Annotated[UserSearchQuery, ...]):
    # 6-1) 📝 추가 쿼리 금지 체크
    allowed = {"username", "age", "gender"}
    extra = set(request.query_params.keys()) - allowed
    if extra:
        raise HTTPException(status_code=400, detail=f"잘못된 요청입니다: {sorted(extra)}")

    # 6-2) 📝 필터링
    filters = {}
    if q.username is not None:
        filters["username"] = q.username
    if q.age is not None:
        filters["age"] = q.age
    if q.gender is not None:
        filters["gender"] = q.gender.value

    users = UserModel.filter(**filters) if filters else []

    if not users:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

    return [UserOut(id=u.id, username=u.username, age=u.age, gender=u.gender) for u in users]


if __name__ == '__main__':
	import uvicorn
	
	uvicorn.run(app, host='0.0.0.0', port=8000) 
	