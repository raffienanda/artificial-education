from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_optional_current_user
from app.models.assessment import AssessmentAttempt
from app.models.module import Course, Module, Subtopic
from app.models.progress import UserProgress
from app.models.user import User
from app.schemas.api_schemas import CourseResponse, ModuleResponse, SubtopicResponse
from app.services.learning_path import build_prerequisite_graph
from typing import List

router = APIRouter()


def _module_passed(module: Module, mastery_by_topic: dict[str, float], completed_post_test_modules: set[str]) -> bool:
    sub_ids = [subtopic.id for subtopic in module.subtopics]
    if not sub_ids:
        return False
    average_mastery = sum(mastery_by_topic.get(sub_id, 0.0) for sub_id in sub_ids) / len(sub_ids)
    return module.id in completed_post_test_modules and average_mastery >= 60.0


def _module_unlocked(module: Module, db: Session, user_id: int, prereq_graph: dict) -> bool:
    if (module.order or 1) <= 1:
        return True

    all_progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
    mastery_by_topic = {progress.topic_id: progress.mastery for progress in all_progress}
    completed_post_test_modules = {
        row.module_id
        for row in db.query(AssessmentAttempt).filter(
            AssessmentAttempt.user_id == user_id,
            AssessmentAttempt.assessment_type == "post_test",
            AssessmentAttempt.finished_at.isnot(None),
            AssessmentAttempt.passed.is_(True),
        ).all()
    }
    module_by_id = {item.id: item for item in db.query(Module).all()}

    prerequisites = prereq_graph.get(module.id, [])
    if prerequisites:
        return all(
            _module_passed(
                module=module_by_id.get(prereq["id"]),
                mastery_by_topic=mastery_by_topic,
                completed_post_test_modules=completed_post_test_modules,
            )
            for prereq in prerequisites
            if module_by_id.get(prereq["id"])
        )

    previous_module = db.query(Module).filter(Module.order == (module.order or 1) - 1).first()
    return bool(previous_module and _module_passed(
        module=previous_module,
        mastery_by_topic=mastery_by_topic,
        completed_post_test_modules=completed_post_test_modules,
    ))


def _completed_pretest(db: Session, user_id: int, module_id: str) -> bool:
    return db.query(AssessmentAttempt).filter(
        AssessmentAttempt.user_id == user_id,
        AssessmentAttempt.module_id == module_id,
        AssessmentAttempt.assessment_type == "pre_test",
        AssessmentAttempt.finished_at.isnot(None),
    ).first() is not None


def _subtopic_unlocked(db: Session, user_id: int, module_id: str, subtopic_id: str) -> bool:
    subtopics = db.query(Subtopic).filter(Subtopic.module_id == module_id).order_by(Subtopic.id).all()
    target_index = next((index for index, item in enumerate(subtopics) if item.id == subtopic_id), -1)
    if target_index < 0:
        return False
    if target_index == 0:
        return True

    previous_ids = [item.id for item in subtopics[:target_index]]
    finished_count = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.user_id == user_id,
        AssessmentAttempt.module_id == module_id,
        AssessmentAttempt.subtopic_id.in_(previous_ids),
        AssessmentAttempt.assessment_type == "quiz",
        AssessmentAttempt.finished_at.isnot(None),
        AssessmentAttempt.passed.is_(True),
    ).count()
    return finished_count >= len(previous_ids)

def _enrich_module_with_user_progress(module: Module, db: Session, user_id: int, prereq_graph: dict) -> dict:
    """Helper to dynamically calculate module and subtopic status for a specific user."""
    module_dict = {
        "id": module.id,
        "course_id": module.course_id,
        "title": module.title,
        "icon": module.icon,
        "description": module.description,
        "difficulty": module.difficulty,
        "estimated_time": module.estimated_time,
        "order": module.order,
        "status": "locked",
        "subtopics": []
    }
    
    # 1. Fetch all progress and finished formal assessment attempts for this user.
    all_progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
    mastery_by_topic = {p.topic_id: p.mastery for p in all_progress}
    attempts = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.user_id == user_id,
        AssessmentAttempt.assessment_type.in_(["quiz", "post_test"]),
        AssessmentAttempt.finished_at.isnot(None),
    ).all()
    completed_quiz_subtopics = {
        attempt.subtopic_id
        for attempt in attempts
        if attempt.assessment_type == "quiz" and attempt.subtopic_id and attempt.passed
    }
    completed_post_test_modules = {
        attempt.module_id
        for attempt in attempts
        if attempt.assessment_type == "post_test" and attempt.passed
    }
    
    # A module only counts as passed after post test activity and enough average mastery.
    all_modules = db.query(Module).all()
    module_passed_status = {}
    for m in all_modules:
        sub_ids = [s.id for s in m.subtopics]
        if not sub_ids:
            module_passed_status[m.id] = False
            continue
        average_mastery = sum(mastery_by_topic.get(sid, 0.0) for sid in sub_ids) / len(sub_ids)
        has_post_test = m.id in completed_post_test_modules
        module_passed_status[m.id] = has_post_test and average_mastery >= 60.0
        
    # 2. Check if prerequisites are met
    is_unlocked = True
    module_prereqs = prereq_graph.get(module.id, [])
    for prereq in module_prereqs:
        prereq_id = prereq["id"]
        if not module_passed_status.get(prereq_id, False):
            is_unlocked = False
            break
            
    # Always unlock the first module (order 1)
    if module.order == 1:
        is_unlocked = True
        
    # 3. Populate subtopics and their completed status
    subtopics_completed = 0
    total_subtopics = len(module.subtopics)
    
    # Sort subtopics properly to maintain structure
    subtopics = sorted(module.subtopics, key=lambda s: s.id)
    
    for sub in subtopics:
        is_completed = sub.id in completed_quiz_subtopics
        if is_completed:
            subtopics_completed += 1
            
        module_dict["subtopics"].append({
            "id": sub.id,
            "title": sub.title,
            "content": sub.content,
            "completed": is_completed
        })
        
    # 4. Determine final module status
    if not is_unlocked:
        module_dict["status"] = "locked"
    elif module_passed_status.get(module.id, False):
        module_dict["status"] = "completed"
    else:
        module_dict["status"] = "in_progress"
        
    return module_dict

@router.get("/course/current", response_model=CourseResponse)
def get_current_course(db: Session = Depends(get_db)):
    course = db.query(Course).order_by(Course.id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/", response_model=List[ModuleResponse])
def get_modules(
    user_id: int = 1,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    user_id = current_user.id if current_user else user_id
    modules = db.query(Module).order_by(Module.order).all()
    prereq_graph = build_prerequisite_graph(db)
    
    response = []
    for module in modules:
        response.append(_enrich_module_with_user_progress(module, db, user_id, prereq_graph))
        
    return response

@router.get("/{module_id}", response_model=ModuleResponse)
def get_module(
    module_id: str,
    user_id: int = 1,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user)
):
    user_id = current_user.id if current_user else user_id
    mod = db.query(Module).filter(Module.id == module_id).first()
    if not mod:
        raise HTTPException(status_code=404, detail="Module not found")
        
    prereq_graph = build_prerequisite_graph(db)
    return _enrich_module_with_user_progress(mod, db, user_id, prereq_graph)

@router.get("/{module_id}/subtopics/{subtopic_id}", response_model=SubtopicResponse)
def get_subtopic(
    module_id: str,
    subtopic_id: str,
    user_id: int = 1,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user)
):
    user_id = current_user.id if current_user else user_id
    subtopic = db.query(Subtopic).filter(Subtopic.id == subtopic_id, Subtopic.module_id == module_id).first()
    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")

    mod = db.query(Module).filter(Module.id == module_id).first()
    prereq_graph = build_prerequisite_graph(db)
    if not mod or not _module_unlocked(module=mod, db=db, user_id=user_id, prereq_graph=prereq_graph):
        raise HTTPException(status_code=403, detail="Modul masih terkunci")
    if not _completed_pretest(db=db, user_id=user_id, module_id=module_id):
        raise HTTPException(status_code=403, detail="Pre test modul harus diselesaikan terlebih dahulu")
    if not _subtopic_unlocked(db=db, user_id=user_id, module_id=module_id, subtopic_id=subtopic_id):
        raise HTTPException(status_code=403, detail="Selesaikan quiz subtopik sebelumnya terlebih dahulu")
        
    is_completed = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.user_id == user_id,
        AssessmentAttempt.module_id == module_id,
        AssessmentAttempt.subtopic_id == subtopic_id,
        AssessmentAttempt.assessment_type == "quiz",
        AssessmentAttempt.finished_at.isnot(None),
        AssessmentAttempt.passed.is_(True),
    ).first() is not None
    
    return {
        "id": subtopic.id,
        "title": subtopic.title,
        "content": subtopic.content,
        "completed": is_completed
    }
