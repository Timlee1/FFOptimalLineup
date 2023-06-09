from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db, mail
from app.forms import *
from app.models import *
from wtforms.fields.core import *
from flask_mail import Message
from app.email import *


@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        if current_user.has_league():
            league_setting = current_user.user_league()
            setting = [league_setting.qb, league_setting.rb, league_setting.wr, league_setting.te, league_setting.rb_wr, league_setting.rb_te,
                       league_setting.wr_te, league_setting.rb_wr_te, league_setting.qb_rb_wr_te, league_setting.kicker, league_setting.dst, league_setting.scoring]                    
            form = createLeagueForm(setting)
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
                league_setting.kicker = form.kicker.data
                league_setting.dst = form.dst.data
                league_setting.scoring = form.scoring.data
                db.session.commit()
                flash('League Setting Saved')
                return redirect(url_for('home'))
        else:
            form = createLeagueForm()
            if form.validate_on_submit():
                league_setting = League(qb=form.qb.data, user_id=current_user.id)
                db.session.add(league_setting)
                db.session.commit()
                flash('League Setting Saved')
                return redirect(url_for('home'))
        players = Player.get_all_players()
        roster = current_user.user_roster()
        roster = sort_by_position(roster)
        opponent_roster = current_user.user_opponent_roster()
        opponent_roster = sort_by_position(opponent_roster)
        return render_template('home.html', title = 'Home', form=form, players=players, roster=roster, opponent_roster=opponent_roster)
    return render_template('home.html', title = 'Home')

@app.route('/player', methods=['GET', 'POST'])
def player():
    if current_user.is_authenticated:
        if request.method == 'POST':
            if request.form['add_or_remove'] == "add":
                player_id = request.form['player_id']
                if request.form['roster_type'] == "roster":
                    if not current_user.is_player_on_user_roster(player_id) and not current_user.is_player_on_user_opponent_roster(player_id):
                        player_to_user = Roster(user_id=current_user.id, player_id=player_id)
                        db.session.add(player_to_user)
                        db.session.commit()
                        flash('Roster Saved')
                else:
                    if not current_user.is_player_on_user_opponent_roster(player_id) and not current_user.is_player_on_user_roster(player_id) :
                        player_to_user = OpponentRoster(user_id=current_user.id, player_id=player_id)
                        db.session.add(player_to_user)
                        db.session.commit()
                        flash('Roster Saved')                   
                    
            if request.form['add_or_remove'] == "remove":
                player_id = request.form['player_id']
                if request.form['roster_type'] == "roster":
                    if current_user.is_player_on_user_roster(player_id):
                        db.session.query(Roster).filter(Roster.user_id==current_user.id).filter(Roster.player_id == player_id).delete()
                        db.session.commit()
                        flash('Roster Saved')
                else:
                    if current_user.is_player_on_user_opponent_roster(player_id):
                        db.session.query(OpponentRoster).filter(OpponentRoster.user_id==current_user.id).filter(OpponentRoster.player_id == player_id).delete()
                        db.session.commit()
                        flash('Roster Saved')
            data = []
            if request.form['roster_type'] == "roster":
                roster = current_user.user_roster().all()
            else:
                roster = current_user.user_opponent_roster().all()
            roster = sort_by_position(roster)
            roster_type = {'roster_type': request.form['roster_type']}
            data.append(roster_type)
            for row in roster:
                row_data = {
                    'id':row.id,
                    'pos':row.pos,
                    'player_name':row.player_name,
                    'team':row.team,
                    'opponent':row.opponent,
                    'home':row.home
                }
                data.append(row_data)
            return jsonify(data)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
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
        user = Users(username=form.username.data, email=form.email.data)
        user.password = user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Users.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/view_username', methods=['GET', 'POST'])
def view_username():
    form = ViewUsernameRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            send_view_username_email(user)
        flash('Check your email to see your username')
        return redirect(url_for('login'))
    return render_template('view_username.html',
                           title='View Username', form=form)

@app.route('/lineup', methods=['GET', 'POST'])
def lineup():
    if current_user.is_authenticated:
        if current_user.has_league():
            league_setting = current_user.user_league()
            setting = [league_setting.qb, league_setting.rb, league_setting.wr, league_setting.te, league_setting.rb_wr, league_setting.rb_te,
                       league_setting.wr_te, league_setting.rb_wr_te, league_setting.qb_rb_wr_te, league_setting.kicker, league_setting.dst, league_setting.scoring]                    
            form = createLeagueForm(setting)
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
                league_setting.kicker = form.kicker.data
                league_setting.dst = form.dst.data
                league_setting.scoring = form.scoring.data
                db.session.commit()
                flash('League Setting Saved')
                return redirect(url_for('lineup'))
        else:
            form = createLeagueForm()
            if form.validate_on_submit():
                league_setting = League(qb=form.qb.data, user_id=current_user.id)
                db.session.add(league_setting)
                db.session.commit()
                flash('League Setting Saved')
                return redirect(url_for('lineup'))
        players = Player.get_all_players()
        roster = current_user.user_roster()
        roster = sort_by_position(roster)
        opponent_roster = current_user.user_opponent_roster()
        opponent_roster = sort_by_position(opponent_roster)
        return render_template('lineup.html', title = 'lineup', form=form, players=players, roster=roster, opponent_roster=opponent_roster)
    return render_template('lineup.html', title = 'lineup')

@app.route('/wdis')
def wdis():
    return render_template('wdis.html', title = 'Who Should I Start')


def sort_by_position(roster):
    res = [] 
    qb = [] 
    rb = [] 
    wr = []
    te = []
    kicker = []
    dst = []
    rest = []
    for player in roster:
        if player.pos == "QB":
            qb.append(player)
        elif player.pos == "RB":
            rb.append(player)
        elif player.pos == "WR":
            wr.append(player)
        elif player.pos == "TE":
            te.append(player)
        elif player.pos == "K":
            kicker.append(player)
        elif player.pos == "DST":
            dst.append(player)
        else:
            rest.append(player)
    res = qb + rb + wr + te + kicker + dst + rest
    return res

