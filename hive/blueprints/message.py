from flask import Blueprint, flash, redirect, request, url_for

from hive.core.extensions import db, limiter
from hive.forms import PostMessageForm
from hive.models import Message

message_bp = Blueprint('message', __name__, url_prefix='/message')

@message_bp.route('/post', methods=['POST'])
@limiter.limit("20 per hour")
def post_message():
    form = PostMessageForm()

    if form.validate_on_submit():
        name = request.form.get('name').strip()
        body = request.form.get('body').strip()
        message = Message(name=name, body=body)
        db.session.add(message)
        db.session.commit()
        flash("Message succesfully added!", "success")
        return(redirect(url_for('main.index')))
    
    flash(f"Error in message {form.errors.items()}", 'warning')
    return redirect(url_for('main.index'))