
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

router = APIRouter()

from modules.api_modules.db_api import crud, models, schemas
from modules.api_modules.db_api.database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create rule
@router.post("/create_rule/", response_model=schemas.RuleRead)
def create_rule(item: schemas.RuleCreate, db: Session = Depends(get_db)):
    return crud.create_rule(db=db, item=item, )

# read all rules
@router.get("/read_all_rules/", response_model=list[schemas.RuleRead])
def read_all_rules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_all_rules(db=db, skip=skip, limit=limit, )

# read rule by id

# delete rule by id
@router.delete("/delete_rule/", )
def delete_rule(rule_id: int, db: Session = Depends(get_db)) -> bool:
    return crud.delete_rule_by_id(db=db, rule_id=rule_id, )

# read all users
@router.get("/read_all_users/", response_model=list[schemas.UserRead])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_all_users(db=db, skip=skip, limit=limit, )

# read user rules
@router.get("/read_user_rules/", response_model=schemas.UserRead)
def read_user_rules(user_id: int, db: Session = Depends(get_db)):
    return crud.read_user_rules(db=db, user_id=user_id, )

# create user
@router.post("/create_user/", response_model=schemas.UserRead)
def create_user(item: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, item=item, )

# delete user by id
@router.delete("/delete_user/", )
def delete_user(user_id: int, db: Session = Depends(get_db)) -> bool:
    return crud.delete_user_by_id(db=db, user_id=user_id, )

