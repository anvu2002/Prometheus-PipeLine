# User Behaviour Analysis

from datetime import datetime
from models import UserAction, SessionLocal

def record_user_action(user_id, action, response_time):
    db = SessionLocal()
    user_action = UserAction(
        user_id=user_id, 
        action=action, 
        response_time=response_time,
        timestamp=datetime.utcnow()
    )
    db.add(user_action)
    db.commit()
    db.close()
