from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.dependencies import get_db, get_current_user
from app.tasks.crud import task_crud, TaskCRUDResult
from app.tasks.schemas import (TaskResponse,TaskCreate,TaskUpdate,TaskListResponse,TaskStatus)
from app.users.models import User
router = APIRouter()

@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def mark_task_complete(
        task_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    updated_task, result = task_crud.update_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
        status=TaskStatus.COMPLETED
    )

    if result == TaskCRUDResult.NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    elif result == TaskCRUDResult.ACCESS_DENIED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    return updated_task


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
        status: Optional[TaskStatus] = Query(None, description="Filter tasks by status"),
        skip: int = Query(0, ge=0, description="Number of tasks to skip"),
        limit: int = Query(100, ge=1, le=100, description="Maximum number of tasks to return"),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    tasks = task_crud.get_user_tasks(
        db=db,
        user_id=current_user.id,
        status=status,
        skip=skip,
        limit=limit
    )

    return tasks

@router.get("/all", response_model=List[TaskResponse])
async def get_all_tasks(
        skip: int = Query(0, ge=0, description="Number of tasks to skip"),
        limit: int = Query(100, ge=1, le=100, description="Maximum number of tasks to return"),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    tasks = task_crud.get_all_tasks(db=db, skip=skip, limit=limit)
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
        task_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    task = task_crud.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    return task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
        task: TaskCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    created_task, result = task_crud.create_task(
        db=db,
        title=task.title,
        user_id=current_user.id,
        description=task.description,
        status=task.status
    )
    if result == TaskCRUDResult.VALIDATION_ERROR:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task data"
        )

    return created_task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
        task_id: int,
        task_update: TaskUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    updated_task, result = task_crud.update_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
        title=task_update.title,
        description=task_update.description,
        status=task_update.status
    )

    if result == TaskCRUDResult.NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    elif result == TaskCRUDResult.ACCESS_DENIED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    return updated_task


@router.delete("/{task_id}")
async def delete_task(
        task_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    success, result = task_crud.delete_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )

    if result == TaskCRUDResult.NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    elif result == TaskCRUDResult.ACCESS_DENIED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own tasks"
        )
    return {"message": "Task deleted"}

