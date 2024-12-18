from flask import Blueprint, render_template
from hive.forms import PostMessageForm
from hive.models import Message

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    form = PostMessageForm()
    messages = Message.query.all()
    return render_template("index.html", messages=messages[0:8], form=form)

@main_bp.route('/about')
def about():
    return render_template("about.html")