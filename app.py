from flask import Flask, redirect, render_template, request, abort

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/login')
def login():
    return render_template('login.html')
