from flask import Flask, redirect, render_template, request, abort

app = Flask(__name__)

about_data = [{"title":"Feeling lonely?", "info":"Well CommuniFree is for you!"},{"title":"Cash strapped?", "info":"Test"},{"title":"For humans by humans", "info":"Test"}]
all_events_data = [{'title': 'ITSC-3155', 'desc': 'Come join us for our weekly meeting on how to cope with a world that has Figma in it!', 'image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'November 13th, 2023'},{'title': 'Graduation Life', 'desc': 'Sad you are not able to graduate just yet? We are too! Join us to cope about this. Pretend to walk the stage with us.', 'image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'November 14th, 2023'},{'title': 'Chancellor Escape Room', 'desc': 'It is time to escape the GABER MANSION! AHHHHHHHHHHHHH! Join us for food and a chance at free tutition.', 'image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'November 15th, 2023'},{'title': 'TA Office Hours', 'desc': 'Hi. We are a couple of students who kinda know what we are doing. Maybe we can help? No promises though.','image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'November 16th, 2023'},{'title': 'Norm', 'desc': 'norm wants your soul give him your soul give him your soul now go niners will he PICK your soul come give us your soul', 'image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'April 9th, 1949'}]

@app.get('/')
def index():
    return render_template('index.html', events=all_events_data)

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
    
@app.route('/event') #Will change routing to /<event_name> once DB is started
def events():
    return render_template('view_event.html')

@app.route('/FAQ')
def faq():
    return render_template('main_faq.html')

@app.get('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')
