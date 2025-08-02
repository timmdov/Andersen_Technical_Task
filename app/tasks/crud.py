from sqlalchemy.orm import Session
from typing import List, Optional
from app.tasks.models import Task, TaskStatus


class TaskCRUD:

    def get_all_tasks(self, db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
        return db.query(Task).offset(skip).limit(limit).all()
    def get_user_tasks(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        return db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()
    def get_task_by_id(self, db: Session, task_id: int) -> Optional[Task]:
        return db.query(Task).filter(Task.id == task_id).first()
    def create_task(self, db: Session, title: str, user_id: int, description: Optional[str] = None,
                    status: TaskStatus = TaskStatus.NEW) -> Task:
        db_task = Task(
            title=title,
            description=description,
            status=status,
            user_id=user_id
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    def update_task(self, db: Session, task_id: int, user_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[TaskStatus] = None) -> Optional[Task]:

        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            return None

        if task.user_id != user_id:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status

        db.commit()
        db.refresh(task)
        return task

    def delete_task(self, db: Session, task_id: int, user_id: int) -> bool:

        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            return False

        if task.user_id != user_id:
            return False

        db.delete(task)
        db.commit()
        return True

task_crud = TaskCRUD()