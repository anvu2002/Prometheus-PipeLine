# models.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql://user:password@localhost/gpu_monitor"

Base = declarative_base()

class GPUUsage(Base):
    __tablename__ = 'gpu_usage'
    
    id = Column(Integer, primary_key=True)
    gpu_id = Column(String)
    memory_used = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class UserAction(Base):
    __tablename__ = 'user_actions'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    action = Column(String)
    response_time = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Database connection setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
