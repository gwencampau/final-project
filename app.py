from flask import Flask, redirect, render_template, request, abort
from datetime import date, datetime

from src.models import db, app_user, event, participatingIn, friends
from src.repositories.communifree_repository import communifree_repository_singleton

from flask_bcrypt import Bcrypt

import os

import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
     f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/communifree'

db.init_app(app)

bcrypt = Bcrypt()
bcrypt.init_app(app)

about_data = [{"title":"Fpeeling lonely?", "info":"Well CommuniFree is for you!"},{"title":"Cash strapped?", "info":"Test"},{"title":"For humans by humans", "info":"Test"}]
all_events_data = [{'title': 'ITSC-3155', 'desc': 'Come join us for our weekly meeting on how to cope with a world that has Figma in it!', 'image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'November 13th, 2023'},{'title': 'Graduation Life', 'desc': 'Sad you are not able to graduate just yet? We are too! Join us to cope about this. Pretend to walk the stage with us.', 'image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'November 14th, 2023'},{'title': 'Chancellor Escape Room', 'desc': 'It is time to escape the GABER MANSION! AHHHHHHHHHHHHH! Join us for food and a chance at free tutition.', 'image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'November 15th, 2023'},{'title': 'TA Office Hours', 'desc': 'Hi. We are a couple of students who kinda know what we are doing. Maybe we can help? No promises though.','image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'November 16th, 2023'},{'title': 'Norm', 'desc': 'norm wants your soul give him your soul give him your soul now go niners will he PICK your soul come give us your soul', 'image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'April 9th, 1949'}]
test_create_form_data = []
display_events = []

@app.get('/')
def index():
    
    #all_users = communifree_repository_singleton.get_all_users()
    #print(all_users)
    #select_user = communifree_repository_singleton.get_user_by_id(27)
    #print(select_user)

    #all_users = app_user.query.all()
    #print(all_users)
    # all_events = event.query.all()
    # today = date.today()
    # print(all_events)
    # test_thing = event.query.get(1)
    # print(test_thing.event_id)
    # user_event = app_user.query.get(1)
    # print(user_event.author)
    # all_participants = participatingIn.query.all()
    # print(all_participants)
    # all_friends = friends.query.all()
    # print(all_friends)

    # # db.session.query(app_user).delete()
    # # db.session.commit()

    # binary_data = "101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010"
    # binary_data = bytes(binary_data, 'utf-8')
    # new_user = app_user('Hello2', 'World2', binary_data, 'My bio 2')
    # db.session.add(new_user)
    # db.session.commit()
    # print(new_user)

    # # db.session.query(event).delete()
    # # db.session.commit()

    # new_event = event('Event Title', '10/31/2023', '11:00pm', 'image_link.com', 'This is my description for my ultra cool event.', ['cool', 'fun'], 1, True, 'Location')
    # db.session.add(new_event)
    # db.session.commit()
    # print(new_event)

    # # db.session.query(participatingIn).delete()
    # # db.session.commit()

    # new_participant = participatingIn(1, 1)
    # db.session.add(new_participant)
    # db.session.commit()
    # print(new_participant)

    # # db.session.query(friends).delete()
    # # db.session.commit()

    # new_friend = friends(1, 2)
    # db.session.add(new_friend)
    # db.session.commit()
    # print(new_friend)

    all_events = event.query.all()
    today = date.today()
    print(all_events)
    
    return render_template('index.html', events=all_events, today=today)

@app.get('/events/search')
def search_events():
    found_events = []
    q = request.args.get('q', '')
    if q != '':
        found_events = communifree_repository_singleton.search_events(q)
        return render_template('search_events.html', search_active=True, events=found_events, search_query=q)
    else:
        return index()


@app.get('/delete/<int:event_id>') #Will change routing to /<event_name> once DB is troubleshot
def delete_event(event_id):
    delete = communifree_repository_singleton.get_event_by_id(event_id)
    db.session.delete(delete)
    db.session.commit()
    return render_template('delete.html')

@app.get('/create')
def create_form():
    return render_template('create_event.html')

@app.post('/create')
def create_event():
    #Still in progress testing this
    title = request.form.get("title")
    description = request.form.get("description")
    location = request.form.get("location")
    date = request.form.get('date')
    time = request.form.get('time')
    link = request.form.get("link")
    public = request.form.get("public")
    if not public:
        public = False
    public = True
    tags=[]
    if request.form.get('music'):
        tags.append('music')
    if request.form.get('sports'):
        tags.append('sports')
    if request.form.get('gaming'):
        tags.append('gaming')
    if request.form.get('tech'):
        tags.append('tech')
    if request.form.get('crafts'):
        tags.append('crafts')
    event=communifree_repository_singleton.create_event(title, description, location, date, time, link, public, tags)
    return redirect('/')

@app.route('/friends')
def friends_list():
    return render_template('/profile_sections/friends.html',logged_in=True, user_selected=False, selfProfilePage=True, user="self", leftEmpty=False, user_image="/static/test.jpeg", user_username="@Username")

@app.route('/about')
def about():
    return render_template('about.html', data=about_data)
    
@app.route('/event/<int:event_id>') #Will change routing to /<event_name> once DB is started
def events(event_id):
    event_data = communifree_repository_singleton.get_event_by_id(event_id)
    event_friends = communifree_repository_singleton.get_friends_by_event(event_id)
    
    return render_template('view_event.html', event_data=event_data,  event_friends= event_friends)

@app.get('/event/<int:event_id>/edit') 
def edit_event_page(event_id):
    event = communifree_repository_singleton.get_event_by_id(event_id)
    if not event:
        return "Event not in database", 400
    title=event.title
    return render_template('edit_event.html', id=event_id, title=title)

@app.post('/event/<int:event_id>')
def edit_event(event_id):
    title = request.form.get("title")
    description = request.form.get("description")
    location = request.form.get("location")
    date = request.form.get('date')
    time = request.form.get('time')
    link = request.form.get("link")
    public = request.form.get("public")
    if not public:
        public = False
    public = True
    tags=[]
    if request.form.get('music'):
        tags.append('music')
    if request.form.get('sports'):
        tags.append('sports')
    if request.form.get('gaming'):
        tags.append('gaming')
    if request.form.get('tech'):
        tags.append('tech')
    if request.form.get('crafts'):
        tags.append('crafts')
    communifree_repository_singleton.update_event(event_id, title, description, location, date, time, link, public, tags)
    return redirect(f'/event/{event_id}')

@app.route('/FAQ')
def faq():
    return render_template('main_faq.html')

@app.get('/login')
def login():
    return render_template('login.html')

@app.route('/login_form', methods=['POST', 'GET'])
def login_post():
    username = request.form.get("username")
    raw_password = request.form.get("password")
    existing_user = app_user.query.filter_by(username=username).first()
    if existing_user and bcrypt.check_password_hash(existing_user.password, raw_password):
        return redirect('/')
    else:
        return render_template('login.html', show_wrong=True)

@app.route('/profile')
def profile():
    return render_template('/profile_sections/home.html', selfProfilePage=True, user="self", leftEmpty=False, logged_in=True, user_image="/static/test.jpeg", user_username="@Username")

@app.route('/settings')
def settings():
    return render_template('/profile_sections/settings.html',logged_in=True, user_selected=False, selfProfilePage=True, user="self", leftEmpty=False, user_image="/static/test.jpeg", user_username="@Username")


@app.get('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.post('/sign_up_form')
def sign_up_post():
    username = request.form.get("username")
    raw_password = request.form.get("password")
    email = request.form.get("email")
    
    hashed_password = bcrypt.generate_password_hash(raw_password, 12).decode()
    hashed_email = bcrypt.generate_password_hash(email, 12).decode()
    new_user = app_user(hashed_email, username, hashed_password, None, None)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/')

@app.route('/FAQ/account')
def account_faq():
    return render_template('account_faq.html')

@app.route('/FAQ/events')
def events_faq():
    return render_template('event_faq.html')
