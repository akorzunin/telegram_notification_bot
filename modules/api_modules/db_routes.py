
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
def create_item(item: schemas.RuleCreate, db: Session = Depends(get_db)):
    return crud.create_rule(db=db, item=item, )

# create user
@router.post("/create_user/", response_model=schemas.UserRead)
def create_item(item: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, item=item, )



@router.get("/test_db")
async def test_db():
    return {'db': 'test_db'}