from flask import Flask, redirect, render_template, request, abort, session
from datetime import date, datetime

from src.models import db, app_user, event, participatingIn, friends, groups , user_cards
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

@app.route('/about')
def about():
    if 'username' in session:
        return render_template('about.html',in_session = True)
    return render_template('about.html')
    

@app.route('/event/<int:event_id>') #Will change routing to /<event_name> once DB is started
def events(event_id):
    event_data = communifree_repository_singleton.get_event_by_id(event_id)
    event_friends = communifree_repository_singleton.get_friends_by_event(event_id)
    owner=False
    if 'username' in session:
        if session['user_id'] == event_data.author_id:
            owner = True
        return render_template('view_event.html', owner=owner, event_data=event_data,  event_friends= event_friends, in_session = True)
    return render_template('view_event.html', owner=owner, event_data=event_data, event_friends= event_friends)

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
    if 'username' not in session:
        return redirect('/sign_up')
    user_id=session['user_id']
    profile_user=communifree_repository_singleton.get_user_by_id(user_id)
    if profile_user is None:
        abort(400)
    user_card_list=communifree_repository_singleton.list_all_user_cards(user_id)

    return render_template('/profile_sections/home.html', 
                    selfProfilePage=True, 
                    leftEmpty=False, 
                    logged_in=True,  
                    #user_id=session['user_id'],
                    #username=session['username'],
                    #profile_img=session['profile_img'],
                    username=profile_user.username,
                    user_card_list=user_card_list,
                    profile_img=profile_user.profile_img,
                    bio=profile_user.bio
                    )

@app.get('/profile/add')
def create_card_form():
    if 'username' in session:
        return render_template('/profile_sections/add_card.html',in_session=True)
    return redirect('/login')

@app.post('/profile/add')
def create_card():
    header_text = request.form.get("header_text")
    body_text = request.form.get("body_text")
    visibility = request.form.get("visibility_type")
    author_user_id = session['user_id']
    card=communifree_repository_singleton.create_card(header_text,body_text,author_user_id,visibility)
    return redirect('/profile')

@app.get('/profile/<int:card_id>/edit')
def edit_card_page(card_id):
    card = communifree_repository_singleton.get_card_by_id(card_id)
    header_text = card.header_text
    body_text = card.body_text
    visibility = card.visibility
    if 'username' not in session:
        return redirect('/profile')
    if not user_cards:
        return "Card not in database", 400
    
    return render_template('/profile_sections/edit_card.html', in_session=True,
                        header_text=header_text,
                        body_text=body_text,
                        visibility=visibility)


@app.post('/profile/<int:card_id>')
def edit_card(card_id):
    header_text = request.form.get("header_text")
    body_text = request.form.get("body_text")
    visibility = request.form.get("visibility_type")
    communifree_repository_singleton.update_card(card_id, header_text, body_text, visibility)
    communifree_repository_singleton.update_card(card_id, header_text, body_text, visibility)
    return redirect(f'/profile/{card_id}')



@app.post('/profile/<int:card_id>/delete')
def delete_card(card_id: int):
    if 'username' not in session:
        return redirect('/profile')
    db.session.delete(user_cards.query.get(card_id))
    db.session.commit()
    return redirect('/profile')

@app.route('/friends')
def friends_list():
    if 'username' not in session:
        return redirect('/sign_up')
    profile_user=communifree_repository_singleton.get_user_by_id(session['user_id'] )
    friend_list = communifree_repository_singleton.get_friends_list(session['user_id'] )
    return render_template('/profile_sections/friends.html',
                            username=profile_user.username,
                            profile_img=profile_user.profile_img,
                            logged_in=True, 
                            user_selected=False, 
                            selfProfilePage=True, 
                            user="self", 
                            leftEmpty=False, 
                            friend_list=friend_list)

@app.get('/users/<int:user_id>')
def view_user(user_id):
    current_user=1
    profile_user=communifree_repository_singleton.get_user_by_id(user_id)
    if profile_user is None:
        abort(400)
    friend_check = communifree_repository_singleton.get_friend_id(current_user, user_id)
    user_profile_img = profile_user.profile_img
    user_username=profile_user.username
    user_bio = profile_user.bio
    user_user_id=profile_user.user_id

    if current_user==None:
        access = 4
    elif friend_check == None:
        access = 3
    else:
        access = 2

    user_card_list=communifree_repository_singleton.list_accessible_user_cards(user_id, access)

    return render_template('/profile_sections/other_user.html',
                            logged_in=True, 
                            friend_check=friend_check,
                            user_user_id=user_user_id, 
                            access=access,
                            user_profile_img=user_profile_img, 
                            user_username=user_username,
                            user_bio=user_bio,
                            user_card_list=user_card_list
                            )

@app.post('/users/<int:user_id>/deleteFriend')
def remove_friend(user_id: int):
    current_user=1
    friend_id = communifree_repository_singleton.get_friend_id(current_user, user_id)
    db.session.delete(friends.query.get(friend_id))
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.post('/users/<int:user_id>/addFriend')
def add_friend(user_id: int):
    current_user=1
    new_friend = friends(user1_id=current_user, user2_id=user_id)
    db.session.add(new_friend)
    db.session.commit()
    return redirect(f'/users/{user_id}')

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
