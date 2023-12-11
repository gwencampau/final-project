from src.models import app_user, event, participatingIn, friends, db

class CommunifreeRepository:

    def get_all_users(self):
        all_user = app_user.query.all()
        return all_user

    def get_user_by_id(self, id):
        select_user = app_user.query.get(id)
        return select_user
    
    def get_all_events(self):
        all_events = event.query.all()
        return all_events
    
    def get_event_by_id(self, id):
        select_event = event.query.get(id)
        return select_event
    
    def search_events(self, title: str):
        searched_event = event.query.filter(event.title.ilike(f"%{title}%")).all()
        return searched_event

# Singleton to be used in other modules
communifree_repository_singleton = CommunifreeRepository()
