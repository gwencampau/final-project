from flask import Flask, redirect, render_template, request, abort

app = Flask(__name__)

about_data = [{"title":"Feeling lonely?", "info":"Well CommuniFree is for you!"},{"title":"Cash strapped?", "info":"Test"},{"title":"For humans by humans", "info":"Test"}]
all_events_data = [{'title': 'ITSC-3155', 'desc': 'Come join us for our weekly meeting on how to cope with a world that has Figma in it!', 'image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'November 13th, 2023'},{'title': 'Graduation Life', 'desc': 'Sad you are not able to graduate just yet? We are too! Join us to cope about this. Pretend to walk the stage with us.', 'image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'November 14th, 2023'},{'title': 'Chancellor Escape Room', 'desc': 'It is time to escape the GABER MANSION! AHHHHHHHHHHHHH! Join us for food and a chance at free tutition.', 'image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'November 15th, 2023'},{'title': 'TA Office Hours', 'desc': 'Hi. We are a couple of students who kinda know what we are doing. Maybe we can help? No promises though.','image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'November 16th, 2023'},{'title': 'Norm', 'desc': 'norm wants your soul give him your soul give him your soul now go niners will he PICK your soul come give us your soul', 'image': 'https://stanforddaily.com/wp-content/uploads/2022/04/chris-ried-ieic5Tq8YMk-unsplash-scaled.jpg', 'date': 'April 9th, 1949'}]
test_create_form_data = []

@app.get('/')
def index():
    return render_template('index.html', events=all_events_data)

@app.get('/create')
def create_form():
    return render_template('create_event.html')

@app.post('/create')
def create_event():
    #This is all just temporary to test that the form works until database is set up
    title = request.form.get("title")
    description = request.form.get("description")
    location = request.form.get("location")
    date = request.form.get("date")
    link = request.form.get("link")
    test_create_form_data.append({title:[description, location, date, link]})
    return redirect('/')

@app.route('/friends')
def friends():
    return render_template('friends.html')

@app.route('/about')
def about():
   
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

@app.get('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/FAQ/account')
def account_faq():
    return render_template('account_faq.html')

@app.route('/FAQ/events')
def events_faq():
    return render_template('event_faq.html')
