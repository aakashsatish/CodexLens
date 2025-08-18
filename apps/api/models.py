from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, nullable=False)
    repo_name = Column(String, nullable=False)
    title = Column(String)
    author = Column(String)
    state = Column(String)
    opened_at = Column(DateTime, default=func.now())
    first_response_ms = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Review(Base):
    __tablename__ = "review_comments"

    id = Column(Integer, primary_key=True)
    pr_id = Column(Integer, nullable=False)
    github_comment_id = Column(Integer, unique=True)  # GitHub's comment ID
    file_path = Column(String)
    line_number = Column(Integer)
    severity = Column(String)  # low, medium, high
    content = Column(Text)
    adopted = Column(Boolean, default=False)  # Did maintainer accept/edit this?
    created_at = Column(DateTime, default=func.now())

class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True)
    pr_id = Column(Integer, nullable=False)
    type = Column(String)  # security, performance, style, bug
    rule_id = Column(String)  # e.g., "ruff.E501", "bandit.B101"
    severity = Column(String)  # low, medium, high
    file_path = Column(String)
    line_number = Column(Integer)
    message = Column(Text)
    payload = Column(JSON)  # Additional data from analyzer
    created_at = Column(DateTime, default=func.now())