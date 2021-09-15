from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from .models import Note, User
import json
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category = 'error')
        else:
            new_note = Note(note_content = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category = 'success')

    return render_template('home.html', user = current_user)

@views.route('/delete-note', methods = ['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/user-profile', methods = ['GET', 'POST'])
def user_profile():
    if request.method == 'POST':
        newEmail = request.form.get('newEmail')
        newName = request.form.get('newName')
        newPassword = request.form.get('newPassword')
        user = User.query.filter_by(email = current_user.email).one()
        check_user = User.query.filter_by(email= newEmail).first()
        
        if check_user:
            flash('Email already exists.', category = 'error')
        elif newEmail != '' and '@' in newEmail and '.com' in newEmail:
            user.email = newEmail 
        if newName != '':
            user.first_name = newName
        if newPassword != '' and len(newPassword) > 7:
            user.password = newPassword
        db.session.commit()
        
    return render_template('user_profile.html', user = current_user)
