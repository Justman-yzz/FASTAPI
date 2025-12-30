# ☐ FastAPI 공식 문서를 통해 API 작성하기 (중)☐ 💡 📝  ✅ 🔥 →
목표: Pydantic / Path / Query 검증을 사용해서 Users API 6개 구현하기

## 0. 준비 체크
- [ ] poetry 환경 OK (poetry run uvicorn, poetry run mypy 등)
- [ ] app/models/users.py 안에 UserModel 메서드 확인(all, get, delete, update/create 등)
- [ ] app/schemas/users.py 에 Pydantic 스키마 작성할 위치 확인

---

## 1. POST /users (유저 생성)
요구:
- Body: username(str), age(int), gender(Enum: male/female)
- Pydantic 검증 후 UserModel 인스턴스 생성
- Response: 생성된 user id 반환

체크:
- [ ] CreateUserSchema 만들기 (username, age, gender)
- [ ] Gender Enum 만들기 (male/female)
- [ ] 라우터 작성: create_user()
- [ ] /docs에서 요청 예시로 동작 확인

---

## 2. GET /users (전체 조회)
요구:
- UserModel.all() 사용
- 유저 없으면 404
- Response: [{id, username, age, gender}, ...]

체크:
- [ ] UserResponseSchema 만들기 (id, username, age, gender)
- [ ] 라우터 작성: list_users()
- [ ] 유저 없을 때 404 확인

---

## 3. GET /users/{user_id} (유저 단건 조회)
요구:
- Path 객체로 user_id 양수 검증
- user 없으면 404
- Response: {id, username, age, gender}

체크:
- [ ] Path(gt=0) 적용
- [ ] UserModel.get(id=user_id) 연동
- [ ] 404 케이스 확인

---

## 4. PATCH /users/{user_id} (유저 부분 수정)
요구:
- Path로 user_id 양수 검증
- Body: username 또는 age (부분 수정)
- user 없으면 404
- Response: {id, username, age, gender}

체크:
- [ ] UpdateUserSchema 만들기 (username: Optional[str], age: Optional[int])
- [ ] user 찾고 값 있으면 업데이트
- [ ] 업데이트된 결과 반환

---

## 5. DELETE /users/{user_id} (유저 삭제)
요구:
- Path로 user_id 양수 검증
- user 없으면 404
- 삭제 후 응답:
  {"detail": "User: {user_id}, Successfully Deleted."}

체크:
- [ ] delete 라우터 작성
- [ ] 응답 문자열 형식 정확히 맞추기

---

## 6. GET /users/search (유저 검색)
요구:
- Query: username, age, gender
- Pydantic + Query로 검증 (age > 0)
- username/age/gender 외 쿼리 받으면 에러
- 결과 없으면 404
- Response: [{id, username, age, gender}, ...]

체크:
- [ ] SearchUserQuerySchema 만들기
- [ ] Query 옵션 적용 (age gt=0 등)
- [ ] "추가 쿼리 금지" 처리 방법 적용
- [ ] 404 케이스 확인
