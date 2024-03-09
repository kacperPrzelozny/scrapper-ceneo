from flask import Flask

from app.Routes import Routes

app = Flask(__name__)
Routes.registerRoutes(app)

if __name__ == '__main__':
    app.run(debug=True)
