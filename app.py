from flask import Flask, redirect, render_template, request, abort, session
import json
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
        return render_template('index.html', events=all_events, today=today, in_session = True, logged_in = True)
    return render_template('index.html', events=all_events, today=today, logged_in = False)

@app.get('/event/<int:event_id>/attend')
def attend_event(event_id):
    if 'username' not in session:
        abort(404)
    user_id = communifree_repository_singleton.get_id_by_user(session['username'])
    attend = communifree_repository_singleton.attend_event(user_id, event_id)
    return events(event_id)

@app.get('/event/<int:event_id>/unattend')
def unattend_event(event_id):
    if 'username' not in session:
        abort(404)
    user_id = communifree_repository_singleton.get_id_by_user(session['username'])
    unattend = communifree_repository_singleton.unattend_event(user_id, event_id)
    return events(event_id)

@app.get('/group/<int:group_id>')
def view_groups(group_id):
    group_data = groups.query.get(group_id)
    if group_data==None:
         return render_template('error.html')
    in_session=False
    if 'username' in session:
        in_session = True
    return render_template('group.html', group_data=group_data, in_session=in_session)


@app.route('/map')
def map():
    from src.models import db, event
    all_events = event.query.all()
    event_data = []

    for event in all_events:

        if event.latitude == None or event.longitude == None:
            try:
                location = event.location
                latitude, longitude = communifree_repository_singleton.geocode_location(location)
                event.latitude = latitude
                event.longitude = longitude
                db.session.commit()
            except Exception as e:
                print(e)
                continue
        

        event_data.append({
            'id': event.event_id,
            'title': event.title, 
            'description': event.description, 
            'location': event.location, 
            'latitude': event.latitude, 
            'longitude': event.longitude
        })
    
    event_data_json = json.dumps(event_data)

    if 'username' in session:
        return render_template('map.html', event_data_json=event_data_json, in_session = True)
    
    return render_template('map.html', event_data_json=event_data_json)

@app.get('/events/search')
def search_events():
    found_events = []
    q = request.args.get('q', '')
    if q != '':
        found_events = communifree_repository_singleton.search_events(q)
        if 'username' not in session:
            abort(404)
        return render_template('search_events.html', search_active=True, events=found_events, search_query=q,in_session = True)
    else:
        return index()

@app.get('/groups')
def get_all_groups():
    in_session = False
    if 'username' in session:
        in_session = True
    all_groups = groups.query.all()
    id = session['user_id']
    return render_template('get_all_groups.html', in_session=in_session, groups=all_groups, id = id)

@app.get('/delete/<int:event_id>') #Will change routing to /<event_name> once DB is troubleshot /<int:group_id>
def delete_event(event_id):
    communifree_repository_singleton.delete_events(event_id)
    return render_template('delete.html')

@app.get('/delete/group/<int:group_id>') #Will change routing to /<event_name> once DB is troubleshot /<int:group_id>
def delete_group(group_id):
    communifree_repository_singleton.delete_group(group_id)
    return render_template('delete.html' )

@app.get('/create/group')
def create_form_group():
    if 'username' in session:
        return render_template('create_group.html',in_session=True)
    return redirect('/login')

@app.post('/create/group')
def create_group():
    if 'username' in session:
    #Still in progress testing this
        title = request.form.get("title")
        link = request.form.get("link")
        description = request.form.get("description")

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
        author_id = session['user_id']
        group=communifree_repository_singleton.create_group(title, description, link, tags, author_id)
        return redirect('/')
    return redirect('/login')


@app.get('/create')
def create_form_event():
    if 'username' in session:
        return render_template('create_event.html',in_session=True)
    return redirect('/login')

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
    author_id = session['user_id']
    event=communifree_repository_singleton.create_event(title, description, location, date, time, link, public, tags, author_id)
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

    user_id = communifree_repository_singleton.get_id_by_user(session['username'])
    attending = communifree_repository_singleton.check_if_user_attending(user_id, event_id)

    owner=False
    if event_data==None:
        return render_template('error.html')
    if 'username' in session:
        if session['user_id'] == event_data.author_id:
            owner = True
        return render_template('view_event.html', owner=owner, event_data=event_data,  event_friends= event_friends, in_session = True, attending = attending)
    return render_template('view_event.html', owner=owner, event_data=event_data, event_friends= event_friends, attending = attending)

@app.get('/event/<int:event_id>/edit') 
def edit_event_page(event_id):
    event = communifree_repository_singleton.get_event_by_id(event_id)
    if 'username' not in session:
        return redirect(f'/event/{event_id}')
    if session['user_id'] != event.author_id:
        return redirect(f'/event/{event_id}')
    if not event:
        return "Event not in database", 400
    title=event.title
    return render_template('edit_event.html', id=event_id, title=title, in_session=True)

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
        session['user_id'] = existing_user.user_id
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

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404