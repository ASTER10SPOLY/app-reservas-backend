# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth
from .database import engine, SessionLocal
from dotenv import load_dotenv

load_dotenv()
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_data = auth.decode_access_token(token)
    if not token_data or not token_data.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user = db.query(models.User).get(token_data.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# --- Auth endpoints ---
@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Profile endpoints ---
@app.get("/profile", response_model=schemas.ProfileOut)
def read_profile(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_profile(db, current_user.id)

@app.put("/profile", response_model=schemas.ProfileOut)
def update_profile(profile: schemas.ProfileCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_profile(db, current_user.id, profile)
