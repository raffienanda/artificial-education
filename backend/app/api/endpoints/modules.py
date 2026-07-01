from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.module import Module, Subtopic
from app.schemas.api_schemas import ModuleResponse, SubtopicResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ModuleResponse])
def get_modules(db: Session = Depends(get_db)):
    modules = db.query(Module).order_by(Module.order).all()
    return modules

@router.get("/{module_id}", response_model=ModuleResponse)
def get_module(module_id: str, db: Session = Depends(get_db)):
    mod = db.query(Module).filter(Module.id == module_id).first()
    if not mod:
        raise HTTPException(status_code=404, detail="Module not found")
    return mod

@router.get("/{module_id}/subtopics/{subtopic_id}", response_model=SubtopicResponse)
def get_subtopic(module_id: str, subtopic_id: str, db: Session = Depends(get_db)):
    subtopic = db.query(Subtopic).filter(Subtopic.id == subtopic_id, Subtopic.module_id == module_id).first()
    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")
    return subtopic
