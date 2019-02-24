import os
import secrets
from PIL import Image
from wtgnc import mail
from flask import url_for, current_app
from flask_mail import Message


# Function to rename and save profile pictures
def save_picture(form_picture):
    # Rename file with random name to avoid filename collisions
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    # Resize the image to 125x125 pixels
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # Save the picture with a new name and return the filename so it can be updated in the database
    i.save(picture_path)
    return picture_fn


# Function to send a reset email message
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='test.mndev.tech@gmail.com',
                  recipients=[user.email],)
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.password_reset', token=token, _external=True)}

If you did not make this request.  Ignore this email and no changes will be made.

Yours Truly,
WTGNC Helper Bot
'''
    mail.send(msg)