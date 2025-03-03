from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext

# FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Vault Service is running"}

# Database setup
DATABASE_URL = "sqlite:///./vault.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Model for stored passwords
class VaultEntry(Base):
    __tablename__ = "vault"

    id = Column(Integer, primary_key=True, index=True)
    site = Column(String, unique=True, index=True)
    username = Column(String)
    password = Column(String)  # Hashed password

Base.metadata.create_all(bind=engine)

# Pydantic model for request validation
class VaultCreate(BaseModel):
    site: str
    username: str
    password: str

# Dependency: Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to store a password
@app.post("/store/")
def store_password(entry: VaultCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(entry.password)
    new_entry = VaultEntry(site=entry.site, username=entry.username, password=hashed_password)
    db.add(new_entry)
    db.commit()
    return {"message": "Password stored successfully"}

# Route to retrieve a password by site
@app.get("/retrieve/{site}")
def retrieve_password(site: str, db: Session = Depends(get_db)):
    entry = db.query(VaultEntry).filter(VaultEntry.site == site).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"site": entry.site, "username": entry.username, "password": "**** (hidden)"}

# Route to delete a password
@app.delete("/delete/{site}")
def delete_password(site: str, db: Session = Depends(get_db)):
    entry = db.query(VaultEntry).filter(VaultEntry.site == site).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return {"message": "Password deleted successfully"}

