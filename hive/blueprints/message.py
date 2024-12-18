from flask import Blueprint, flash, redirect, render_template, url_for
from hive.forms import PostMessageForm
from hive.models import Message

message_bp = Blueprint('message', __name__, url_prefix='/message')

@message_bp.route('/post', methods=['POST'])
def post_message():
    form = PostMessageForm()

    if form.validate_on_submit():
        flash("Message posted.")
        return redirect(url_for('main.index'))
    
    flash("Error in message", 'warning')
    return redirect(url_for('main.index'))