from fastapi import APIRouter

from app.data.dataLoader import load_available_funds

router = APIRouter()


@router.get("/")
def funds():
    result = load_available_funds()

    return result