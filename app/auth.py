# auth.py
from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
import random
import smtplib
from  email.mime.text import MIMEText
from  email.mime.multipart import MIMEMultipart
from datetime import datetime,timezone
from app.model import UserInfo,SessionHistory
def send_email_otp(to_email, otp):
    # These are placeholder settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "narayananbhadri34@gmail.com"
    sender_password = "ynwj rsae aivl rcuh" # Generate this in Google Account settings

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = "Your Verification Code"
    message.attach(MIMEText(f"Your OTP is: {otp}", "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
router = APIRouter()

# Simple memory storage
otp_storage = {}


@router.post("/send-otp")
async def send_otp(data: dict):
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp

    # Trigger the real email delivery
    try:
        send_email_otp(email, otp)
        return {"message": "OTP sent successfully"}
    except Exception as e:
        print(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email")


@router.post("/verify-otp")
async def verify_otp(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    user_otp = data.get("otp")

    if otp_storage.get(email) == user_otp:
        # Clear OTP after successful use
        del otp_storage[email]

        # 1. Create the new session record
        new_session = SessionHistory(
            email=email,
            time_in=datetime.utcnow(),
            time_out=None,  # Will be filled on logout
            duration="Active"  # Placeholder until session ends
        )

        # 2. Add to database and commit
        db.add(new_session)
        db.commit()
        db.refresh(new_session)

        return {"success": True}

    return {"success": False}


@router.post("/logout")
async def logout(email: str, db: Session = Depends(get_db)):
    # 1. Find the specific ACTIVE session record for this user
    # We look for the entry where time_out is still None (the session hasn't ended)
    active_session = db.query(SessionHistory) \
        .filter(SessionHistory.email == email, SessionHistory.time_out == None) \
        .first()

    if not active_session:
        return {"message": "No active session found"}

    # 2. Update the session record
    now = datetime.now(timezone.utc)
    active_session.time_out = now

    # Calculate duration
    duration = now - active_session.time_in.replace(tzinfo=timezone.utc)
    active_session.duration = str(duration)  # Storing as string representation

    # 3. Commit changes
    db.commit()
    db.refresh(active_session)

    return {
        "message": "Logged out successfully",
        "duration": active_session.duration
    }
@router.get("/history/{email}")
def get_history(email: str, db: Session = Depends(get_db)):
    # Fetch all logs for this user, ordered by the most recent first
    return db.query(SessionHistory).filter(SessionHistory.email == email).all()