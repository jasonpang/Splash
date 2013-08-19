from config import configure_app
from views.users import users
from views.server import server


if __name__ == '__main__':
    app = configure_app(__name__)
    app.register_blueprint(server)
    app.register_blueprint(users)
    app.run(host='0.0.0.0')
