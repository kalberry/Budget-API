from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, FieldList, IntegerField, DecimalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Optional
from app.models import check_user

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    last_pay_date = DateField('Last date paid (m/d/y)', validators=[DataRequired()], format='%m/%d/%Y')
    pay_frequency = IntegerField('Pay frequency', validators=[Optional()])
    pay_dates = FieldList(StringField('Pay date', validators=[Optional()]), min_entries=2)
    submit = SubmitField('Register')

    # TODO - Make a proper email check to see if it exists in the database
    #def validate_email(self, email):
    #    user = check_user(email=email.data, password=self.password.data)
    #    if user is not None:
    #        raise ValidationError('Please use a different email address.')

    #TODO - Make a way to see if pay dates or pay frequency is selected, not neither not both
    #def validate_frequency(self, pay_frequency):
    #    if pay_frequency.data and self

class AddBillForm(FlaskForm):
    name = StringField('Name of bill', validators=[DataRequired()])
    cost = DecimalField('Cost of bill', validators=[DataRequired()])
    due_date = IntegerField('Day bill is due', validators=[Optional()])
    frequency = IntegerField('Days until bill due', validators=[Optional()])
    last_paid = DateField('Day bill was last paid (m/d/y)', validators=[DataRequired()], format='%m/%d/%Y')
    category = StringField('Category of bill (optional)', validators=[Optional()])
    submit = SubmitField('Add bill')

    # TODO: Add verification for either frequency or due date, not neither, not both

class AddPayPeriodExpense(FlaskForm):
    name = StringField('Name of bill', validators=[DataRequired()])
    cost = DecimalField('Cost of bill', validators=[DataRequired()])
    category = StringField('Category of bill (optional)', validators=[Optional()])
    submit = SubmitField('Add pay period expense')
