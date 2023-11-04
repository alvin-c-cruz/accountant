from flask import Flask
from flask_migrate import Migrate
from pathlib import Path

from . import blueprints
from . extensions import db


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
           
    # Register Blueprints
    bps = [
        getattr(getattr(blueprints, module), "bp") 
        for module in dir(blueprints) if hasattr(getattr(blueprints, module),"bp")
        ]
    for blueprint in bps:
        app.register_blueprint(blueprint)

    # Initialize the database
    db.init_app(app)
    Migrate(app=app, db=db)
    
    return app
