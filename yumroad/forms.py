
import flask_wtf
import wtforms

from flask_wtf.form import FlaskForm
from werkzeug.security import check_password_hash
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError
from wtforms import validators
from yumroad.models import User

class ProductForm(FlaskForm):
    name = StringField('Name:', [validators.DataRequired(), validators.Length(min=3, max=60)])
    description = StringField('Description:', [validators.DataRequired()])
    # submit = SubmitField('Create Product')


class SignupForm(FlaskForm):
    ##validator::required() -> [Please fill out this field]
    email = StringField('Email Address:', [validators.DataRequired(), validators.Email(), validators.InputRequired()])
    password = PasswordField('Password:', [validators.DataRequired(), validators.Length(min=4), validators.EqualTo('confirm_password', message='Mat khau khong khop')])
    confirm_password = PasswordField('Confirm Password:',[validators.DataRequired()])
    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        if user is not None:
            raise ValidationError('__form_validate__That email already has an account')
        return True


    # def validate(self): #! self là this của form
    #     check_validate = super(SignupForm, self).validate()
    #     #the default method is define in FlaskForm for Validate login
    #     if not check_validate:
    #         return False
    #     user = User.query.filter_by(email=self.email.data).first()
    #     if user:
    #         self.email.errors.append('__form_validate__That email already has an account') #append error on to the email form
    #         return False
    #     return True


class LoginForm(FlaskForm):
    email = StringField('Email:', [validators.DataRequired(), validators.email()])
    password = PasswordField('Password:', [validators.DataRequired()])
    
    def validate(self):
        #??? check_validate = super(SignupForm, self).validate()
        check_validate = super(LoginForm, self).validate()
        #the default method is define in Platform for Validate login
        if not check_validate:
            return False
        
        user = User.query.filter_by(email=self.email.data).first()
        if not user and not check_password_hash(user.password, self.password.data):
            #mat khau khong hop le, email khong ton tai
            self.email.errors.append('_myerror_Invalid email or password')
            return False
        return True
