from flask import Flask, request, redirect, url_for, abort
from flask_migrate import Migrate
from flask_login import LoginManager
from pathlib import Path
from http import HTTPStatus

from . import blueprints
from . extensions import db, bcrypt, mail, migrate


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '4359618c434ed9d52b99638a77e0b4a5'
    app.config['DEBUG'] = True

    instance_path = Path(app.instance_path)
    parent_directory = Path(instance_path.parent)
    if not parent_directory.is_dir():
        parent_directory.mkdir()
    
    if not instance_path.is_dir():
        instance_path.mkdir()
    
    
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return blueprints.user.User.query.get(user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        if request.blueprint == 'api':
            abort(HTTPStatus.UNAUTHORIZED)
        return redirect(url_for('user.login'))
    
    
    # Register Blueprints
    bps = [
        getattr(getattr(blueprints, module), "bp") 
        for module in dir(blueprints) if hasattr(getattr(blueprints, module),"bp")
        ]
    for blueprint in bps:
        app.register_blueprint(blueprint)

    # Initialize the database
    bcrypt.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    
    return app
