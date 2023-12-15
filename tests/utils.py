from src.models import app_user, event

def reset_db():
    app_user.query.delete()
    event.query.delete()
