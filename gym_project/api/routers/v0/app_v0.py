from fastapi import ApiRouter, Depends, HTTPException, status


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user():
    pass
