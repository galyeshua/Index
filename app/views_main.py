from app import app
from flask import render_template, jsonify, request, url_for, redirect, flash
from app.forms import loginForm
from app.datafile_functions import get_data
from flask_login import login_user, logout_user, current_user
from app.models import User
from werkzeug.urls import url_parse


@app.route('/index')
@app.route('/')
def index():
    filename = app.config['DATA_FILENAME']
    categories = get_data(filename)
    timestamp = categories.get("timestamp", 0)
    return render_template('index.html', title='Index',
                           categories=categories['categories'], timestamp=timestamp)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login', next='/admin'))
        login_user(user, remember=False)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin')
        return redirect(next_page)

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/json', methods=['GET', 'POST'])
def get_json():
    '''
    return jsonify data
    if it is a POST request it will return 403
    '''
    if request.method == 'POST':
        if current_user.is_anonymous:
            return jsonify(message='You must log in to do it'), 403

    filename = app.config['DATA_FILENAME']
    categories = get_data(filename)
    return jsonify(categories)
