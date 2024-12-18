from flask import Blueprint, render_template, request
from hive.forms import PostMessageForm
from hive.models import Message
from hive.core.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    form = PostMessageForm()
    page = db.paginate(db.select(Message).order_by(Message.created_at.desc()), per_page=100)
    return render_template("index.html", page=page, form=form)

@main_bp.route('/about')
def about():
    return render_template("about.html")