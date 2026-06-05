# app/repositories/audit_log.py
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog

class AuditLogRepository:
    @staticmethod
    def log_event(db: Session, username: str, action: str, resource: str, ip_address: str = None, extra: dict = None):
        """
        Inserts a pristine, immutable security trail record directly into the audit_logs table.
        """
        log_entry = AuditLog(
            username=username,
            action=action,
            resource=resource,
            ip_address=ip_address,
            extra_details=extra
        )
        try:
            db.add(log_entry)
            db.commit()
            db.refresh(log_entry)
            return log_entry
        except Exception as e:
            db.rollback()
            # If the database logging fails, we raise it so transactions don't pass silently
            raise e