from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class FindUserForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired()], render_kw={"placeholder": "Username"})
    submit = SubmitField('Submit')                                     
