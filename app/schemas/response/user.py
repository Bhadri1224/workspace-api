# app/schemas/responses/user.py
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username: str
    # 🛡️ NOTICE: No password field here! Security tracking data only.

    # Tells Pydantic to read raw SQLAlchemy user models cleanly
    model_config = {"from_attributes": True}