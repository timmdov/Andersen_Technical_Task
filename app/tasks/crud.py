from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from app.tasks.models import Task, TaskStatus
from app.tasks.schemas import TaskCRUDResult
from sqlalchemy.exc import IntegrityError

class TaskCRUD:

    def get_all_tasks(self, db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
        return db.query(Task).offset(skip).limit(limit).all()

    def get_user_tasks(self, db: Session, user_id: int, status: Optional[TaskStatus] = None, skip: int = 0, limit: int = 100):
        query = db.query(Task).filter(Task.user_id == user_id)
        if status is not None:
            query = query.filter(Task.status == status)
        return query.offset(skip).limit(limit).all()

    def get_task_by_id(self, db: Session, task_id: int) -> Optional[Task]:
        return db.get(Task, task_id)

    def get_tasks_by_status(self, db: Session, status: TaskStatus, skip: int = 0, limit: int = 100) -> List[Task]:
        return db.query(Task).filter(Task.status == status).offset(skip).limit(limit).all()

    def count_user_tasks(self, db: Session, user_id: int, status: Optional[TaskStatus] = None) -> int:
        query = db.query(Task).filter(Task.user_id == user_id)
        if status is not None:
            query = query.filter(Task.status == status)
        return query.count()

    def count_all_tasks(self, db: Session) -> int:
        return db.query(Task).count()

    def create_task(self, db: Session, title: str, user_id: int, description: Optional[str] = None, status: TaskStatus = TaskStatus.NEW) -> Tuple[Optional[Task], TaskCRUDResult]:
        db_task = Task(
            title=title,
            description=description,
            status=status,
            user_id=user_id
        )
        try:
            db.add(db_task)
            db.commit()
            db.refresh(db_task)
            return db_task, TaskCRUDResult.SUCCESS
        except IntegrityError as e:
            db.rollback()
            error_message = str(e).lower()
            if "foreign key constraint" in error_message or "violates foreign key" in error_message:
                return None, TaskCRUDResult.NOT_FOUND
            else:
                return None, TaskCRUDResult.VALIDATION_ERROR
        except Exception:
            db.rollback()
            raise

    def update_task(self, db: Session, task_id: int, user_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[TaskStatus] = None,) -> Tuple[Optional[Task], TaskCRUDResult]:

        task = db.get(Task, task_id)

        if not task:
            return None, TaskCRUDResult.NOT_FOUND
        if task.user_id != user_id:
            return None, TaskCRUDResult.ACCESS_DENIED
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        try:
            db.commit()
            db.refresh(task)
            return task, TaskCRUDResult.SUCCESS
        except Exception:
            db.rollback()
            raise

    def delete_task(self, db: Session, task_id: int, user_id: int) -> Tuple[bool, TaskCRUDResult]:
        task = db.get(Task, task_id)
        if not task:
            return False, TaskCRUDResult.NOT_FOUND
        if task.user_id != user_id:
            return False, TaskCRUDResult.ACCESS_DENIED
        try:
            db.delete(task)
            db.commit()
            return True, TaskCRUDResult.SUCCESS
        except Exception:
            db.rollback()
            raise

task_crud = TaskCRUD()