from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from .models import PrivateNote, User
import json
from . import db

views = Blueprint('views', __name__)

# This serves as a method that is called whenever a user enters the home page
@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    # If request is a post method, it means that the user has submitted a note
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category = 'error')
        else:
            new_note = PrivateNote(note_content = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category = 'success')

    return render_template('home.html', user = current_user)

@views.route('/delete-note', methods = ['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = PrivateNote.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

# This is the page where users are able to change their profile details
@views.route('/user-profile', methods = ['GET', 'POST'])
def user_profile():
    # If a POST request has been received that means that a user has submitted information that needs to be changed
    if request.method == 'POST':
        # The new variables are what the user has sent
        newEmail = request.form.get('newEmail')
        newName = request.form.get('newName')
        newPassword = request.form.get('newPassword')
        user = User.query.filter_by(email = current_user.email).one()
        check_user = User.query.filter_by(email= newEmail).first()
        
        # Checks if the user's inputted information is correct
        if check_user:
            flash('Email already exists. Other information has been changed.', category = 'error')
        elif newEmail != '' and '@' in newEmail and '.com' in newEmail:
            user.email = newEmail 
        if newName != '':
            user.first_name = newName
        if newPassword != '' and len(newPassword) > 7:
            user.password = newPassword
        db.session.commit()
        
    return render_template('user_profile.html', user = current_user)
