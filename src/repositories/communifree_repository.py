
from src.models import app_user, event, participatingIn, friends, groups, participating_in_group, user_cards, db

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
        f_id = friends.query.filter_by(user1_id=id).where(friends.user2_id==other_id).first()
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
    
    def get_card_by_id(self, id) -> user_cards | None:
        select_card = user_cards.query.get(id)
        return select_card

    def update_card(self, card_id, header_text, body_text, visibility):
        curr_card = user_cards.query.get(card_id)
        curr_card.header_text = header_text
        curr_card.body_text = body_text
        curr_card.visibility = visibility
        return curr_card

    def create_card(self, header_text, body_text, author_user_id, visibility):
        new_card = user_cards(header_text=header_text,body_text=body_text,author_user_id=author_user_id,visibility=visibility)
        db.session.add(new_card)
        db.session.commit()

    def delete_card(self, card_id):
        del_card = user_cards.query.get(card_id).remove()
        db.session.commit()
        
    def get_id_by_user(self, name):
        get_user_id = app_user.query.filter_by(username=name).first()
        return get_user_id.user_id

    def update_user(self, user_id, profile_img, username, bio):
        c_user = app_user.query.get(user_id)
        c_user.profile_img = profile_img
        c_user.username = username
        c_user.bio = bio
        db.session.commit()

    def delete_user(self, user_id):
        del_user = app_user.query.get(user_id).remove()
        db.session.commit()
    
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
    
    def get_group_by_id(self, id):
        select_group = groups.query.get(id)
        return select_group
    
    def update_group(self, group_id, title, description, image_link, tags):
        curr_group = groups.query.get(group_id)
        curr_group.title = title
        curr_group.description = description
        curr_group.image_link = image_link
        curr_group.tags = tags
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
    
    def geocode_location(self, location: str):
        import geopy
        from geopy.geocoders import Nominatim
        import ssl
        import certifi
        
        ctx = ssl.create_default_context(cafile=certifi.where())
        geopy.geocoders.options.default_ssl_context = ctx


        geolocator = Nominatim(scheme='https', user_agent="communifree")
        location_result = geolocator.geocode(location)
        
        if location_result:
            return location_result.latitude, location_result.longitude
        else:
            return None, None
        
    def delete_events(self, id):
        test_part= participatingIn.query.filter_by(event_id=id).delete()
        test_event = event.query.filter_by(event_id=id).delete()
        db.session.commit()
        
        return ""
    def delete_group(self, id):
        test_part =  participating_in_group.query.filter_by(group_id=id).delete()
        test_event = groups.query.filter_by(group_id=id).delete()
        db.session.commit()
        return ""
    def create_group(self, title, description, image_link, tags, author_id):
        new_group = groups(title=title, description=description, image_link=image_link, tags=tags, author_id=author_id)
        db.session.add(new_group)
        db.session.commit()
        return new_group
    
    def join_group(self, u_id, g_id):
        new_join = participating_in_group(user_id=u_id, group_id=g_id)
        db.session.add(new_join)
        db.session.commit()
        return new_join
    
    def get_group_members(self, g_id):
        member = db.session.query(app_user)
        member = member.join(participating_in_group, app_user.user_id == participating_in_group.user_id)
        member = member.join(groups, participating_in_group.group_id == groups.group_id)
        member = member.filter(participating_in_group.group_id == g_id).all()
        return member

    def attend_event(self, u_id, e_id):
        new_attend = participatingIn(user_id=u_id, event_id=e_id)
        db.session.add(new_attend)
        db.session.commit()
        return new_attend

    def unattend_event(self, u_id, e_id):
        unattend = participatingIn.query.filter_by(user_id=u_id, event_id=e_id).delete()
        db.session.commit()
        return unattend

    def check_if_user_attending(self, u_id, e_id):
        if (participatingIn.query.filter_by(user_id=u_id, event_id=e_id).first()):
            return True
        else:
            return False
        
# Singleton to be used in other modules
communifree_repository_singleton = CommunifreeRepository()
