from flask import Flask

from app.Routes import Routes
from app.Services.SQLiteService import SQLiteService

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ed84ccef7da9e9c5427c0039ddead93e527008a0e8246b9a'
Routes.registerRoutes(app)


if __name__ == '__main__':
    app.run(debug=True)
