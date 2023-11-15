from flask import Flask, redirect, render_template, request, abort

app = Flask(__name__)

about_data = [{"title":"Feeling lonely?", "info":"Well CommuniFree is for you!"},{"title":"Cash strapped?", "info":"Test"},{"title":"For humans by humans", "info":"Test"}]

@app.get('/')
def index():
    return render_template('index.html')

@app.route('/create')
def create():
    return render_template('create_event.html')

@app.route('/friends')
def friends():
    return render_template('friends.html')

@app.route('/about')
def about():
    image = '/templates/images/about.png'
    return render_template('about.html', data=about_data)
    

@app.route('/FAQ')
def faq():
    return render_template('main_faq.html')

@app.get('/login')
def login():
    return render_template('login.html')

@app.get('/sign_up')
def sign_up():
    return render_template('sign_up.html')