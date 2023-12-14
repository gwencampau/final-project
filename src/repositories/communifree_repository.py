from src.models import app_user, event, participatingIn, friends, groups, user_cards, db

class CommunifreeRepository:

    def get_all_users(self):
        all_user = app_user.query.all()
        return all_user

    def get_user_by_id(self, id) -> app_user | None:
        select_user = app_user.query.get(id)
        return select_user
    
    def get_friends_list(self, id):
        friends_list = db.session.query(app_user).join(friends, (friends.user2_id == app_user.user_id)).where(friends.user1_id==id)
        return friends_list
    
    def get_friend_id(self, id, other_id):
        f_id = friends.query.where(friends.user1_id==id and friends.user2_id==other_id).first()
        if f_id != None:
            f_id = f_id.friend_id
        return f_id

    def add_friend(self, id, friend_id):
        new_friend = friends(user1_id=id, user2_id=friend_id)
        db.session.add(new_friend)
        db.session.commit()
        return new_friend
    
    def list_all_user_cards(self, author_id):
        cards_list = db.session.query(user_cards).where(user_cards.author_user_id==author_id).all()
        return cards_list
    
    def list_accessible_user_cards(self, author_id, access):
        cards_list = db.session.query(user_cards).where(user_cards.author_user_id==author_id).where(user_cards.visibility >= access)
        return cards_list
    
    def get_all_events(self):
        all_events = event.query.all()
        return all_events
    
    def get_event_by_id(self, id):
        select_event = event.query.get(id)
        return select_event
    
    def create_event(self, title, description, location, date, time, image_link, public, tags, author_id):
        new_event = event(title=title, description=description, location=location, date=date, time=time, image_link=image_link, public=public, tags=tags, author_id=author_id)
        db.session.add(new_event)
        db.session.commit()
        return new_event

    def update_event(self, event_id, title, description, location, date, time, image_link, public, tags):
        curr_event = event.query.get(event_id)
        curr_event.title = title
        curr_event.description = description
        curr_event.location = location
        curr_event.date = date
        curr_event.time = time
        curr_event.image_link = image_link
        curr_event.public = public
        curr_event.tags = tags
        db.session.commit()
    
    def search_events(self, title: str) -> list[event]:
        found_events: list[event] = event.query.filter(event.title.ilike(f'%{title}%')).all()
        return found_events
    
    def get_friends_by_event(self, id):

        #Updated to be more readable
        attending = db.session.query(app_user)
        attending = attending.join(participatingIn, app_user.user_id == participatingIn.user_id)
        attending = attending.join(friends, (friends.user1_id == app_user.user_id) | (friends.user2_id == app_user.user_id))
        attending = attending.filter(participatingIn.event_id == id).all()
        return attending
        
    def delete_events(self, id):
        test_part= participatingIn.query.filter_by(event_id=id).delete()
        test_event = event.query.filter_by(event_id=id).delete()
        db.session.commit()
        
        return ""
# Singleton to be used in other modules
communifree_repository_singleton = CommunifreeRepository()
