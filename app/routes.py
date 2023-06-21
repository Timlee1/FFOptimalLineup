from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import *
from app.models import *
from wtforms.fields.core import *

@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        if current_user.has_league():
            league_setting = current_user.user_league()
            setting = [league_setting.qb, league_setting.rb, league_setting.wr, league_setting.te, league_setting.rb_wr, league_setting.rb_te,
                       league_setting.wr_te, league_setting.rb_wr_te, league_setting.qb_rb_wr_te, league_setting.k, league_setting.dst, league_setting.scoring]                    
            form = LeagueFormTest(setting)
            if form.validate_on_submit():
                league_setting.qb = form.qb.data
                league_setting.rb = form.rb.data
                league_setting.wr = form.wr.data
                league_setting.te = form.te.data
                league_setting.rb_wr = form.rb_wr.data
                league_setting.rb_te = form.rb_te.data
                league_setting.wr_te = form.wr_te.data
                league_setting.rb_wr_te = form.rb_wr_te.data
                league_setting.qb_rb_wr_te = form.qb_rb_wr_te.data
                league_setting.k = form.k.data
                league_setting.dst = form.dst.data
                league_setting.scoring = form.scoring.data
                db.session.commit()
                flash('League Setting Saved')
                return redirect(url_for('home'))
        else:
            form = LeagueFormTest()
            if form.validate_on_submit():
                league_setting = League(qb=form.qb.data, user_id=current_user.id)
                db.session.add(league_setting)
                db.session.commit()
                flash('League Setting Saved')
                return redirect(url_for('home'))
        return render_template('home.html', title = 'Home', form=form)
    return render_template('home.html', title = 'Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/lineup')
def lineup():
    return render_template('lineup.html', title = 'Optimize Lineup')

@app.route('/wdis')
def wdis():
    return render_template('wdis.html', title = 'Who Should I Start')