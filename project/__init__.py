from flask import Flask 
from flask_login import LoginManager 
from .models import db



def create_app(config_name):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/Consultorio.db'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Paciente, Profesional

    @login_manager.user_loader
    def load_user(user_id):
        a =  Paciente.query.get(int(user_id))
        if not a:
            a = Profesional.query.get(int(user_id))
        return a

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .turno import turno as turno_blueprint
    app.register_blueprint(turno_blueprint)

    return app