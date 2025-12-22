from flask import Blueprint, render_template

from hive.core.extensions import db
from hive.forms import PostMessageForm
from hive.models import Message

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    form = PostMessageForm()
    page = db.paginate(db.select(Message).order_by(Message.created_at.desc()), per_page=100)
    return render_template("index.html", page=page, form=form)