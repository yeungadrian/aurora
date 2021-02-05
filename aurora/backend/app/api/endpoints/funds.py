from fastapi import APIRouter

from app.data.dataLoader import load_available_funds

router = APIRouter()


@router.get("/")
def get_funds():
    result = load_available_funds()

    return result
