from flask import Blueprint, flash, redirect, render_template, request, url_for
from hive.forms import PostMessageForm
from hive.models import Message
from hive.core.extensions import db

message_bp = Blueprint('message', __name__, url_prefix='/message')

@message_bp.route('/post', methods=['POST'])
def post_message():
    form = PostMessageForm()

    if form.validate_on_submit():
        name = request.form.get('name')
        body = request.form.get('body')
        message = Message(name=name, body=body)
        db.session.add(message)
        db.session.commit()
        flash("Message succesfully added!", "success")
        return(redirect(url_for('main.index')))
    
    flash("Error in message", 'warning')
    return redirect(url_for('main.index'))