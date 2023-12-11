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
        searched_event = event.query.filter(event.title.ilike(title)).all()
        return searched_event
    def get_friends_by_event(self, id):
        # Instructor.query.filter_by(last_name='Garner').all()
        attending = (
    db.session.query(app_user)
    .join(participatingIn, app_user.user_id == participatingIn.user_id)
    .join(friends, (friends.user1_id == app_user.user_id) | (friends.user2_id == app_user.user_id))
    .filter(participatingIn.event_id == id)
    .all()
)
        
        return attending
        

# Singleton to be used in other modules
communifree_repository_singleton = CommunifreeRepository()
