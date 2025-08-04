from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.users.models import User
from app.core.security import get_password_hash

class UserCRUD:
    def create_user(self,db: Session,first_name: str,username: str,password: str,last_name: Optional[str] = None,) -> Optional[User]:
        hashed = get_password_hash(password)
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            hashed_password=hashed,
        )
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            return None

    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

user_crud = UserCRUD()