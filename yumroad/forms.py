
import flask_wtf
import wtforms


from flask_wtf.form import FlaskForm
from werkzeug.security import check_password_hash
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import Length, email, required, EqualTo
from yumroad.models import User

class ProductForm(FlaskForm):
    name = StringField('Name:', [Length(min=3, max=60)])
    description = StringField('Description:')
    # submit = SubmitField('Create Product')

class SignupForm(FlaskForm):

    ##validator::required() -> [Please fill out this field]
    email = StringField('Email:', validators=[email(), required()])
    password = PasswordField('Password:', validators=[required(), Length(min=4), EqualTo('confirm_password', message='Mat khau khong khop')])
    confirm_password = PasswordField('Confirm Password:', validators=[required()])

    def validate(self):
        check_validate = super(SignupForm, self).validate()
        #the default method is define in Platform for Validate login
        if not check_validate:
            return False
        
        user = User.query.filter_by(email=self.email.data).first()
        #fisrt nếu có return True
        if user: #(True -> Neu da co email - Email da ton tai)
            #append error on to the email form
            self.email.errors.append('_myerror_That email already has an account')
            return False
        return True

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[email(), required()])
    password = PasswordField('Password:', validators=[required()])
    
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
    
