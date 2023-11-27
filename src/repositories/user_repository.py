# This highkey doesn't work at the moment
from src.models import AppUser, db

class UserRepository:

    def get_all_users(self):
        all_events = AppUser.query.all()
        return all_events

    def get_user_by_id(self, event_id):
        select_event = AppUser.query.get(event_id)
        return select_event

# Singleton to be used in other modules
user_repository_singleton = UserRepository()
