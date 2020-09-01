from app import app, db
from flask import render_template, jsonify, url_for, redirect, flash, request
from app.forms import dataForm, uploadFileForm, addUserForm, changePasswordForm
from app.datafile_functions import save_data
from app.models import Data, User
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os


@app.route('/admin')
@login_required
def admin():
    last_json = Data.query.order_by(Data.create_timestamp.desc()).first()
    user_count = User.query.count()
    files_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    files_count = len([file for file in os.listdir(path=files_path) if os.path.isfile(os.path.join(files_path, file))])

    data = {'last_update': last_json,
            'user_count': user_count,
            'files_count': files_count}
    return render_template('admin/admin.html', title='Index - Admin Page', data=data)


@app.route('/urls')
@login_required
def urls():
    page = request.args.get('page', 1, type=int)
    data_json = Data.query.order_by(Data.create_timestamp.desc()).paginate(page, 20, False)
    return render_template('admin/urls.html', title='Index - History', data_json=data_json)


@app.route('/urls/<url_id>')
@login_required
def show_url_json(url_id):
    data_json = Data.query.get_or_404(url_id)
    return render_template('admin/show_url.html', title='Index - Admin Page', data_json=data_json)


@app.route('/edit', methods=['GET'])
@login_required
def edit():
    form = dataForm()
    return render_template('admin/edit.html', title='Index - Edit', form=form)


@app.route('/save', methods=['POST'])
def save_json():
    '''
    get data from DataForm and save it to file if its valid
    return 403 if user not logged in
    '''
    if current_user.is_anonymous:
        return jsonify(message='You must be logged in to do it'), 403

    form = dataForm()
    if form.validate_on_submit():
        filename = app.config['DATA_FILENAME']
        save_data(filename, form.categories.data)
        db.session.commit()
        flash('Changes saved Successfully', 'success')
        return jsonify(message='OK')

    elif form.is_submitted():

        cat_index, cat_val = next((i, v) for i, v in enumerate(form.categories.errors) if v != {})
        if 'items' in cat_val.keys():
            item_index, item_val = next((i, v) for i, v in enumerate(cat_val['items']) if v != {})
            errorMsg = str(list(item_val.values())[0])[2:-2] + ' (' + list(item_val.keys())[0] + ' of Item ' +\
                       str(item_index+1) + ' in Category ' + str(cat_index+1) + ')'
            elem_id = 'category-' + str(cat_index) + '-items-' + str(item_index)
            return jsonify(message=errorMsg, elem_id=elem_id), 400
        elif 'name' in cat_val.keys():
            errorMsg = cat_val['name'][0] + '(name of Category ' + str(cat_index+1) + ')'
            elem_id = 'category-' + str(cat_index) + '-name'
            return jsonify(message=errorMsg, elem_id=elem_id), 400

    return jsonify(message='Bad Request'), 400


@app.route('/files', methods=['GET', 'POST'])
@login_required
def files():
    form = uploadFileForm()
    if form.validate_on_submit():
        f = form.file.data

        ext = os.path.splitext(f.filename)[1]
        if ext not in app.config['UPLOAD_EXTENSIONS']:
            flash('Bad Extention. allowed Extentions are {}'.format(app.config['UPLOAD_EXTENSIONS']), 'danger')
            return redirect(url_for('files'))

        t = str(int(datetime.timestamp(datetime.now())))
        filename = secure_filename(t + '_' + f.filename)
        f.save(os.path.join(app.root_path, 'static', 'uploads', filename))
        flash('/static/uploads/' + filename, 'success')
        return redirect(url_for('files'))

    files_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    files = [{'timestamp': datetime.fromtimestamp(os.path.getctime(os.path.join(files_path, file))),
              'url': '/static/uploads/' + file} for file in os.listdir(path=files_path) if
            os.path.isfile(os.path.join(files_path, file))][::-1]

    return render_template('admin/files.html', title='Admin - Upload Files', form=form, files=files)


@app.route('/admin/user/add', methods=['GET', 'POST'])
@login_required
def add_user():
    form = addUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'User {form.username.data} created successfully', 'success')
        return redirect(url_for('admin'))
    return render_template('admin/add_user.html', title='Admin - Add user', form=form)


@app.route('/admin/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = changePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully', 'success')
            return redirect(url_for('admin'))
        else:
            flash('invalid password', 'danger')
    return render_template('admin/change_password.html', title='Admin - Change Password', form=form)
