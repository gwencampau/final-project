from src.models import app_user, event, participatingIn, friends, groups, db

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
# Singleton to be used in other modules
communifree_repository_singleton = CommunifreeRepository()
