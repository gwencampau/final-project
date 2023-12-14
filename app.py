from flask import Flask, redirect, render_template, request, abort, session
from datetime import date, datetime

from src.models import db, app_user, event, participatingIn, friends, groups 
from src.repositories.communifree_repository import communifree_repository_singleton

from flask_bcrypt import Bcrypt

import os

import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
     f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/communifree'

app.secret_key = 'chicken_nuggies'

db.init_app(app)

bcrypt = Bcrypt()
bcrypt.init_app(app)

about_data = [{"title":"Fpeeling lonely?", "info":"Well CommuniFree is for you!"},{"title":"Cash strapped?", "info":"Test"},{"title":"For humans by humans", "info":"Test"}]
test_create_form_data = []

@app.get('/')
def index():
    all_events = event.query.all()
    today = date.today()
    if 'username' in session:
        return render_template('index.html', events=all_events, today=today, in_session = True)
    return render_template('index.html', events=all_events, today=today)

@app.get('/group/<int:group_id>')
def view_groups(group_id):
    group_data = communifree_repository_singleton.get_group(group_id)
    event_data = communifree_repository_singleton.get_event_by_id(1)
    print(group_data)
    return render_template('group.html', group_data=group_data)


@app.get('/events/search')
def search_events():
    found_events = []
    q = request.args.get('q', '')
    if q != '':
        found_events = communifree_repository_singleton.search_events(q)
        if 'username' in session:
            return render_template('search_events.html', search_active=True, events=found_events, search_query=q,in_session = True)
        return render_template('search_events.html', search_active=True, events=found_events, search_query=q)
    else:
        return index()


@app.get('/delete/<int:event_id>') #Will change routing to /<event_name> once DB is troubleshot /<int:group_id>
def delete_event(event_id):
    delete = communifree_repository_singleton.get_event_by_id(event_id)
    name = delete.title
    db.session.delete(delete)
    db.session.commit()
    return render_template('delete.html', name=name)

@app.get('/delete/groups/<int:event_id>') #Will change routing to /<event_name> once DB is troubleshot /<int:group_id>
def delete_group(event_id):
    delete = communifree_repository_singleton.get_event_by_id(event_id)
    db.session.delete(delete)
    db.session.commit()
    return render_template('delete.html', )


@app.get('/create')
def create_form():
    if 'username' in session:
        return render_template('create_event.html',in_session=True)
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
    if 'username' in session:
        return render_template('/profile_sections/friends.html',logged_in=True, user_selected=False, selfProfilePage=True, user="self", leftEmpty=False, user_image="/static/test.jpeg", user_username="@Username",in_session = True)
    return render_template('/profile_sections/friends.html',logged_in=True, user_selected=False, selfProfilePage=True, user="self", leftEmpty=False, user_image="/static/test.jpeg", user_username="@Username")

@app.route('/about')
def about():
    if 'username' in session:
        return render_template('about.html',in_session = True)
    return render_template('about.html')
    

@app.route('/event/<int:event_id>') #Will change routing to /<event_name> once DB is started
def events(event_id):
    event_data = communifree_repository_singleton.get_event_by_id(event_id)
    event_friends = communifree_repository_singleton.get_friends_by_event(event_id)
    if 'username' in session:
        return render_template('view_event.html', event_data=event_data,  event_friends= event_friends,in_session = True)
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
    if 'username' in session:
        return render_template('main_faq.html',in_session=True)
    return render_template('main_faq.html')

@app.get('/login')
def login():
    if 'username' in session:
        return redirect('/')
    return render_template('login.html')

@app.route('/login_form', methods=['POST', 'GET'])
def login_post():
    username = request.form.get("username")
    raw_password = request.form.get("password")
    existing_user = app_user.query.filter_by(username=username).first()
    if existing_user and bcrypt.check_password_hash(existing_user.password, raw_password):
        session['username'] = username
        return redirect('/')
    else:
        return render_template('login.html', show_wrong=True)

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('/profile_sections/home.html', selfProfilePage=True, user="self", leftEmpty=False, logged_in=True, user_image="/static/test.jpeg", user_username=session['username'],in_session = True)

    return render_template('/profile_sections/home.html', selfProfilePage=True, user="self", leftEmpty=False, logged_in=True, user_image="/static/test.jpeg", user_username='@username')

@app.route('/settings')
def settings():
    if 'username' in session:
        return render_template('/profile_sections/settings.html',logged_in=True, user_selected=False, selfProfilePage=True, user="self", leftEmpty=False, user_image="/static/test.jpeg", user_username="@Username",in_session= True)


@app.get('/sign_up')
def sign_up():
    if 'username' in session:
        return redirect('/')
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
    if 'username' in session:
       return render_template('account_faq.html',in_session = True) 
    return render_template('account_faq.html')

@app.route('/FAQ/events')
def events_faq():
    if 'username' in session:
        return render_template('event_faq.html',in_session= True)
    return render_template('event_faq.html')

@app.post('/logout')
def logout():
    del session['username']
    return redirect('/')
