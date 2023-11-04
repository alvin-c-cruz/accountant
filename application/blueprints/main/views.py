from flask import Blueprint


bp = Blueprint("main", __name__, template_folder="pages")


@bp.route("/")
def home():
    return "Hello World!"
