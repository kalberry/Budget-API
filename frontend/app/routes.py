from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm, RegistrationForm, AddBillForm, AddPayPeriodExpense
from app.models import User, check_user, register_user, add_bill, add_pay_period_expense

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

@app.route('/bill/add', methods=['GET', 'POST'])
@login_required
def bill_add():
    form = AddBillForm()
    if form.validate_on_submit():
        bill = add_bill(
        current_user.id,
        form.name.data,
        form.cost.data,
        form.due_date.data,
        form.frequency.data,
        form.last_paid.data,
        form.category.data
        )
        if bill:
            flash('Bill added!')
            return redirect(url_for('index'))
        else:
            flash('Bill failed to add!')
            return redirect(url_for('bill_add'))
    return render_template('add_bill.html', title='Add Bill', form=form)

@app.route('/ppe/add', methods=['GET', 'POST'])
@login_required
def ppe_add():
    form = AddPayPeriodExpense()
    if form.validate_on_submit():
        ppe = add_pay_period_expense(
        current_user.id,
        form.name.data,
        form.cost.data,
        form.category.data
        )
        if ppe:
            flash('Pay period expense added!')
            return redirect(url_for('index'))
        else:
            flash('Pay period expense failed to add!')
            return redirect(url_for('ppe_add'))
    return render_template('add_ppe.html', title='Add Pay Period Expense', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
