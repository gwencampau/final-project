from flask import Flask, redirect, render_template, request, abort
from datetime import date, datetime

from src.models import db, app_user, event, participatingIn, friends
from src.repositories.communifree_repository import communifree_repository_singleton

from flask_bcrypt import Bcrypt

import os
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
     f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/communifree'

db.init_app(app)

bcrypt = Bcrypt()
bcrypt.init_app(app)

about_data = [{"title":"Fpeeling lonely?", "info":"Well CommuniFree is for you!"},{"title":"Cash strapped?", "info":"Test"},{"title":"For humans by humans", "info":"Test"}]
test_create_form_data = []
display_events = []

@app.get('/')
def index():
    all_events = event.query.all()
    today = date.today()
    
    no_events = [1, 2, 3, 4]

    return render_template('index.html', events=all_events, today=today, no_events=no_events)

@app.get('/events/search')
def search_events():
    found_events = []
    q = request.args.get('q', '')
    if q != '':
        found_events = communifree_repository_singleton.search_events(q)
        return render_template('search_events.html', search_active=True, events=found_events, search_query=q)
    else:
        return index()


@app.get('/delete') #Will change routing to /<event_name> once DB is troubleshot
def delete_event():
    # del = communifree_repository_singleton.get_event_by_id(x)
    # db.session.delete(del)
    # db.session.commit()
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
    whole_date = datetime(request.form.get("date"))
    date = whole_date.date 
    time = whole_date.time
    link = request.form.get("link")
    public = request.form.get("public")
    if not public:
        public = False
    public = True
    new_event = event(title=title, description=description, location=location, date=date, time=time, image_link=link, public=public)
    db.session.add(new_event)
    db.session.commit()
    return redirect('/')

@app.route('/friends')
def friends_list():
    return render_template('/profile_sections/friends.html',logged_in=True, user_selected=False, selfProfilePage=True, user="self", leftEmpty=False, user_image="/static/test.jpeg", user_username="@Username")

@app.route('/about')
def about():
    return render_template('about.html', data=about_data)
    
@app.route('/event') #Will change routing to /<event_name> once DB is started
def events():
    return render_template('view_event.html')

@app.get('/event/edit') 
def edit_event_page():
    return render_template('edit_event.html')

@app.post('/event/edit')
def edit_event():
    return redirect('/event')

@app.route('/FAQ')
def faq():
    return render_template('main_faq.html')

@app.get('/login')
def login():
    return render_template('login.html')

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
