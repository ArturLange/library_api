from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from lib_api import crud, schemas
from lib_api.db import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.User])
async def get_users(
    skip: int | None = None, limit: int | None = None, db: Session = Depends(get_db)
):
    return crud.get_users(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user.id)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with given id already exists",
        )
    return crud.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=schemas.User)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db, user_id=user_id)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id=user_id)

    return Response(status_code=204)
