from flask import render_template, url_for, flash, redirect
from flask_login import current_user, login_user
from app import app
from app.forms import LoginForm
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="home", user={'username': 'kyle'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user 
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
