from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, current_user, logout_user

from .models import User
from .forms import LoginForm, UserForm

from application.extensions import db


bp = Blueprint("user", __name__, template_folder="pages", url_prefix="/user")


@bp.route("/")
@login_required
def home():
    return "User profile"


@bp.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == "POST":
        form = LoginForm()
        form.post(request.form)
        
        if form.validate():
            user = User.query.filter_by(user_name=form.user_name).first()
            if user:
                if user.check_pass_word(form.pass_word):
                    login_user(user)
                    flash(f"Welcome {user.user_name}.", category="success")
                    return redirect(url_for("main.home"))
                
            flash("Invalid username / password.", category="error")
    else:
        form = LoginForm()
        
    context = {
        "form": form,
    }
    return render_template("user/login.html", **context)


@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        form = UserForm()
        form.post(request.form)
        if form.validate():
            user = User(
                user_name=form.user_name,
                first_name=form.first_name,
                middle_name=form.middle_name,
                last_name=form.last_name,
                email=form.email
            )
            user.set_pass_word(form.pass_word)
            
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(f"Welcome {user.user_name}.", category="success")
            return redirect(url_for("main.home"))
        
    else:
        form = UserForm()
    
    context = {
        "form": form
    }
    return render_template("user/register.html", **context)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("User logged out.", category="success")
    return redirect(url_for('user.login'))
