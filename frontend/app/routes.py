from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm, RegistrationForm
from app.models import User, check_user, register_user

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="home")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = check_user(form.email.data, form.password.data)
        if user is None:
            flash("Invalid email or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = register_user(
        form.email.data,
        form.password.data,
        form.last_pay_date.data.strftime('%m/%d/%Y'),
        form.pay_frequency.data,
        form.pay_dates.data)
        if user:
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        else:
            flash('Register failed!!')
            return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
