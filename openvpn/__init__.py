from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager



# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

from openvpn import views

# app.config['SECRET_KEY'] = 'secret-key-goes-here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from openvpn.models import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# blueprint for auth routes in our app
from auth.auth import user_management as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix="/auth")

# blueprint for non-auth parts of app
from googleoauth.oauth import oauth as oauth_blueprint
app.register_blueprint(oauth_blueprint, url_prefix="/googleoauth")

