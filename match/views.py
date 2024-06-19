from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
import requests

from match import app, db, lm
from match.forms import LoginForm, SignupForm, RankingForm
from match.models import User
from match.authenticate import authenticate
from match.controller import MatchController


allocation = app.config.get('ALLOCATION')
notification = app.config.get('NOTIFICATION')


@app.route('/')
@app.route('/index')
def index():
    api = MatchController(allocation=allocation, notification=notification)

    if api.is_open:
        return redirect(url_for('rank'))
    else:
        return redirect(url_for('results'))


@app.route('/rank', methods=['GET', 'POST'])
@login_required
def rank():
    api = MatchController(allocation=allocation, notification=notification)

    if not api.is_open:
        flash('Ranking is currently closed.')
        return redirect(url_for('results'))

    form = RankingForm()

    if form.is_submitted():
        if form.validate_on_submit():
            rankings = form.ballot.data.split('|')
            if api.is_open:
                api.rank(g.user, *rankings)
            else:
                flash('Ranking closed before your rankings were submitted.')
                return redirect(url_for('results'))

        else:
            flash_errors(form)

    if g.user.is_admin():
        admin_links = [
            ('Match!', url_for('close')),
            ('Clear Rankings', url_for('clear')),
        ]
    else:
        admin_links = []

    return render_template(
        'rank.html',
        title='Match',
        user=g.user,
        options=g.user.no_preferences,
        rankings=g.user.preferences,
        form=form,
        admin_links=admin_links,
        users=api.list_users(ranked=True),
        info=app.config.get('INFO_TEXT')
    )


@app.route('/results')
@login_required
def results():
    api = MatchController(allocation=allocation, notification=notification)

    if g.user.is_admin():
        if api.is_open:
            admin_links = [
                ('Match!', url_for('close')),
                ('Clear Rankings', url_for('clear'))
            ]
        else:
            admin_links = [('Open Match', url_for('open'))]
    else:
        admin_links = []

    return render_template(
        'results.html',
        title='Past Results' if api.is_open else 'Results',
        user=g.user,
        results=api.results(),
        admin_links=admin_links,
        info=app.config.get('INFO_TEXT')
    )


@app.route('/close')
@login_required
def close():
    api = MatchController(allocation=allocation, notification=notification)

    if g.user.is_admin():
        api.close()

    return redirect(url_for('index'))


@app.route('/open')
@login_required
def open():
    api = MatchController(allocation=allocation, notification=notification)

    if g.user.is_admin():
        api.open()

    return redirect(url_for('index'))


@app.route('/clear')
@login_required
def clear():
    api = MatchController(allocation=allocation, notification=notification)

    if g.user.is_admin():
        api.clear()

    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST' and form.validate_on_submit():
        payload = {
            'id': form.username.data,
            'email': form.email.data,
            'password': form.password.data,
            'name': form.name.data,
            'next': url_for('login', _external=True)
        }

        r = requests.post(app.config.get('NEW_USER_URI'), json=payload)

        if r.status_code == 200:
            flash('Success! Please check your email to complete signup.')
            return redirect(url_for('login'))

        else:
            flash(f'Signup failed: {r.text}.')

    elif form.errors:
        flash_errors(form)

    return render_template(
        'signup.html',
        title='Sign Up',
        form=form,
        hide_user=True
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', title='Log In', form=form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user, message = authenticate(username, password)

        if not user:
            flash('Login failed: {}'.format(message))
            return render_template('login.html', title='Log In', form=form)

        if user and user.is_authenticated:
            db_user = User.query.get(user.id)
            if db_user is None:
                db.session.add(user)
                db.session.commit()

            login_user(user, remember=form.remember.data)

            return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@lm.user_loader
def load_user(id):
    return User.query.get(id)


@app.before_request
def before_request():
    g.user = current_user


def flash_errors(form):
    for field, messages in form.errors.items():
        label = getattr(getattr(getattr(form, field), 'label'), 'text', '')
        label = label.replace(':', '')
        error = ', '.join(messages)

        message = f'Error in {label}: {error}' if label else 'Error: {error}'

        flash(message)
        print(message)
