from flask import Flask
from flask_login import LoginManager
#from client import bootstrap_system
from EMS import EMS

app = Flask(__name__)
app.secret_key = "Galigaygay"
EventManageSystem = EMS()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return EventManageSystem.get_user_by_id(user_id) 