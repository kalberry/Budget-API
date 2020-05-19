from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm, RegistrationForm, AddBillForm, AddPayPeriodExpense, EditBillForm, EditPayPeriodExpense
from app.models import User, check_user, register_user, add_bill, add_pay_period_expense, update_bill, find_bill, find_ppe, update_ppe
from datetime import datetime

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

@app.route('/bill/edit/<id>', methods=['GET', 'POST'])
@login_required
def bill_edit(id):
    form = EditBillForm()
    if form.validate_on_submit():
        if update_bill(id, form.name.data, form.cost.data, form.due_date.data, form.frequency.data, form.last_paid.data, form.category.data):
            flash('Bill updated!')
            return redirect(url_for('index'))
        else:
            flash('Bill failed to update!')
            return redirect(url_for('bill_edit', id))

    bill = find_bill(id, current_user.bills)
    if not bill:
        abort(404)

    form.name.data = bill.name
    form.cost.data = bill.cost
    form.due_date.data = bill.due_date
    form.frequency.data = bill.frequency
    form.last_paid.data = datetime.strptime(bill.last_paid, '%Y-%m-%d')
    form.category.data = bill.category
    return render_template('edit_bill.html', title='Update Bill', form=form, bill=bill)

@app.route('/ppe/edit/<id>', methods=['GET', 'POST'])
@login_required
def ppe_edit(id):
    form = EditPayPeriodExpense()
    if form.validate_on_submit():
        if update_ppe(id, form.name.data, form.cost.data, form.category.data):
            flash('Pay period expense updated!')
            return redirect(url_for('index'))
        else:
            flash('Pay period expense failed to update!')
            return redirect(url_for('ppe_edit', id))

    ppe = find_ppe(id, current_user.pay_period_expenses)
    if not ppe:
        abort(404)

    form.name.data = ppe.name
    form.cost.data = ppe.cost
    form.category.data = ppe.category

    return render_template('edit_ppe.html', title='Update Pay Period Expense', form=form, ppe=ppe)

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
