from flask_wtf import FlaskForm
from wtforms import FormField, Form, StringField, PasswordField, SubmitField
from app.fields import UnorderedFieldList
from wtforms.validators import DataRequired, ValidationError, URL, length, EqualTo
from flask_wtf.file import FileField, FileRequired
from app.models import User


class itemForm(Form):
    name = StringField(validators=[DataRequired(), length(max=30)])
    type = StringField(validators=[DataRequired()])
    url = StringField(validators=[DataRequired()])

    def validate_type(self, type):
        valid_values = ['globe', 'file', 'download-alt']
        if type.data not in valid_values:
            raise ValidationError('type not allowed ({})'.format(type.data))


class categoryForm(Form):
    name = StringField(validators=[length(max=30)])
    items = UnorderedFieldList(FormField(itemForm))


class dataForm(FlaskForm):
    '''
    dynamic form, conaines categories and items.
    data sent from edit page.
    '''
    categories = UnorderedFieldList(FormField(categoryForm))


class loginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class uploadFileForm(FlaskForm):
    file = FileField(validators=[FileRequired()])
    submit = SubmitField('Upload')


class addUserForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Add')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('User already exist.')


class changePasswordForm(FlaskForm):
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password_confirm = PasswordField('Confirm Password', validators=[EqualTo('new_password')])
    submit = SubmitField('Change')
