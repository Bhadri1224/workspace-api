from sqlalchemy.orm import Session
from app.models.user import Users

class UserRepository:
    @staticmethod
    def get_user_by_name(db: Session, username: str) -> Users | None:
        return db.query(Users).filter(Users.user_name == username).first()

    @staticmethod
    def create_user(db: Session, db_user: Users) -> Users:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user