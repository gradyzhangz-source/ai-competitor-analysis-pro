from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from app.core.database import Base

class AnalysisTask(Base):
    __tablename__ = "analysis_tasks"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    industry = Column(String)
    competitors = Column(JSON)  # list of strings
    status = Column(String, default="pending")  # pending, running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Store the full AnalysisState JSON
    result_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
