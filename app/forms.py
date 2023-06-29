from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Users


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

def createLeagueForm(setting=None):
    class LeagueForm(FlaskForm):
        pass
    if setting is None:
        LeagueForm.qb = SelectField('QB', choices=[1,2,3,4])
        LeagueForm.rb = SelectField('RB', choices=[1,2,3,4])
        LeagueForm.wr = SelectField('WR', choices=[1,2,3,4])
        LeagueForm.te = SelectField('TE', choices=[1,2,3,4])
        LeagueForm.rb_wr = SelectField('RB/WR', choices=[1,2,3,4])
        LeagueForm.rb_te = SelectField('RB/TE', choices=[1,2,3,4])
        LeagueForm.wr_te = SelectField('WR/TE', choices=[1,2,3,4])
        LeagueForm.rb_wr_te = SelectField('RB/WR/TE', choices=[1,2,3,4])
        LeagueForm.qb_rb_wr_te = SelectField('QB/RB/WR/TE', choices=[1,2,3,4])
        LeagueForm.kicker = SelectField('K', choices=[1,2,3,4])
        LeagueForm.dst = SelectField('DST', choices=[1,2,3,4])
        LeagueForm.scoring = SelectField('Scoring', choices=["Standard","Half PPR", "PPR"])
        LeagueForm.submit = SubmitField('Save Settings')
    else:
        LeagueForm.qb = SelectField('QB', choices=[1,2,3,4], coerce=int, default=setting[0])
        LeagueForm.rb = SelectField('RB', choices=[1,2,3,4], coerce=int, default=setting[1])
        LeagueForm.wr = SelectField('WR', choices=[1,2,3,4], coerce=int, default=setting[2])
        LeagueForm.te = SelectField('TE', choices=[1,2,3,4], coerce=int, default=setting[3])
        LeagueForm.rb_wr = SelectField('RB/WR', choices=[1,2,3,4], coerce=int, default=setting[4])
        LeagueForm.rb_te = SelectField('RB/TE', choices=[1,2,3,4], coerce=int, default=setting[5])
        LeagueForm.wr_te = SelectField('WR/TE', choices=[1,2,3,4], coerce=int, default=setting[6])
        LeagueForm.rb_wr_te = SelectField('RB/WR/TE', choices=[1,2,3,4], coerce=int, default=setting[7])
        LeagueForm.qb_rb_wr_te = SelectField('QB/RB/WR/TE', choices=[1,2,3,4], coerce=int, default=setting[8])
        LeagueForm.kicker = SelectField('K', choices=[1,2,3,4], coerce=int, default=setting[9])
        LeagueForm.dst = SelectField('DST', choices=[1,2,3,4], coerce=int, default=setting[10])
        LeagueForm.scoring = SelectField('Scoring', choices=["Standard","Half PPR", "PPR"], coerce=str, default=setting[11])
        LeagueForm.submit = SubmitField('Save Settings')
    form = LeagueForm()
    return form

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class ViewUsernameRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('View Username via Email')
