from fastapi import APIRouter

router = APIRouter(prefix="/mental", tags=["mental"])

@router.get("")
def mental():
    return {"status": "not ok"}