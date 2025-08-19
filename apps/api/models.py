from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class PullRequest(Base):
    __tablename__ = "pull_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, index=True)
    pr_number = Column(Integer)  # Changed from 'number' to 'pr_number'
    title = Column(String(500))
    repo_name = Column(String(200))
    state = Column(String(50))
    action = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class ReviewComment(Base):
    __tablename__ = "review_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, index=True)
    pr_github_id = Column(Integer, index=True)
    body = Column(Text)
    path = Column(String(500))
    line = Column(Integer)
    position = Column(Integer)
    created_at = Column(DateTime, default=func.now())

class Finding(Base):
    __tablename__ = "findings"
    
    id = Column(Integer, primary_key=True, index=True)
    pr_github_id = Column(Integer, index=True)
    tool = Column(String(100))
    severity = Column(String(50))
    message = Column(Text)
    path = Column(String(500))
    line = Column(Integer)
    created_at = Column(DateTime, default=func.now())