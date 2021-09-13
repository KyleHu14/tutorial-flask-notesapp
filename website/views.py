from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
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

        print('Post Request Received : ')
        print(newEmail)
        print(newName)
        print(newPassword)
        
    return render_template('user_profile.html', user = current_user)
